from langchain_huggingface import HuggingFaceEmbeddings
from qna_model.config import EMBEDDING_MODEL_NAME

# embedding_func = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
embedding_func = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    