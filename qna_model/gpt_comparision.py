#gpt_comparision.py

from openai import OpenAI, chat
from openai.types.chat.chat_completion_message import ChatCompletionMessage
from dotenv import load_dotenv
import os

from qna_model.config import GPT_MODEL_NAME, TEMPERATURE, GPT_MAX_TOKENS

class gpt_model:
    def __init__(self) -> None:
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.openai_client = OpenAI(api_key=self.api_key)

    def extract_result(self, message: str): 
        # print("\n...........", type(message.content), "\nFeedback" in str(message.content))
        if "\nFeedback" in str(message):
            return [s.split(":")[1].strip() if "Answer:" in s else s.strip() for s in message.split("\nFeedback:")]
        else:
            return message  
    
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
        GPT_COMPARISION_PROMPT2 = f"""
            Question: "{question}"
            Student's answer: "{student_answer}"
            Actual answer: "{llm_answer}"
            
            Assume that you are an 8th grade Teacher to evaluate student's answer against the actual answer provided.

            Follow below instructions before classifying the answer:
                1. Consider that the student answer and actual answer are from 8th grade science domain, biology subject. 
                2. Consider only by capturing semantic meaning between correct answer and student answer.
                4. Evaluate answer as "correct" when student answer correctly conveys the main idea.
                
            Answer:Positive/Neutral/Negative
            Feedback:
            """
        
        # print(GPT_COMPARISION_PROMPT)
            
        response = self.openai_client.chat.completions.create(
            model= GPT_MODEL_NAME,  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": GPT_COMPARISION_PROMPT2}
            ],
            max_tokens=GPT_MAX_TOKENS,
            temperature=TEMPERATURE
        )
        # print(f"Raw response => {response}")
        message_content = response.choices[0].message.content
        print(message_content)
        return message_content     
    
    
if __name__ == "__main__":
    gpt_obj = gpt_model()
    
    question = "Why should harvested grains be kept safe from moisture, insects, rats, and microorganisms?"
    llm_answer = "Harvested grains should be kept safe from moisture, insects, rats, and microorganisms to prevent spoilage or attacks by organisms that can make them unfit for use or germination. Proper drying of grains in the sun reduces moisture, preventing attacks by insect pests, bacteria, and fungi."
    student_answer = "Drying grains adequately under sunlight is key to decreasing moisture content, which helps in warding off pests like insects, harmful bacteria, and fungi."
    
    chat_message = gpt_obj.compare_sentences(question, student_answer, llm_answer)
    answer, feedback = gpt_obj.extract_result(chat_message)
    print(question, llm_answer, student_answer, sep="\n\n", end="\n\n")
    print(answer, feedback, sep="\n\n")     
    