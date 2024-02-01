import json
import logging
from os import environ
from openai_api import OpenAI_api
from anthropic_api import Anthropic_api
import openai
import random

from prompt_input import add_discussion_prompt, evaluate_submission, start_discussion, update_discussion_prompt, generate_criteria_prompt
from tqdm import tqdm
import yaml


environ["OPENAI_API_KEY"] = "" # insert your openai key
openai.api_key = environ.get("OPENAI_API_KEY")
environ["ANTHROPIC_API_KEY"] = ""  # insert your anthropic key

api_openai = OpenAI_api()
api_anthropic = Anthropic_api()


with open("config.yaml") as f:
    config = yaml.safe_load(f)


def load_responses():
    with open(config["evaluation"]["submission1_path"], "r") as f1, open(
        config["evaluation"]["submission2_path"], "r"
    ) as f2:
        sub1 = [json.loads(line) for line in f1.readlines()]
        sub2 = [json.loads(line) for line in f2.readlines()]

    return sub1, sub2


def load_criteria():
    # change file path based on which criteria you want to use
    with open(config["evaluation"]["metric_path"], "r") as f:
        metric = yaml.safe_load(f)
        # need to change the criteria name based on the criteria file
        criteria = metric["criteria"]["helpfulness"]
    return criteria


def generate_init_evaluation():
    sub1, sub2 = load_responses()
    criteria = load_criteria()

    output = []; submission_order = []; speaker_order = []
    with open(config["evaluation"]["results_path"], "w") as result:
        id = 0
        for model1_sub, model2_sub in tqdm(zip(sub1, sub2)):
            assert model1_sub["prompt"] == model2_sub["prompt"]
            id += 1
            question = model1_sub["prompt"]
            submissions = [model1_sub["response"], model2_sub["response"]]
            
            # randomize order of submission
            order = random.randint(0, 1)
            submission_order.append(order)
            submission1 = submissions[order]
            submission2 = submissions[1-order]

            sys_prompt, prompt = evaluate_submission(
                question, submission1, submission2, criteria
            )
            speakers = [config["evaluation"]["speaker1"], config["evaluation"]["speaker2"], config["evaluation"]["speaker3"]]
            order = random.randint(0, 2)
            speaker_order.append(order)
            speakers = [speakers[order], speakers[(order+1)%len(speakers)], speakers[(order+2)%len(speakers)]]
            logging.warning(speakers)

            evals = [None, None, None]
            scores = [None, None, None]

            for i, speaker in enumerate(speakers):
                logging.warning(speaker)
                if speaker.startswith("gpt"):
                    try:
                        evals[i], scores[i] = api_openai.call(
                            sys_prompt, prompt, speaker
                        )
                    except Exception as e:
                        # Handle specific API errors here
                        logging.warning(f"Error calling the API for speaker {speaker}: {e}")
                
                if speaker.startswith("claude"):
                    try:
                        evals[i], scores[i] = api_anthropic.call(
                            sys_prompt, prompt, speaker
                        )
                    except Exception as e:
                        # Handle specific API errors here
                        logging.warning(f"Error calling the API for speaker {speaker}: {e}")

            data = {
                "id": id,
                "Question": question,
                "Submission 1": submission1,
                "Submission 2": submission2,
                "Speaker 1 - Initial Evaluation": {
                    "reasoning": evals[0],
                    "score": scores[0],
                },
                "Speaker 2 - Initial Evaluation": {
                    "reasoning": evals[1],
                    "score": scores[1],
                },
                "Speaker 3 - Initial Evaluation": {
                    "reasoning": evals[2],
                    "score": scores[2],
                },
            }
            output.append(data)
            json.dump(data, result, ensure_ascii=False, indent=4)
            result.write("\n")

    return output, submission_order, speaker_order


