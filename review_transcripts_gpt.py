import os
import glob
import json

from parsers.persona import parse_persona_text
from models.openai import client, MODEL
from prompts.reviewer import REVIEWER_SYSTEM_PROMPT

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

# transcripts = glob.glob(f"{INTERVIEW_TRANSCRIPTS_DIR}/*.txt")
personas = parse_persona_text(latest_experiment_dir + "/survey_personas.txt")

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
            transcript_text += f"Question: {item['question']}\nResponse: {item['response']}\nOptions: {item.get('options', '')}\nType: {item['type']}\n"

            if "follow_up" in item:
                transcript_text += "\nQuestion Type: Follow Up\n"
            else:
                transcript_text += "\nQuestion Type: Main Question\n"

    prompt_content += f"<interview_{i+1}>\n{persona_text}\n\n{transcript_text}\n</interview_{i+1}>\n\n"

PROMPT = f"""
Analyze the following interview transcripts and look for potential issues in the survey questionnaire.

<research_question>
{research_question}
</research_question>


<interview_transcripts>
{prompt_content}
</interview_transcripts>
"""

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
