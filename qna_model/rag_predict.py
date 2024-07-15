import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from qna_model.src.qa_chain import  rag_model
import pandas as pd

rm = rag_model()

def get_answer(question: str):
    result = rm.get_llm_answer(question)
    print(result['answer'])
    
def get_answers(questions: str):
    llm_answers, errors = rm.get_llm_answers(questions)
    if not errors is None:
        print(errors)
        raise Exception(errors)
    return llm_answers


if __name__ == "__main__":
    # query = "Who is the prime minister of India?"
    # get_answer(query)
    
    # queries = ['what are types of Microorganisms', 'what are types of crop seasons']
    # answers, errors= get_answers(questions=queries)
    # print(answers[0], answers)
    # print(errors)
    
    
    input_data =  {
        "inputs": [
            {
                "question": "what are types of Microorganisms",
                "user_input": "bacteria, fungi, protozoa and some algae.."
            },
            {
                "question": "what are types of crop seasons",
                "user_input": "The two types of crop seasons are kharif and rabi crops."
            }
        ]
    }
    input_df = pd.DataFrame(input_data['inputs'])
    # print(input_df.head())
    
    rm = rag_model()
    llm_answers, errors = rm.get_llm_answers(input_df['question'].values.tolist())
    if not errors is None:
        raise Exception(errors)
    # print(llm_answers)
    input_df['llm_answer'] = None
    for index, row in input_df.iterrows():
        if row['question'] == llm_answers[index][0]:
            row['llm_answer'] = llm_answers[index][1]
    print("Done!")