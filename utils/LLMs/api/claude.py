import json
from os import environ
import logging
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT  # pip install anthropic

environ["ANTHROPIC_API_KEY"] = ""  # insert your anthropic key
token = environ.get("ANTHROPIC_API_KEY")


def get_claude_response(prompt: str):
    """

    Args:
        prompt: the prompt to ask the chatbot

    Returns:
        the response from the chatbot

    """

    client = Anthropic(api_key=token)
    response = client.completions.create(
        prompt=f"{HUMAN_PROMPT} {prompt}{AI_PROMPT}",
        model="claude-instant-1",
        max_tokens_to_sample=512,
    )
    return response.completion


# print(get_claude_response("What is the meaning of life?"))
def generate_responses_and_save():
    """
    Reads prompts and categories from a JSONL file, gets responses for each prompt,
    and saves the prompts, categories, and responses in a new JSONL file.

    Returns:
        None
    """
    with open("prompts.jsonl", "r") as input_file, open(
        "claude_responses.jsonl", "w"
    ) as output_file:  # change to appropriate file names
        for line in input_file:
            data = json.loads(line)
            prompt = data["input"][1]["content"]
            category = data["category"]
            response = get_claude_response(prompt)
            result = {"prompt": prompt, "category": category, "response": response}
            output_file.write(json.dumps(result) + "\n")

generate_responses_and_save()
