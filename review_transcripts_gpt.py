import os
import glob
import json

from parsers.persona import parse_persona_text
from models.openai import client, MODEL

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

INTERVIEW_TRANSCRIPTS_DIR = latest_experiment_dir + "/" + "interview_transcripts/"

REVIEWER_SYSTEM_PROMPT = """
As a reviewer, you have been provided with the transcripts of a survey pilot study interviews, along with the original research question. 
Your task is to evaluate the survey questionnaire based on several criteria, including clarity, comprehension, and sensitivity. 
Select a question from the interview transcript where the participant encountered difficulties or misunderstandings.
Check for any contradictions or inconsistencies in the participant's responses. 

Some of the possible issues that you need to look for are:
double questions
ambiguous questions
ambiguous word meanings
loaded or leading questions or phrase
level of question difficulty
lopsided response categories
missing response categories
missing questions
necessity and relevance of individual questions
discriminating questions (between certain groups within the target group)
non-response rates
effect of ordinal position of multiple responses
perceptions of pictures
degree of attention


Please provide a detailed review of the survey questionnaire, highlighting any areas that need improvement or revision. Then, suggest the corrected questions as well.
Consider only the main questions when suggesting improvements. For follow-up questions, you can analyze just the responses of the participants and you don't need to suggest improvement for those.
Think carefully about the participant's responses and the overall flow of the interview.
"""

transcripts = glob.glob(f"{INTERVIEW_TRANSCRIPTS_DIR}/*.txt")
personas = parse_persona_text(latest_experiment_dir + "/survey_personas.txt")

research_question = open(latest_experiment_dir + "/research_question.txt").read()

prompt_content = ""


for i, (persona, transcript) in enumerate(zip(personas, transcripts)):
    # prepare the persona
    persona_text = f"Participant {i+1}:\n"
    for key, value in persona.items():
        persona_text += f"{key}: {value}\n"

    # prepare the transcript
    with open(transcript) as f:
        transcript_json = json.load(f)
        transcript_text = ""
        for item in transcript_json:
            transcript_text += (
                f"Question: {item['question']}\nResponse: {item['response']}\n\n"
            )

            if "follow_up" in item:
                transcript_text += f"Is Follow-up: {item['follow_up']}\n"

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
    temperature=1.1,
)

review_text = response.choices[0].message.content

with open(latest_experiment_dir + "/survey_questionnaire_review.txt", "w") as f:
    f.write(review_text)
