# question_answering.py

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class QuestionAnswering:
    def __init__(self, documents, persist_directory):
        self.documents = documents
        self.embedding = OpenAIEmbeddings()  # Initialize OpenAIEmbeddings directly
        self.persist_directory = persist_directory

    def setup_vector_db(self):
        vectordb = Chroma.from_documents(
            documents=self.documents,
            embedding=self.embedding,
            persist_directory=self.persist_directory
        )
        vectordb.persist()
        return vectordb

    def setup_qa_chain(self, llm_name):
        llm = ChatOpenAI(model_name=llm_name, temperature=0)
        prompt = PromptTemplate(input_variables=["context", "question"],
                                template="""Use the following pieces of context to answer the question at the end.
                                            explain the answer in 1-2 sentences
                                            If question is not from the uploaded document, just say that you don't know, don't try to make up an answer.
                                            {context}
                                            Question: {question}
                                            Helpful Answer:""")
        qa_chain = RetrievalQA.from_chain_type(llm,
                                               retriever=self.setup_vector_db().as_retriever(search_type="mmr",
                                                                                               search_kwargs={
                                                                                                   "k": 2,
                                                                                                   "fetch_k": 6}),
                                               chain_type_kwargs={"prompt": prompt},
                                               return_source_documents=True)
        return qa_chain

    def invoke_qa_chain(self, qa_chain, query):
        result = qa_chain.invoke({"query": query})
        return result
