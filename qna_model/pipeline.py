# pipeline.py

import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

import os
from qna_model.src.qa_chain import rag_model
from qna_model.src.vectorstore import VectorStore
from qna_model.src.data_loader import DatasetLoader
from qna_model.src.preprocessor import split_documents, preprocess_docs
from qna_model.config import DOCUMENTS_DIRECTORY

def run_pipeline():

    # Get the absolute path of the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    # Combine relative path with project directory to get the full path
    pdf_directory = os.path.join(project_dir, DOCUMENTS_DIRECTORY)
    print(pdf_directory)
    # print(os.listdir(pdf_directory))

    # 1. Load and preprocess the docs 
    data_loader = DatasetLoader()
    docs = data_loader.load_pdfs(pdf_directory)
    print(f'loaded documents are: {len(docs)}')
    docs = preprocess_docs(docs)
    
    #2.split into chunks    
    splits = split_documents(docs)
    
    #3. add to vector db
    vectorstore = VectorStore()
    message= vectorstore.add_documents(splits)
    print(message)
    
    # #4. Test
    # query = "Who is the prime minister of USA?"
    # rm = rag_model()
    # llm_answer = rm.get_llm_answer(query)
    # print(llm_answer)
    
if __name__ == "__main__":
    run_pipeline()
