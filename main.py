import os
import shutil
import openai
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from openai import OpenAI
from config import OPENAI_API_KEY

CONST_OPENAI_API_KEY =  'OPENAI_API_KEY'
VECTOR_DB_PERSIST_DIR = 'docs/chroma/'
LLM_NAME = "gpt-3.5-turbo"
MAX_TOKENS = 150

def authenticate_open_api():
    # f = open('/content/openapi_key.txt')
    # api_key = f.read()
    # if os.getenv('OPENAI_API_KEY') is None:
    #         os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
    print(OPENAI_API_KEY)
    openai.api_key = OPENAI_API_KEY


def load_pdf_documents(filepaths :list) -> list:
    loaders = [PyPDFLoader(filepath) for filepath in filepaths]
    docs = []
    for loader in loaders:
        docs.extend(loader.load())
    return docs

def split_docs(documents :list, chunk_size:int, chunk_overlap:int) -> list:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap
    )
    return text_splitter.split_documents(documents)


def remove_old_chroma_files(directory_path):
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        try:
            shutil.rmtree(directory_path)
            print(f"Files in directory '{directory_path}' removed successfully.")
        except OSError as e:
            print(f"Error removing directory '{directory_path}': {e}")


def vector_db_store(splits, embeddings) -> Chroma:
    remove_old_chroma_files(VECTOR_DB_PERSIST_DIR)  # remove old database files if any
    vectordb = Chroma.from_documents(
        documents=splits, # splits we created earlier
        embedding=embeddings,
        persist_directory=VECTOR_DB_PERSIST_DIR # save the directory
    )
    vectordb.persist() # Let's **save vectordb** so we can use it later!
    return vectordb

def build_rag_prompt():
    template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}
    Question: {question}
    Helpful Answer:"""
    return PromptTemplate(input_variables=["context", "question"],template=template)

# Function to get the comparison and similarity score from GPT
def compare_sentences(query, input_answer, llm_answer):
    prompt = f"""
    You are an assistant that evaluate a student's answer to a reference answer.

    question: "{query}"
    Student's answer: "{input_answer}"
    Reference answer: "{llm_answer}"

    for the question the correct answer is the "{llm_answer}"
    based on this fact evaluate the "{input_answer}" to be Correct, Partially correct or Incorrect
    """
    client = OpenAI()
    response = client.chat.completions.create(
        model = LLM_NAME,  # or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens= MAX_TOKENS,
        temperature=0
    )
    # result = response.choices[0].message
    # print(result)
    # # Print the extracted result for debugging
    # print("Extracted result:", result)
    return response

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def load_parquet_dataset(doc_locs: str) -> list:
    return [pd.read_parquet(doc_loc) for doc_loc in doc_locs]

def read_directory(directory_path):
    """
    Reads all files in a directory and its subdirectories recursively.

    Args:
        directory_path (str): The path to the directory to read.

    Returns:
        list: A list of absolute paths to all files found in the directory and subdirectories.
    """
    pdf_files = []
    parquet_files = []
    other_files = []
    for root, _, files in os.walk(directory_path):
        for filename in files:
            # Construct the full path to the file
            file_path = os.path.join(root, filename)
            try:
                # Extract file extension (lowercase for case-insensitivity)
                extension = os.path.splitext(filename)[1].lower()
                if extension == ".pdf":
                    pdf_files.append(file_path)
                elif extension == ".parquet":
                    parquet_files.append(file_path)
                else:
                    other_files.append(file_path)
            except (IndexError, PermissionError) as e:
                    print(f"Error processing file '{filename}': {e}")
    return {
        "pdf_files": pdf_files,
        "parquet_files": parquet_files,
        "other_files": other_files  # Add category for non-PDF/Parquet files
    }

def main():
    directory_path = "./data"
    categorized_files = read_directory(directory_path)
    docs = []
    
    if len(categorized_files["other_files"]) > 0:
        print(f"These files are ignored because of incorrect format. Only parquet and pdf supported.")
    
    if len(categorized_files["parquet_files"]) > 0:
        print(f"Parquet files: "+ str(len(categorized_files["parquet_files"])))
        df_list = load_parquet_dataset(categorized_files["parquet_files"][:1])
        # print('Parquet datasets: ', list(df_list))
        print('Parquet dataset shape : ', df_list[0].shape)
        
    if len(categorized_files["pdf_files"]) > 0:
        print(f"\nPDF files: "+ str(len(categorized_files["pdf_files"])))
        file_paths = categorized_files["pdf_files"]
        docs = load_pdf_documents(file_paths[:1])
    
    splits  = split_docs(docs, chunk_size=500, chunk_overlap=50) 
    authenticate_open_api()
    vectorstore = vector_db_store(splits, embeddings=OpenAIEmbeddings(api_key=OPENAI_API_KEY))
    llm = ChatOpenAI(model_name=LLM_NAME, temperature=0)
    retriever = vectorstore.as_retriever(search_type="mmr",search_kwargs={"k": 2, "fetch_k":6} )# "k":2, "fetch_k":3
    QA_CHAIN_PROMPT = build_rag_prompt()
    rag_chain = RetrievalQA.from_chain_type(llm,
                                        retriever=retriever, 
                                        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
                                        return_source_documents=True
                                        )

    question = "Convert the following temperature to celsius scale: a. 300 K b. 573 K?"
    student_answer = "(a)300 K = 22°C\n (b) 573 K = 250°C"
    result = rag_chain.invoke({"query": question})
    llm_answer = result["result"]
    print(result["result"])
    
    response = compare_sentences(question, student_answer, llm_answer)
    

if __name__ == "__main__":
    main()