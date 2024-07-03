from sentence_transformers import SentenceTransformer, InputExample, losses, evaluation
from torch.utils.data import DataLoader
import numpy as np
from src.preprocessor import Preprocessor
import os
import csv

class SBERTModel:
    def __init__(self, model_name='all-mpnet-base-v2'):
        self.model_name = model_name
        self.model = None
        self.evaluation_metrics = {}
        self.preprocessor = Preprocessor()
    
    def load_model(self, model_path):
        self.model = SentenceTransformer(model_path)
        return self.model
    
    # def __init__(self):
    #     self.model = SentenceTransformer('all-mpnet-base-v2')
    #     self.preprocessor = Preprocessor()

    def preprocess_data(self, df):
        return self.preprocessor.preprocess_data(df)

    def create_examples(self, df):
        examples = []
        for index, row in df.iterrows():
            question = row['question']
            answer = row['answer']
            distractors = [row['D1'], row['D2'], row['D3']]
            examples.append(InputExample(texts=[question, answer], label=1.0))
            for distractor in distractors:
                examples.append(InputExample(texts=[question, distractor], label=0.0))
        return examples

    def fine_tune(self, train_data, epochs=1, batch_size=16, output_path='output/sbert'):
        train_dataloader = DataLoader(train_data, shuffle=True, batch_size=batch_size)
        train_loss = losses.CosineSimilarityLoss(self.model)
        self.model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=epochs, warmup_steps=100)
        self.model.save(output_path)
        
        # Calculate and save evaluation metrics after fine-tuning
        evaluation_result = self.evaluate(train_data)
        self.save_evaluation_metrics("fine_tune", evaluation_result)
                
        # Save metrics to a CSV file
        self.save_metrics_to_csv(output_path, "fine_tune_metrics.csv")


    def evaluate(self, test_data, batch_size=16):
        test_dataloader = DataLoader(test_data, shuffle=False, batch_size=batch_size)
        evaluator = evaluation.EmbeddingSimilarityEvaluator(test_dataloader)
        return self.model.evaluate(evaluator)

    def test_similarity(self, question, correct_answer, student_answer):
        question = self.preprocessor.clean_text(question)
        correct_answer = self.preprocessor.clean_text(correct_answer)
        student_answer = self.preprocessor.clean_text(student_answer)
        embeddings = self.model.encode([question, correct_answer, student_answer])
        sim_score = self.cosine_similarity(embeddings[1], embeddings[2])
        return sim_score

    def cosine_similarity(self, emb1, emb2):
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    
    def save_evaluation_metrics(self, phase, metrics):
        self.evaluation_metrics[phase] = metrics
    
    def get_evaluation_metrics(self):
        return self.evaluation_metrics
    
    def save_metrics_to_csv(self, output_path, filename):
        filepath = os.path.join(output_path, filename)
        with open(filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Phase", "Metrics"])
            for phase, metrics in self.evaluation_metrics.items():
                writer.writerow([phase, metrics])
                    
    def predict(self, question, answer):
        if not self.model:
            raise ValueError("Model has not been loaded. Please load the model first.")

        embeddings = self.model.encode([question, answer])
        similarity_score = self.cosine_similarity(embeddings[0], embeddings[1])

        # Save prediction results
        self.save_evaluation_metrics("prediction", similarity_score)

        return similarity_score
