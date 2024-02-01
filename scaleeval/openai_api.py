import openai
import time
import re
import logging
from os import environ

logging.basicConfig(level=logging.INFO)

class OpenAI_api:
    def __init__(self):
        self.api_key = environ.get("OPENAI_API_KEY")

    def call(self, sys_prompt, prompt, speaker):
        messages = [
            {"role": "system", "content": "You are a fair, unbiased, and reasonable speaker."},
            {"role": "user", "content": prompt + "\n\n" + sys_prompt},
        ]
        
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model=speaker,
                    messages=messages,
                    temperature=0.5,
                    max_tokens=512,
                    frequency_penalty=0,
                    presence_penalty=0,
                    n=1,
                )
                break
            except Exception as e:
                time.sleep(30)
                print("Error occurred, please wait...", str(e))

        prediction = response["choices"][0]["message"]["content"]
        score = re.findall(r'\d+', prediction)[-1]
        return prediction, score

