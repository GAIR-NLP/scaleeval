from __future__ import annotations

import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)


def evaluate_submission(question, submission_1, submission_2, criteria):

    user_prompt = """Compare the two submissions based on the criteria above.
    Which one is better? First, provide a step-by-step explanation of your evaluation
    reasoning according to the criteria. Avoid any potential bias. Ensure that
    the order in which the submissions were presented does not affect your judgement.
    Keep your explanation strictly under 150 words. Afterwards, choose one
    of the following options:
    Submission 1 is better: "1"
    Submission 2 is better: "2"
    Neither is better: "0"

    Directly type in "1" or "2" or "0" (without quotes or punctuation) that corresponds 
    to your reasoning. At the end, repeat just the number again by itself on a new line.
    """

    system_prompt = """You are evaluating two submissions for a particular question,
    using a specific set of criteria. Above is the data."""

    prompt = f"""
        [Question]: '''{question}'''

        [Submission 1]: '''{submission_1}'''

        [Submission 2]: '''{submission_2}'''

        [Criteria]: '''{criteria}'''

        [User]: '''{user_prompt}'''

        """

    return system_prompt, prompt


def start_discussion(
    question,
    submission_1,
    submission_2,
    criteria,
    evaluation_1,
    evaluation_2,
    evaluation_3
):

    user = """Read the question, submissions, criteria, and evaluations above.
    First, explain your thoughts step-by-step about other speakers' evaluations.
    Second, explain your reasoning step-by-step regarding whether or not to change your
    original answer about which submission you think is better after considering other 
    speakers' perspectives. Keep your reasoning strictly under 150 words. Afterwards, 
    choose one of the following options:
    Submission 1 is better: "1"
    Submission 2 is better: "2"
    Neither is better: "0"

    Directly type in "1" or "2" or "0" (without quotes or punctuation) that corresponds 
    to your reasoning. At the end, repeat just the number again by itself on a new line.
    """

    system_prompt_1 = """*Always remember you are Speaker 1*. Review again your own previous 
    evaluations/discussions first, then answer user's request from Speaker 1's perspective. 
    You are discussing with other speakers about your evaluation of the submission responses."""
    system_prompt_2 = """*Always remember you are Speaker 2*. Review again your own previous 
    evaluations/discussions first, then answer user's request from Speaker 2's perspective. 
    You are discussing with other speakers about your evaluation of the submission responses."""
    system_prompt_3 = """*Always remember you are Speaker 3*. Review again your own previous 
    evaluations/discussions first, then answer user's request from Speaker 3's perspective. 
    You are discussing with other speakers about your evaluation of the submission responses."""

    system_prompts = [system_prompt_1, system_prompt_2, system_prompt_3]
    prompt = f"""
            [Question]: '''{question}'''

            [Submission 1]: '''{submission_1}'''

            [Submission 2]: '''{submission_2}'''

            [Criteria]: '''{criteria}'''

            [Speaker 1's Initial Evaluation]: '''{evaluation_1}'''

            [Speaker 2's Initial Evaluation]: '''{evaluation_2}'''

            [Speaker 3's Initial Evaluation]: '''{evaluation_3}'''

            """

    user_prompt = f"""
            [User]: '''{user}'''
            """

    return system_prompts, prompt, user_prompt


def add_discussion_prompt(round_number, speaker_number, discussion_reasoning):
    discussion_prompt = f"""
        [Speaker {speaker_number}'s Discussion - Round {round_number}]:
        '''{discussion_reasoning}'''

        """

    return discussion_prompt


def update_discussion_prompt(
    question,
    submission_1,
    submission_2,
    criteria,
    discussion_1,
    discussion_2,
    discussion_3
):
    prompt = f"""
        [Question]: '''{question}'''

        [Submission 1]: '''{submission_1}'''

        [Submission 2]: '''{submission_2}'''

        [Criteria]: '''{criteria}'''

        [Speaker 1's Previous Discussion]: '''{discussion_1}'''

        [Speaker 2's Previous Discussion]: '''{discussion_2}'''

        [Speaker 3's Previous Discussion]: '''{discussion_3}'''

        """
    return prompt


def generate_criteria_prompt(question, submission_1, submission_2, criteria):
    prompt = f"""
        [Question]: '''{question}'''

        [Submission 1]: '''{submission_1}'''

        [Submission 2]: '''{submission_2}'''

        [Criteria]: '''{criteria}'''

        """
     
    user_prompt = f"""Compare the two submissions based on the criteria above.
    Which one is better? Provide a step-by-step explanation of your evaluation
    reasoning according to the criteria. Avoid any potential bias. Ensure that
    the order in which the submissions were presented does not affect your judgement.
    Keep your explanation strictly under 150 words. Afterwards, choose one
    of the following options:
    Submission 1 is better: "1"
    Submission 2 is better: "2"
    Neither is better: "0"

    Directly type in "1" or "2" or "0" (without quotes or punctuation) that corresponds 
    to your reasoning. At the end, repeat just the number again by itself on a new line.
    """

    return prompt, user_prompt