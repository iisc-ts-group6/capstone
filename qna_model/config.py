# Dataset paths
DATASET_PATH = 'data/bio_dataset/combined_dataset.csv'
SBERT_DATASET_PATH = 'data/master_sheet_use.csv'
MATERSHEET_FILEPATH = 'data/master_sheet_use.xlsx'
SBERT_TRAIN_DS = 'data/sts_qa_train.csv'
SBERT_EVAL_DS = 'data/sts_qa_eval.csv'
SBERT_TEST_DS = 'data/sts_qa_test.csv'
VECTOR_DB_DIRECTORY = '/docs/chroma/'
CROMADB_COLLECTION_NAME = 'qna_vectordb'
DOCUMENTS_DIRECTORY = 'data/8' 

train_test_split_size =0.2
eval_test_split_size =0.5

# Model configurations
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'

sts_model_name="all-MiniLM-L6-v2"
FINETUNE_MODEL_PATH = f'.trained_models/{sts_model_name}_finetuned'

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