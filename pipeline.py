from prefect import task, Flow
from src.data_loader import DataLoader
from src.preprocessor import Preprocessor
from src.model import Model
from src.llm_evaluator import LLMEvaluator
from src.sbert_model import SBERTModel
from dotenv import load_dotenv
import os

@task
def load_env():
    load_dotenv()
    print("Environment variables loaded.")

@task
def load_combined_dataset():
    data_loader = DataLoader()
    combined_data = data_loader.load_combined_dataset()
    return combined_data

@task
def split_dataset(data):
    data_loader = DataLoader()
    train_data, test_data = data_loader.split_dataset(data)
    return train_data, test_data

@task
def preprocess_documents(docs):
    preprocessor = Preprocessor()
    splits = preprocessor.split_documents(docs)
    return splits

@task
def create_vectorstore(splits):
    model = Model()
    vectordb = model.create_vectorstore(splits)
    return vectordb

@task
def create_qa_chain(vectordb):
    model = Model()
    qa_chain = model.create_qa_chain(vectordb)
    return qa_chain

@task
def run_qa_chain(qa_chain, question):
    model = Model()
    answer = model.get_answer(qa_chain, question)
    return answer

@task
def evaluate_gpt_answer(question, student_answer, llm_answer):
    evaluator = LLMEvaluator()
    gpt_evaluation_result = evaluator.compare_sentences(question, student_answer, llm_answer)
    return gpt_evaluation_result

@task
def preprocess_and_finetune_sbert(train_data):
    sbert_model = SBERTModel()
    train_data = sbert_model.preprocess_data(train_data)
    train_examples = sbert_model.create_examples(train_data)
    sbert_model.fine_tune(train_examples)
    return "SBERT model fine-tuned successfully."

@task
def evaluate_sbert(test_data):
    sbert_model = SBERTModel()
    test_data = sbert_model.preprocess_data(test_data)
    test_examples = sbert_model.create_examples(test_data)
    sbert_evaluation_result = sbert_model.evaluate(test_examples)
    return sbert_evaluation_result

@task
def compare_results(gpt_result, sbert_result):
    if gpt_result > sbert_result:
        print("GPT-based evaluation provides better results.")
    elif sbert_result > gpt_result:
        print("SBERT-based evaluation provides better results.")
    else:
        print("Both evaluations provide similar results.")

with Flow(name="Automated Answer Evaluation") as flow:
# def automated_answer_evaluation():
    load_env()
    combined_data = load_combined_dataset()
    train_data, test_data = split_dataset(combined_data)

    splits = preprocess_documents(train_data)
    vectordb = create_vectorstore(splits)
    qa_chain = create_qa_chain(vectordb)

    question = "What does photosynthesis need?"
    student_answer = "Photosynthesis needs oxygen, carbon dioxide, and sunlight"
    llm_answer = run_qa_chain(qa_chain, question)

    gpt_evaluation_result = evaluate_gpt_answer(question, student_answer, llm_answer)

    sbert_finetune_result = preprocess_and_finetune_sbert(train_data)
    sbert_evaluation_result = evaluate_sbert(test_data)

    compare_results(gpt_evaluation_result, sbert_evaluation_result)

if __name__ == "__main__":
    flow.run()
