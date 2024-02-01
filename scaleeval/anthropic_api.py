import time
import re
import logging
from os import environ
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

logging.basicConfig(level=logging.INFO)

class Anthropic_api:
    def __init__(self):
        self.total_cost = 0.0
        self.token = environ.get("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=self.token)

    def call(self, sys_prompt, prompt, speaker):
        messages = f"""{HUMAN_PROMPT}{prompt}\n\n{sys_prompt}{AI_PROMPT}"""
        while True:
            try:
                response = self.client.completions.create(
                    prompt=messages,
                    max_tokens_to_sample=512,
                    model=speaker,
                    temperature=0.5,
                )
                break

            except Exception as e:
                time.sleep(30)
                print("Error occurred, please wait...", str(e))

        prediction = response.completion
        try:
            score = re.findall(r'\d+', prediction)[-1]
        except:
            score = "0"
            
        return prediction, score
