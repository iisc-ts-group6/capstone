from langchain_chroma import Chroma

from src.qna_embeddings import embedding_func
from config import VECTOR_DB_DIRECTORY, CROMADB_COLLECTION_NAME

class VectorStore:
    def __init__(self):
        self.embeddings = embedding_func
        self.vectorstore = Chroma(collection_name=CROMADB_COLLECTION_NAME, 
                                  embedding_function=self.embeddings,
                                  persist_directory=VECTOR_DB_DIRECTORY)
        
    def add_documents(self, splits):
        self.vectorstore.reset_collection()
        print(f"cleared vector store collection: {CROMADB_COLLECTION_NAME}")
        self.vectorstore.add_documents(splits, embedding=self.embeddings)
        print(f"added {len(splits)} splits to vector store collection")
        
    
    def embed_query(self, query):
        return self.embeddings.embed_query(query)
    
    def embed_query_and_search_by_vector(self, query):
        query_vector = self.embeddings.embed_query(query)
        return self.vectorstore.similarity_search_by_vector(query_vector)
        
    def similarity_search_by_vector(self, embedding_vector):
        return self.vectorstore.similarity_search_by_vector(embedding_vector)

    def as_retriever(self, search_type, search_kwargs):
        return self.vectorstore.as_retriever(search_type=search_type, search_kwargs=search_kwargs)