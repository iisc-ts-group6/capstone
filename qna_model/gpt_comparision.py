#gpt_comparision.py

from openai import OpenAI
from dotenv import load_dotenv
import os

from qna_model.config import GPT_MODEL_NAME, TEMPERATURE, GPT_MAX_TOKENS

class gpt_model:
    def __init__(self) -> None:
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.openai_client = OpenAI(api_key=self.api_key)

    # Function to get the comparison and similarity score from GPT
    def compare_sentences(self, question, student_answer, llm_answer) -> list:
        GPT_COMPARISION_PROMPT = f"""You are an assistant that evaluate a student's answer to a Correct answer.

            question: "{question}"
            Student's answer: "{student_answer}"
            Correct answer: "{llm_answer}"

            for the question the correct answer is the "{llm_answer}"
            based on this fact evaluate the "{student_answer}"  and respond in below format

            Answer:Correct/Incorrect/Partially Correct
            Feedback:
            """
            
        response = self.openai_client.chat.completions.create(
            model= GPT_MODEL_NAME,  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": GPT_COMPARISION_PROMPT}
            ],
            max_tokens=GPT_MAX_TOKENS,
            temperature=TEMPERATURE
        )


        # Print the raw response for debugging
        print(f"Raw response:{response}\n")

        #score = float(response.choices[0].message['content'].strip())
        result = response.choices[0].message.content

        print(result)
        
        return result.split("\n\n")
    
    
if __name__ == "__main__":
    gpt_obj = gpt_model()
    
    question = "What are some components or organelles present in the cytoplasm?"
    llm_answer = "Some components or organelles present in the cytoplasm include the nucleus, mitochondria, endoplasmic reticulum, and ribosomes."
    student_answer = "organelles present in the cytoplasm include the nucleus, mitochondria, endoplasmic reticulum."
    
    answer, feedback = gpt_obj.compare_sentences(question,student_answer, llm_answer)
    print(question, llm_answer, student_answer, sep="\n\n", end="\n\n")
    print(answer, feedback, sep="\n\n")     
    