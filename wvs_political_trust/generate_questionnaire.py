import os
import logging
from datetime import datetime

from models.openai import client, MODEL
from modules.relevant_articles import get_summarized_relevant_articles
from modules.sqp_retriever import get_ranked_questions
from prompts.questionnaire import (
    QUESTIONNNAIRE_GENERATOR_SYSTEM_PROMPT,
)
from wvs_political_trust.prompt import QUESTIONNAIRE_GENERATION_PROMPT

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

questionnaire = None

research_question = QUESTIONNAIRE_GENERATION_PROMPT

# Create a time-based directory for the experiment
experiment_dir = f"./wvs_political_trust/experiments"
os.makedirs(experiment_dir, exist_ok=True)

# Get relevant news articles
articles_summary = get_summarized_relevant_articles(
    "political trust survey results", experiment_dir
)

QUESTIONNAIRE_GENERATION_PROMPT += "<relevant_articles>\n"
QUESTIONNAIRE_GENERATION_PROMPT += articles_summary
QUESTIONNAIRE_GENERATION_PROMPT += "</relevant_articles>\n"

# save news summary
with open(f"{experiment_dir}/exa_articles_summary.txt", "w") as f:
    f.write(articles_summary)

relevant_questions = get_ranked_questions(research_question, num_questions=10)

QUESTIONNAIRE_GENERATION_PROMPT += "<relevant_questions>\n"
for q in relevant_questions:
    QUESTIONNAIRE_GENERATION_PROMPT += f"* {q}\n"
QUESTIONNAIRE_GENERATION_PROMPT += "</relevant_questions>\n"

# save survey generation prompt
with open(f"{experiment_dir}/survey_generation_prompt.txt", "w") as f:
    f.write(QUESTIONNAIRE_GENERATION_PROMPT)

# save research question
with open(f"{experiment_dir}/research_question.txt", "w") as f:
    f.write(research_question)

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": QUESTIONNNAIRE_GENERATOR_SYSTEM_PROMPT,
        },
        {"role": "user", "content": QUESTIONNAIRE_GENERATION_PROMPT},
    ],
    # response_format={"type": "json_object"},
    temperature=1.1,
)

questionnaire = response.choices[0].message.content

if questionnaire:
    # Save the survey questionnaire to a file
    logger.info("Saving the survey questionnaire...")

    with open(f"{experiment_dir}/survey_questionnaire.txt", "w") as f:
        f.write(questionnaire)
