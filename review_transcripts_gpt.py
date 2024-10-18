import os
import json

from parsers.persona import parse_persona_text
from parsers.questionnaire import parse_questionnaire_text
from models.openai import client, MODEL
from prompts.reviewer import REVIEWER_SYSTEM_PROMPT

MODEL = "gpt-4-turbo"

EXPERIMENTS_DIR = "./experiments/"

# Get the latest experiment directory
experiment_dirs = sorted(
    [
        EXPERIMENTS_DIR + d
        for d in os.listdir(EXPERIMENTS_DIR)
        if os.path.isdir(os.path.join(EXPERIMENTS_DIR, d))
    ],
    reverse=True,
)
latest_experiment_dir = experiment_dirs[0]
print("Experiment DIR: ", latest_experiment_dir)

INTERVIEW_TRANSCRIPTS_DIR = latest_experiment_dir + "/" + "interview_transcripts/"

# Get the list of personas for the prompt
personas = parse_persona_text(latest_experiment_dir + "/survey_personas.txt")

# prepare questionnaire for the prompt
questions = parse_questionnaire_text(
    latest_experiment_dir + "/survey_questionnaire.txt"
)
questions_text = ""
for question in questions:
    questions_text += f"Question: {question['question']}\nType: {question['type']}\nOptions: {question.get('options', '')}\n\n"

# Get research question for the prompt
research_question = open(latest_experiment_dir + "/research_question.txt").read()

prompt_content = ""


for i, (persona) in enumerate(personas):
    # prepare the persona
    persona_text = f"Participant {i+1}:\n"
    for key, value in persona.items():
        persona_text += f"{key}: {value}\n"

    # prepare the transcript
    transcript_file = (
        f"{INTERVIEW_TRANSCRIPTS_DIR}/interview_transcript_persona_{i+1}.txt"
    )
    with open(transcript_file) as f:
        transcript_json = json.load(f)
        transcript_text = ""
        for item in transcript_json:
            transcript_text += f"Question: {item['question']}\nResponse: {item['response']}\nType: {item['type']}\n"

            if "follow_up" in item:
                transcript_text += "Question Type: Follow Up\n\n"
            else:
                transcript_text += "Question Type: Main Question\n\n"

    prompt_content += f"<interview_{i+1}>\n{persona_text}\n\n{transcript_text}\n</interview_{i+1}>\n\n"

PROMPT = f"""
Analyze the following interview transcripts and look for potential issues in the survey questionnaire.

<research_question>
{research_question}
</research_question>

<questionnaire>
{questions_text}
</questionnaire>

<interview_transcripts>
{prompt_content}
</interview_transcripts>
"""

# with open("prompt.txt", "w") as f:
#     f.write(PROMPT)

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": REVIEWER_SYSTEM_PROMPT,
        },
        {"role": "user", "content": PROMPT},
    ],
    # response_format={"type": "json_object"},
    temperature=1.0,
)

review_text = response.choices[0].message.content

with open(latest_experiment_dir + "/survey_questionnaire_review.txt", "w") as f:
    f.write(review_text)
