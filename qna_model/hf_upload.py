from sentence_transformers import SentenceTransformer
import os
from qna_model.config import FINETUNE_MODEL_PATH
from dotenv import load_dotenv

load_dotenv()
model = SentenceTransformer(FINETUNE_MODEL_PATH)
hf_token = os.getenv('HuggingFace_Access_Token')
print(hf_token)
try:
    model.push_to_hub("msamg/sts_qna_model", token=hf_token)
    print("upload is success")
except Exception as e:
    print(f"error in uploading. {e}")