def generate_discussion(output, submission_order, speaker_order):
    sub1, sub2 = load_responses()
    # add evaluation results to prompt for input
    for i, (model1_sub, model2_sub) in enumerate(tqdm(zip(sub1, sub2))):
        submissions = [model1_sub["response"], model2_sub["response"]]
        submission1 = submissions[submission_order[i]]
        submission2 = submissions[1-submission_order[i]]

        # check if all speaker agree on the initial evaluation
        if config["discussion"]["equal_score"] and (
            output[i]["Speaker 1 - Initial Evaluation"]["score"]
            == output[i]["Speaker 2 - Initial Evaluation"]["score"]
            == output[i]["Speaker 3 - Initial Evaluation"]["score"]
        ):
            continue

        system_prompts, prompt, user_prompt = start_discussion(
            model1_sub["prompt"],
            submission1,
            submission2,
            load_criteria(),
            output[i]["Speaker 1 - Initial Evaluation"]["reasoning"],
            output[i]["Speaker 2 - Initial Evaluation"]["reasoning"],
            output[i]["Speaker 3 - Initial Evaluation"]["reasoning"],
        )
        speakers = [config["evaluation"]["speaker1"], config["evaluation"]["speaker2"], config["evaluation"]["speaker3"]]
        speakers = [speakers[speaker_order[i]], speakers[(speaker_order[i]+1)%len(speakers)], speakers[(speaker_order[i]+2)%len(speakers)]]

        # accumulate prompt user input after a speaker speaks
        discussion_prompts = prompt
        for round_number in range(config["discussion"]["num_round"]):
            discussions = [None, None, None]
            scores = [None, None, None]

            if speakers[0].startswith("gpt"):
                discussions[0], scores[0] = api_openai.call(
                    system_prompts[0],
                    discussion_prompts + "\n\n" + user_prompt,
                    speakers[0],
                )
            elif speakers[0].startswith("claude"):
                discussions[0], scores[0] = api_anthropic.call(
                    system_prompts[0],
                    discussion_prompts + "\n\n" + user_prompt,
                    speakers[0],
                )

            discussion_prompts = (
                discussion_prompts
                + "\n\n"
                + add_discussion_prompt(round_number + 1, 1, discussions[0])
            )

            if speakers[1].startswith("gpt"):
                discussions[1], scores[1] = api_openai.call(
                    system_prompts[1],
                    discussion_prompts + "\n\n" + user_prompt,
                    speakers[1],
                )
            elif speakers[1].startswith("claude"):
                discussions[1], scores[1] = api_anthropic.call(
                    system_prompts[1],
                    discussion_prompts + "\n\n" + user_prompt,
                    speakers[1],
                )

            discussion_prompts = (
                discussion_prompts
                + "\n\n"
                + add_discussion_prompt(round_number + 1, 2, discussions[1])
            )

            if speakers[2].startswith("gpt"):
                discussions[2], scores[2] = api_openai.call(
                    system_prompts[2],
                    discussion_prompts + "\n\n" + user_prompt,
                    speakers[2],
                )
            elif speakers[2].startswith("claude"):
                discussions[2], scores[2] = api_anthropic.call(
                    system_prompts[2],
                    discussion_prompts + "\n\n" + user_prompt,
                    speakers[2],
                )

            discussion_prompts = update_discussion_prompt(
                model1_sub["prompt"],
                submission1,
                submission2,
                load_criteria(),
                discussions[0],
                discussions[1],
                discussions[2],
            )

            # save discussion results
            output[i]["Speaker 1 - Discussion Round " + str(round_number + 1)] = {
                "reasoning": discussions[0],
                "score": scores[0],
            }
            output[i]["Speaker 2 - Discussion Round " + str(round_number + 1)] = {
                "reasoning": discussions[1],
                "score": scores[1],
            }
            output[i]["Speaker 3 - Discussion Round " + str(round_number + 1)] = {
                "reasoning": discussions[2],
                "score": scores[2],
            }

            # check if all speaker agree after discussion
            if config["discussion"]["equal_score"] and (len(set(scores)) == 1):
                break

    with open(config["evaluation"]["results_path"], "w") as result:
        json.dump(output, result, ensure_ascii=False, indent=4)

