import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from langchain_huggingface import HuggingFaceEmbeddings
from qna_model.config import EMBEDDING_MODEL_NAME

# embedding_func = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
embedding_func = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    