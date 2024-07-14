# pipeline.py
import os

from src.qa_chain import rag_model
from src.vectorstore import VectorStore
from src.data_loader import DatasetLoader
from src.preprocessor import split_documents, preprocess_docs
from config import DOCUMENTS_DIRECTORY

def run_pipeline():

    # file_paths = ['data\8\\ncert-textbook-for-class-8-science-chapter-1.pdf',
    #               'data\8\\ncert-textbook-for-class-8-science-chapter-2.pdf']
    
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
    vectorstore.add_documents(splits)
    
    #4. Test
    query = "Who is the prime minister of USA?"
    rm = rag_model()
    llm_answer = rm.get_llm_answer(query)
    print(llm_answer)
    
if __name__ == "__main__":
    run_pipeline()
