# ScaleEval: Scalable Meta-Evaluation of LLMs as Evaluators via Agent Debate
This repository contains the source code and link to our [paper](https://arxiv.org/pdf/2401.16788.pdf).

ScaleEval is an agent-debate-assisted meta-evaluation framework that leverages the capabilities of multiple communicative LLM agents. This framework supports multi-round discussions to assist humans in discerning the most capable LLM-based evaluators. Users can supply their LLM submissions, criteria, and scenarios with our framework to conduct meta-evaluation.

<p align="center">
    <img src="figs/scale_framework.png" width="600" height="400" alt="ScaleEval Framework">
</p>


## Get Started

```shell
pip install scaleeval
export OPENAI_API_KEY=XXXX.YYYY.ZZZ
export ANTHROPIC_API_KEY=XXXX.YYYY.ZZZ
```
python 3.9+ is required.

## For Developers

### Install as developer

```bash
git clone git@github.com:GAIR-NLP/scaleeval.git
cd scaleeval
pip install -e .

# install pre-commit hooks
pip install pre-commit
pre-commit install
```

### Run formating
```shell
# this is necessary before you commit
git init
git add .
pre-commit run
```

## Run Meta-Evaluation

```bash
cd scaleeval
python evaluation.py
```

### Sample Criteria 
* `criteria/metaeval_creativity`: Scoring of 1 to 5 for each LLM submission based on the creativity criteria, and decide which submission is better.
* `criteria/metaeval_helpfulness`: Scoring of 1 to 5 for each LLM submission based on the helpfulness criteria, and decide which submission is better.
* `criteria/metaeval_interpretability`: Scoring of 1 to 5 for each LLM submission based on the interpretability, and decide which submission is better.
* `criteria/metaeval_reasoning`: Scoring of 1 to 5 for each LLM submission based on the reasoning criteria, and decide which submission is better.

### Sample LLM Question Prompts and Submissions
* `scaleeval/responses/gpt3.5/brainstorming.jsonl`: Responses generated from gpt3.5-turbo based on the prompts in the brainstorming scenario.
* `scaleeval/responses/claude-instant/brainstorming.jsonl`: Responses generated from claude-instant based on the prompts in the brainstorming scenario.

### Supply your own criteria and scenario!
```bash
cd criteria
```

Add your own criteria descriptions to a new .yaml file! Follow the format below:
```python
criteria:
    [your defined criteria]:
        "1": ...
        "2": ...
        "3": ...
        "4": ...
        "5": ...
```

### Supply your own LLM submissions!
Collect your LLM submissions and save them in a .jsonl file with the following format:
```python
{"prompt": ..., "category": ..., "response": ...}
```

Here is one example:
```python
{"prompt": "Can you tell me how to make chocolate chip cookies?", "category": "brainstorming", "response": "Certainly! Here's a simple recipe for making chocolate chip cookies:\n\nIngredients:\n- 1 cup (2 sticks) unsalted butter, softened\n- 1 cup granulated sugar\n- 1 cup packed brown sugar\n- 2 large eggs\n- 1 teaspoon vanilla extract\n- 3 cups all-purpose flour\n- 1 teaspoon baking soda\n- 1/2 teaspoon salt\n- 2 cups chocolate chips\n\nInstructions:\n1. Preheat your oven to 350\u00b0F (175\u00b0C) and line a baking sheet with parchment paper.\n2. In a large mixing bowl, cream together the softened butter, granulated sugar, and brown sugar until well combined and creamy.\n3. Add the eggs one at a time, beating well after each addition. Then, stir in the vanilla extract.\n4. In a separate bowl, whisk together the flour, baking soda, and salt. Gradually add this dry mixture to the wet ingredients, mixing until just combined.\n5. Fold in the chocolate chips until evenly distributed throughout the dough.\n6. Using a cookie scoop or tablespoon, drop rounded portions of dough onto the prepared baking sheet, spacing them about 2 inches apart.\n7. Bake in the preheated oven for 10-12 minutes, or until the edges are golden brown. The centers may still appear slightly soft, but they will firm up as they cool.\n8. Remove the baking sheet from the oven and let the cookies cool on the sheet for a few minutes before transferring them to a wire rack to cool completely.\n9. Repeat the process with the remaining dough until all the cookies are baked.\n\nEnjoy your homemade chocolate chip cookies!"}
```

## Citation
Please consider citing our [paper](https://arxiv.org/pdf/2401.16788.pdf) if you find our repo and results useful!
```
@article{chern2024scaleeval,
  title={Can Large Language Models be Trusted for Evaluation? Scalable Meta-Evaluation of LLMs as Evaluators via Agent Debate},
  author={Chern, Steffi and Chern, Ethan and Neubig, Graham and Liu, Pengfei},
  journal={arXiv preprint arXiv:2401.16788},
  year={2024}
}
```


