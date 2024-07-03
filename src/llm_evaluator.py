from langchain.chains import RetrievalQA
import openai
from dotenv import load_dotenv
import os

class LLMEvaluator:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key

    def compare_sentences(self, question, student_answer, llm_answer):
        prompt = f"""
        You are an assistant that evaluate a student's answer to a Correct answer.

        question: "{question}"
        Student's answer: "{student_answer}"
        Correct answer: "{llm_answer}"

        for the question the correct answer is the "{llm_answer}"
        based on this fact evaluate the "{student_answer}"  and respond in below format

        Answer:Correct/Incorrect/Partially Correct
        Feedback:
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0
        )

        result = response.choices[0].message.content
        print(result)

        return result

    def create_qa_chain(self, vectordb):
        self.qa_chain = RetrievalQA.from_chain_type(
            self.llm,
            retriever=vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 2, "fetch_k": 6}),
            chain_type_kwargs={"prompt": self.prompt_template},
            return_source_documents=True
        )