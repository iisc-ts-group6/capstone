# qa_chain.py

from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
import openai
from config import LLM_NAME, RETURN_K, SEARCH_TYPE, TEMPERATURE, TEMPLATE, TOP_K, OPENAI_API_KEY
from src.vectorstore import VectorStore
import os

class rag_model:
    def __init__(self) -> None:
        self.QA_CHAIN_PROMPT = PromptTemplate(
            input_variables=["context", "question"],
            template=TEMPLATE)
        os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
        self.api_key = os.getenv('OPENAI_API_KEY')
        print(self.api_key)
        openai.api_key = self.api_key
        self.llm = ChatOpenAI(model_name=LLM_NAME, temperature=TEMPERATURE)

    def create_qa_chain(self, llm, retriever):
        return RetrievalQA.from_chain_type(
            llm,
            retriever=retriever,
            chain_type_kwargs={"prompt": self.QA_CHAIN_PROMPT},
            return_source_documents=True
        )

    def get_llm_answer(self, query):
        chroma_client = VectorStore()
        errors = None
        llm_answer = None
        try:
            retriever = chroma_client.as_retriever(
                search_type=SEARCH_TYPE, 
                search_kwargs={"k": RETURN_K, "fetch_k": TOP_K })
            
            qa_chain = self.create_qa_chain(self.llm, retriever)
            
            result = qa_chain.invoke({"query": query})
            llm_answer = result["result"]
        except Exception as e:
            errors = f"Error during processing: {e}"
        return {"question": query, "answer": llm_answer, "errors": errors}
