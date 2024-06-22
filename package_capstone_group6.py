# -*- coding: utf-8 -*-
"""Package Capstone_Group6.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XIk-0yg5ZJT21vPxZy_ab9KARdnTuLJV

# Automated answer evaluation

**1. Installing and importing packages**
"""

!pip install openai
!pip install langchain
!pip install langchain-openai
!pip install pypdf
!pip install chromadb
!pip install tiktoken
!pip install langchain-community

!pip install langchain-community

!pip install langchainhub

"""Imports"""

import os
import openai
import numpy as np

"""**Authentication for OpenAI API**"""

f = open('/content/openapi_key.txt')
api_key = f.read()
os.environ['OPENAI_API_KEY'] = api_key
openai.api_key= os.getenv('OPENAI_API_KEY')

"""**Loading the documents**"""

from langchain_community.document_loaders import PyPDFLoader

# Load PDF pypdf2
loaders = [
    # Duplicate documents on purpose
    PyPDFLoader("/content/ncertbio.pdf"),

]
docs = []
for loader in loaders:
    docs.extend(loader.load())

"""**print them**"""

print(docs[0].page_content)

"""# Splitting of document"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

# Split
#from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50
)

splits = text_splitter.split_documents(docs)
print(len(splits))
splits

"""# Embeddings"""

from langchain_openai import OpenAIEmbeddings
embedding = OpenAIEmbeddings()

embedding

"""**Understanding similarity search with a toy example**"""

sentence1 = "i like dogs"
sentence2 = "i like cats"
sentence3 = "the weather is ugly, too hot outside"

embedding1 = embedding.embed_query(sentence1)
embedding2 = embedding.embed_query(sentence2)
embedding3 = embedding.embed_query(sentence3)

len(embedding1), len(embedding2), len(embedding3)

np.dot(embedding1, embedding2), np.dot(embedding1, embedding3),np.dot(embedding2, embedding3)

"""#Vectorstores"""

from langchain_community.vectorstores import Chroma # Light-weight and in memory

persist_directory = 'docs/chroma/'
!rm -rf ./docs/chroma  # remove old database files if any

vectordb = Chroma.from_documents(
    documents=splits, # splits we created earlier
    embedding=embedding,
    persist_directory=persist_directory # save the directory
)

vectordb.persist() # Let's **save vectordb** so we can use it later!

print(vectordb._collection.count()) # same as number of splits

"""# Retrieval + Question Answering : Connecting with LLMs"""

llm_name = "gpt-3.5-turbo"
print(llm_name)

question = "what are Characteristics of Particles of Matter?"
docs = vectordb.max_marginal_relevance_search(question, k=2, fetch_k=3)
len(docs)

docs[0]

docs[1]

"""**Vector store-backed retriever**"""

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model_name=llm_name, temperature=0)

from langchain.chains import RetrievalQA

question = "A diver is able to cut through water in a swimming pool. Which property of matter does this observation show?"

qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectordb.as_retriever(), return_source_documents=True)

result = qa_chain.invoke({"query": question})

result["result"]

result["source_documents"]

from langchain import hub
prompt = hub.pull("rlm/rag-prompt")
prompt

# Build prompt
from langchain.prompts import PromptTemplate
template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template,)

QA_CHAIN_PROMPT

# Run chain
from langchain.chains import RetrievalQA
qa_chain = RetrievalQA.from_chain_type(llm,
                                       retriever=vectordb.as_retriever(search_type="mmr",search_kwargs={"k": 2, "fetch_k":6} ), # "k":2, "fetch_k":3
                                       chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
                                       return_source_documents=True
                                       )

qa_chain

question = "For any substance, why does the temperature remain constant during the change of state?"
result = qa_chain.invoke({"query": question})
result["source_documents"]

result["result"]

question = "Convert the following temperature to celsius scale: a. 300 K b. 573 K"
result = qa_chain.invoke({"query": question})
result["result"]
result["source_documents"]

result["result"]

student_answer = "(a)300 K = 22°C\n (b) 573 K = 250°C"
llm_answer = result["result"]

!pip install --upgrade openai

"""# Compare two sentences using GPT

"""

from openai import OpenAI

client = OpenAI()
# Function to get the comparison and similarity score from GPT
def compare_sentences(question, student_answer, llm_answer):
    prompt = f"""
    You are an assistant that evaluate a student's answer to a reference answer.

    question: "{question}"
    Student's answer: "{student_answer}"
    Reference answer: "{llm_answer}"

    for the question the correct answer is the "{llm_answer}"
    based on this fact evaluate the "{student_answer}" to be Correct, Partially correct or Incorrect
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0
    )


    # Print the raw response for debugging
    #print("Raw response:", response)

    #score = float(response.choices[0].message['content'].strip())
    result = response.choices[0].message
    print(result)
    # Print the extracted result for debugging
    print("Extracted result:", result)

    return response

# Example sentences
question = "what is needed for photsynthesis?"
student_answer = "photsynthesis process needs corbondioxide and sun light"
llm_answer = "photsynthesis process needs corbondioxide and sun light"