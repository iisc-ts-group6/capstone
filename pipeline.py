# pipeline.py

from src.qa_chain import rag_model
from src.vectorstore import VectorStore
# from langchain_openai import ChatOpenAI

from src.data_loader import DatasetLoader
from src.preprocessor import split_documents, preprocess_docs
# from config import LLM_NAME, TEMPERATURE, SEARCH_TYPE, RETURN_K, TOP_K
import os, openai

def run_pipeline():
    f = open('openapi_key.txt')
    api_key = f.read()
    os.environ['OPENAI_API_KEY'] = api_key
    openai.api_key= os.getenv('OPENAI_API_KEY')

    file_paths = ['data\8\\ncert-textbook-for-class-8-science-chapter-1.pdf',
                  'data\8\\ncert-textbook-for-class-8-science-chapter-2.pdf']
    # 1. Load and preprocess the docs 
    data_loader = DatasetLoader()
    docs = data_loader.load_pdfs(file_paths)
    docs = preprocess_docs(docs)
    
    #2.split into chunks    
    splits = split_documents(docs)
    
    #3. add to vector db
    vectorstore = VectorStore()
    vectorstore.add_documents(splits)
    
    # retriever = vectorstore.as_retriever(search_type=SEARCH_TYPE, search_kwargs={"k": RETURN_K, "fetch_k": TOP_K })
    # llm = ChatOpenAI(model_name=LLM_NAME, temperature=TEMPERATURE)
    # qa_chain = create_qa_chain(llm, retriever)
    
    query = "how many types of crop seasons in India?"
    # result = qa_chain.invoke({"query": query})
    # llm_answer = result["result"]
    rm = rag_model()
    llm_answer = rm.get_llm_answer(query)
    print(llm_answer)
    # print(query, llm_answer, sep="\n")
    # Pass answer to comparison model
    # Example: comparison.compare_with_user_input(answer, user_input)    
    
if __name__ == "__main__":
    run_pipeline()
