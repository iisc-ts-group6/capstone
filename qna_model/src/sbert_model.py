import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from sentence_transformers import SentenceTransformer, InputExample, losses, evaluation
from torch.utils.data import DataLoader
import numpy as np
import pandas as pd
import os
import csv
from dotenv import load_dotenv

import qna_model.src.preprocessor as pp
from qna_model.config import sts_model_name, FINETUNE_MODEL_PATH, HF_FINTUNE_MODEL_PATH, EPOCHS, BATCH_SIZE,WARMUP_STEPS


class SBERTModel:
    def __init__(self):
        self.evaluation_metrics = {}
        self.output_model_path= FINETUNE_MODEL_PATH
        self.model =  SentenceTransformer(sts_model_name)
        
    
    def load_model(self, model_path):
        self.model = SentenceTransformer(model_path)
        return self.model
    
    def preprocess_data(self, df):
        return pp.preprocess_data(df)

    def create_examples(self, df: pd.DataFrame):
        examples = []
        # print(df.columns.tolist(), type(df))
        for index, row in df.iterrows():
            question = row['Question']
            answer = row['Answer']
            distractors = [row['D1'], row['D2'], row['D3']]
            examples.append(InputExample(texts=[question, answer], label=1.0))
            for distractor in distractors:
                examples.append(InputExample(texts=[question, distractor], label=0.0))
        return examples
    
    def df_to_input_examples(self, df):
        # Convert pairs and labels to InputExample format
        pairs = df[['Sentence1', 'Sentence2']].values.tolist()
        labels = df['Label'].values.tolist() 
        examples = [InputExample(texts=[pair[0], pair[1]], label=label) for pair, label in zip(pairs, labels)]
        print(f"pairs: {len(pairs)}, labels: {len(labels)}, examples: {len(examples)}")
        return examples

    def upload_to_hub(self):
        load_dotenv()
        hf_token = os.getenv('HuggingFace_Access_Token')
        print(hf_token)
        try:
            self.model.push_to_hub(HF_FINTUNE_MODEL_PATH, token=hf_token)
            print("upload is success")
        except Exception as e:
            print(f"error in uploading. {e}")

    def fine_tune(self, train_df: pd.DataFrame, epochs=1, batch_size=16):
        train_examples = self.df_to_input_examples(train_df)
        train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=BATCH_SIZE)
        train_loss = losses.CosineSimilarityLoss(self.model)
        print("train started...")
        # self.upload_to_hub()
        self.model.fit(train_objectives=[(train_dataloader, train_loss)], 
                       epochs=EPOCHS, warmup_steps=WARMUP_STEPS, show_progress_bar=True)        
        print("train ended")
        self.model.save(self.output_model_path)
        
        
    
    def evaluate(self, data, output_path="output/metrics", phase="fine_tune"):
        # test_dataloader = DataLoader(test_data, shuffle=False, batch_size=batch_size)
        train_examples = self.df_to_input_examples(data)
        evaluator = evaluation.EmbeddingSimilarityEvaluator.from_input_examples(train_examples)
        evaluation_result = self.model.evaluate(evaluator)
        self.save_evaluation_metrics(phase, evaluation_result)
        self.save_metrics_to_csv(output_path, f"{phase}_metrics.csv")
        return evaluation_result                

    def test_similarity(self, question, correct_answer, student_answer):
        question = pp.clean_text(question)
        correct_answer = pp.clean_text(correct_answer)
        student_answer = pp.clean_text(student_answer)
        embeddings = self.model.encode([question, correct_answer, student_answer])
        sim_score = self.cosine_similarity(embeddings[1], embeddings[2])
        return sim_score

    def cosine_similarity(self, emb1, emb2):
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    
    def save_evaluation_metrics(self, phase, metrics):
        self.evaluation_metrics[phase] = metrics
    
    def get_evaluation_metrics(self):
        return self.evaluation_metrics
    
    def create_directory(self, filepath):
        # Extract directory path
        directory = os.path.dirname(filepath)
        try:
            # Create directory if it doesn't exist
            if not os.path.exists(directory):
                os.makedirs(directory)  # Create nested directories if necessary

            print(f"Directory created successfully: {directory}")
        except OSError as e:
            print(f"Error creating directory: {e}")

    def save_metrics_to_csv(self, output_path, filename):
        filepath = os.path.join(output_path, filename)
        if not os.path.exists(filepath):
            self.create_directory(filepath)
        with open(filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Phase", "Metrics"])
            for phase, metrics in self.evaluation_metrics.items():
                writer.writerow([phase, metrics])