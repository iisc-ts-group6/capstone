# Prerequisite 
# pip install pandas
# pip install langchain
# pip install langchain_community
# pip install pyarrow
# pip install pypdf
# pip install chromadb
# pip install torch
# pip install -q transformers
# pip install -q sentence-transformers

import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate

def load_dataset(doc_loc: str, doc_type: str):
    if doc_type == 'par': # parquet
        return pd.read_parquet(doc_loc)
    elif doc_type == 'pdf':
        loaders = [PyPDFLoader(doc_loc),]
        docs = []
        for loader in loaders:
            docs.extend(loader.load())
        return docs
    return "ERROR: Dataset load failed. Check file type. Only parquet and pdf supported."

def train_rag(docs: list): # Still working on this. - Vikrant 
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50
    )
    splits = text_splitter.split_documents(docs)
    print(len(splits))
    splits
    model_kwargs = {'device':'cuda'} # cuda/cpu
    # Create a dictionary with encoding options, specifically setting 'normalize_embeddings' to False
    encode_kwargs = {'normalize_embeddings': False}
    embedding =  HuggingFaceEmbeddings(
        model_name=modelPath,     # Provide the pre-trained model's path
        model_kwargs=model_kwargs, # Pass the model configuration options
        encode_kwargs=encode_kwargs # Pass the encoding options
    )
    return True

def import_cuda():
    from torch import cuda
    device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'
    device

def auth_hf():
    import os
    f = open('/content/hfapi_key.txt')
    hfapi_key=f.read()
    os.environ["HF_TOKEN"] = hfapi_key
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = hfapi_key

def prep_llm():
    from langchain_community.llms import HuggingFaceEndpoint
    llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    max_new_tokens = 512,
    top_k = 30,
    temperature = 0.1,
    repetition_penalty = 1.03,
    )
    
def split_doc():
    return True

def create_embeddings():
    return True

def ask_llm(question: str)-> str:
    response=llm.invoke("How to learn programming? give 5 points")
    return response

def main():
    # doc_loc = 'data/data-SciEntsBank/train-00001.parquet' # pick kaggle parquet dataset to load from /data
    # doc_type = 'par'
    # df = load_dataset(doc_loc, doc_type)
    # print('Parquet dataset shape : ', df.shape)

    # doc_loc = 'data/10/jesc1an.pdf' # pick pdf to load from /data
    # doc_type = 'pdf'
    # pdf_text = load_dataset(doc_loc, doc_type)
    # print('PDF dataset :' , pdf_text)

    load_dataset('/data')
    import_cuda()
    auth_hf()
    prep_llm()
    split_doc()
    create_embeddings()
    ask_llm("question")

main()