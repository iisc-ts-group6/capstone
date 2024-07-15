# qa_chain.py
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
import openai
import os
from dotenv import load_dotenv

from qna_model.src.vectorstore import VectorStore
from qna_model.config import LLM_NAME, RETURN_K, SEARCH_TYPE, TEMPERATURE, TEMPLATE, TOP_K

class rag_model:
    def __init__(self) -> None:
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key
        if self.api_key != None or self.api_key != '':
            print('assigned api key')
        self.llm = ChatOpenAI(model_name=LLM_NAME, temperature=TEMPERATURE, api_key=self.api_key)
        self.QA_CHAIN_PROMPT = PromptTemplate(
            input_variables=["context", "question"],
            template=TEMPLATE)

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

    def get_llm_answers(self, questions: list):
        print("inside get llm answer")
        chroma_client = VectorStore()
        errors = None
        llm_answers = []
        try:
            retriever = chroma_client.as_retriever(
                search_type=SEARCH_TYPE, 
                search_kwargs={"k": RETURN_K, "fetch_k": TOP_K })
            
            qa_chain = self.create_qa_chain(self.llm, retriever)
            print("calling qa_chain.invoke")
            
            for question in questions:
                try:
                    result = qa_chain.invoke({"query": question})
                    print(result["result"])
                    llm_answers.append((question, result["result"]))
                except Exception as e:
                    errors = f"Error while getting llm_answer processing: {e}"
                    print(errors)
        except Exception as e:
            errors = f"Error while creating qa_chain: {e}"
            print(errors)
        return llm_answers, errors
