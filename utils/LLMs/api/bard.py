import json
from os import environ

# pip install googlebard
from Bard import Chatbot

environ["BARD_TOKEN"] = ""  # insert your bard key
token = environ.get("BARD_TOKEN")


def get_bard_response(prompt: str):
    """

    Args:
        prompt: the prompt to ask the chatbot

    Returns:
        the response from the chatbot

    """
    chatbot = Chatbot(token)
    response = chatbot.ask(prompt)
    return response


def generate_responses_and_save():
    """
    Reads prompts and categories from a JSONL file, gets responses for each prompt,
    and saves the prompts, categories, and responses in a new JSONL file.

    Returns:
        None
    """
    with open("prompts.jsonl", "r") as input_file, open(
        "bard_responses.jsonl", "w"
    ) as output_file:  # change to appropriate file names
        for line in input_file:
            data = json.loads(line)
            category = data["category"]
            prompt = data["input"][1]["content"]
            response = get_bard_response(prompt)
            result = {"prompt": prompt, "category": category, "response": response["content"]}
            print(response)
            output_file.write(json.dumps(result) + "\n")


generate_responses_and_save()
