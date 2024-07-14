import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from qna_model.src.qa_chain import  rag_model

query = "Who is the prime minister of India?"
rm = rag_model()
result = rm.get_llm_answer(query)
print(result['answer'])
