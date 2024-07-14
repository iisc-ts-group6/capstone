from src.qa_chain import  rag_model

query = "Who is the prime minister of India?"
rm = rag_model()
result = rm.get_llm_answer(query)
print(result['answer'])
