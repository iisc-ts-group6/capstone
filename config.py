# Dataset paths
DATASET_PATH = 'data/bio_dataset/combined_dataset.csv'
OPENAI_API_KEY= ''
VECTOR_DB_DIRECTORY = '/docs/.chroma/'
CROMADB_COLLECTION_NAME = 'langchain_store'
DOCUMENTS_DIRECTORY = '/content/'
FINETUNE_MODEL_PATH = 'output/sbert'
# Model configurations
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'

# Training configurations
BATCH_SIZE = 16
EPOCHS = 1
TEMPERATURE = 0

TOP_K = 5
RETURN_K = 2
SEARCH_TYPE = 'mmr'
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