# Dataset paths
DATASET_PATH = 'data/bio_dataset/combined_dataset.csv'
OPENAI_API_KEY = '<openai api key>'
VECTOR_DB_DIRECTORY = 'docs/chroma/'
DOCUMENTS_DIRECTORY = '/content/'

# Model configurations
SBERT_MODEL_NAME = 'all-mpnet-base-v2'

# Training configurations
BATCH_SIZE = 16
EPOCHS = 1

# Evaluation configurations
SIMILARITY_THRESHOLD = 0.98


# Model names
LLM_NAME = "gpt-3.5-turbo"
SBERT_MODEL_PATH = "models/sbert_model.bin"  # Path to SBERT model
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Prompt template
TEMPLATE = """Use the following pieces of context to answer the question at the end.
explain the answer in 1-2 sentences

If question is not from the uploaded document, just say that you don't know, don't try to make up an answer.
{context}
Question: {question}
Helpful Answer:"""
