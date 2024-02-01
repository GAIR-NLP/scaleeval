import json
from os import environ
import logging
# pip install openai
import openai

environ["OPENAI_API_KEY"] = ""  # insert your openai key
openai.api_key = environ.get("OPENAI_API_KEY")


def get_gpt_response(prompt: str):
    """

    Args:
        prompt: the prompt to ask the gpt3.5

    Returns:
        the response from the gpt3.5

    """
    messages = [{"role": "user", "content": prompt}]
    model = "gpt-3.5-turbo"  # or gpt-4
    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=512,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].message.content
    return response


def generate_responses_and_save():
    """
    Reads prompts and categories from a JSONL file, gets responses for each prompt,
    and saves the prompts, categories, and responses in a new JSONL file.

    Returns:
        None
    """
    with open("prompts.jsonl", "r") as input_file, open(
        "gpt-3.5-turbo_responses.jsonl", "w"
    ) as output_file:  # change to appropriate file names
        for line in input_file:
            data = json.loads(line)
            prompt = data["input"][1]["content"]
            category = data["category"]
            response = get_gpt_response(prompt)
            result = {"prompt": prompt, "category": category, "response": response}
            output_file.write(json.dumps(result) + "\n")


generate_responses_and_save()
