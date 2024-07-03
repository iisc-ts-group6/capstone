from sentence_transformers import SentenceTransformer, InputExample, losses, evaluation
from torch.utils.data import DataLoader
from src.preprocessor import Preprocessor

class Model:
    def __init__(self, model_name='all-mpnet-base-v2'):
        self.model = SentenceTransformer(model_name)
        self.preprocessor = Preprocessor()

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

    def evaluate(self, test_data, batch_size=16):
        test_dataloader = DataLoader(test_data, shuffle=False, batch_size=batch_size)
        evaluator = evaluation.EmbeddingSimilarityEvaluator.from_input_examples(test_dataloader)
        return self.model.evaluate(evaluator)
