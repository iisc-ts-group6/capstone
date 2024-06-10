"""
Install the Google AI Python SDK

$ pip install google-generativeai
json,pandas,time, python-dotenv

You will need to save your GEMINI_API_KEY in environment folder

You need one csv file called Questions.csv (Column header name as Questions)
Script will generate Sample.csv with question,ref_ans,partially_correct_ans and incorrect ans

"""

import os
import json
import pandas as pd
import google.generativeai as genai
import time
from dotenv import load_dotenv

 
load_dotenv()
 
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 0.0,
  "top_p": 1,
  "top_k": 40,
  "max_output_tokens": 256,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)


def remove_markdown(text):
  
        """Removes basic markdown formatting from text.

        Args:
            text: The text with potential markdown formatting.

        Returns:
            The text with markdown formatting removed.
        """
        # Remove leading/trailing whitespace and newlines
        text = text.strip()

        # Escape special characters for safe printing
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text.replace('>', '&gt;')

        # Replace headers with plain text
        text = text.replace('#', '')

        # Remove code block markers
        text = text.replace('```', '')

        return text

questions_df = pd.read_csv('Questions.csv',names=['Questions'],skiprows=1)
cols = ['question','Fully_Correct_Ans','Partially_Correct_Ans','Incorrect_Ans']
df = pd.DataFrame(columns = cols)

context = f"""You are a student of science answering questions"""


for i,row in questions_df.iterrows():
      
        question = row['Questions']
        print(question)        
        validation_prompt = f"""Provide 1 fully correct answer, 1 partially correct answer and 1 incorrect answer to the {question}.
                            return below fields in JSON format:
                            1) Fully Correct : 
                            2) Partially Correct :
                            3) Incorrect :
                            do not provide any justifications or explanations.
                            """
        
        
        
        # Delay for 10 seconds
        time.sleep(10)
        try:
            response = model.generate_content([context, validation_prompt])
        except:
            continue
        
        
        try:
            formatted_response = remove_markdown(response.text).replace('json','')
        except:
            print(f"formatting failed {question}")
            continue
        
        print(formatted_response)
        
        # Assuming the response is a string containing JSON data
        try:
            data_object = json.loads(formatted_response)
            # Access data from the object  
            new_row = {'question':question,
                            'Fully_Correct_Ans':data_object["Fully Correct"],
                            'Partially_Correct_Ans': data_object["Partially Correct"],
                            'Incorrect_Ans':data_object["Incorrect"]
                        }

            df.loc[len(df.index)] = new_row
            print(df.shape)
        except json.JSONDecodeError:
            print(f"Error: The response was not valid JSON for question {question}")
            continue

df.to_csv("sample.csv", index=False) 