def speaker1_score(speaker_order):
    with open(config["evaluation"]["results_path"], "r") as r:
        agent_scores = json.load(r)

    extracted_data = []
    for i in range(len(speaker_order)):
        if speaker_order[i] == 0:
            data = {
                "ID": agent_scores[i]["id"],
                "Score": agent_scores[i]["Speaker 1 - Initial Evaluation"]["score"],
                "Reasoning": agent_scores[i]["Speaker 1 - Initial Evaluation"]["reasoning"],
            }
        elif speaker_order[i] == 1:
            data = {
                "ID": agent_scores[i]["id"],
                "Score": agent_scores[i]["Speaker 3 - Initial Evaluation"]["score"],
                "Reasoning": agent_scores[i]["Speaker 3 - Initial Evaluation"]["reasoning"],
            }
            
        elif speaker_order[i] == 2:
            data = {
                "ID": agent_scores[i]["id"],
                "Score": agent_scores[i]["Speaker 2 - Initial Evaluation"]["score"],
                "Reasoning": agent_scores[i]["Speaker 2 - Initial Evaluation"]["reasoning"],
            }
        extracted_data.append(data)
    
    with open(config["evaluation"]["speaker1_score_path"], "w") as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=4)
        

def speaker2_score(speaker_order):
    with open(config["evaluation"]["results_path"], "r") as r:
        agent_scores = json.load(r)

    extracted_data = []
    for i in range(len(speaker_order)):
        if speaker_order[i] == 0:
            data = {
                "ID": agent_scores[i]["id"],
                "Score": agent_scores[i]["Speaker 2 - Initial Evaluation"]["score"],
                "Reasoning": agent_scores[i]["Speaker 2 - Initial Evaluation"]["reasoning"],
            }
        elif speaker_order[i] == 1:
            data = {
                "ID": agent_scores[i]["id"],
                "Score": agent_scores[i]["Speaker 1 - Initial Evaluation"]["score"],
                "Reasoning": agent_scores[i]["Speaker 1 - Initial Evaluation"]["reasoning"],
            }
            
        elif speaker_order[i] == 2:
            data = {
                "ID": agent_scores[i]["id"],
                "Score": agent_scores[i]["Speaker 3 - Initial Evaluation"]["score"],
                "Reasoning": agent_scores[i]["Speaker 3 - Initial Evaluation"]["reasoning"],
            }
        extracted_data.append(data)
    
    with open(config["evaluation"]["speaker2_score_path"], "w") as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=4)


def speaker3_score(speaker_order):
    with open(config["evaluation"]["results_path"], "r") as r:
        agent_scores = json.load(r)

    extracted_data = []
    for i in range(len(speaker_order)):
        if speaker_order[i] == 0:
            data = {
                "ID": agent_scores[i]["id"],
                "Score": agent_scores[i]["Speaker 3 - Initial Evaluation"]["score"],
                "Reasoning": agent_scores[i]["Speaker 3 - Initial Evaluation"]["reasoning"],
            }
        elif speaker_order[i] == 1:
            data = {
                "ID": agent_scores[i]["id"],
                "Score": agent_scores[i]["Speaker 2 - Initial Evaluation"]["score"],
                "Reasoning": agent_scores[i]["Speaker 2 - Initial Evaluation"]["reasoning"],
            }
            
        elif speaker_order[i] == 2:
            data = {
                "ID": agent_scores[i]["id"],
                "Score": agent_scores[i]["Speaker 1 - Initial Evaluation"]["score"],
                "Reasoning": agent_scores[i]["Speaker 1 - Initial Evaluation"]["reasoning"],
            }
        extracted_data.append(data)
    
    with open(config["evaluation"]["speaker3_score_path"], "w") as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    if config["discussion"]["num_round"] == 0:
        output, submission_order, speaker_order = generate_init_evaluation()
        speaker1_score(speaker_order)
        speaker2_score(speaker_order)
        speaker3_score(speaker_order)
    elif config["discussion"]["num_round"] > 0:
        output, submission_order, speaker_order = generate_init_evaluation()
        generate_discussion(output, submission_order, speaker_order)
        #print(submission_order)
        #print(speaker_order)
        speaker1_score(speaker_order)
        speaker2_score(speaker_order)
        speaker3_score(speaker_order)

    else:
        logging.warning("Invalid number of discussion rounds!")
