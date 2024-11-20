import os
import json
import string
import logging

from models.openai import client, MODEL

from parsers.persona import parse_persona_text
from modules.follow_up import get_follow_up_question
from prompts.pretest import PERSONA_SYSTEM_PROMPT
from questionnaire import QUESTIONNAIRE

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

latest_experiment_dir = "./pretest_gesis/pretest_selected_questions/experiments"

INTERVIEW_TRANSCRIPTS_DIR = latest_experiment_dir + "/" + "interview_transcripts/"
os.makedirs(INTERVIEW_TRANSCRIPTS_DIR, exist_ok=True)

PERSONA_PROMPTS_DIR = latest_experiment_dir + "/" + "persona_prompts/"
os.makedirs(PERSONA_PROMPTS_DIR, exist_ok=True)


def prepare_transcript(transcript_json):

    if isinstance(transcript_json, str):
        transcript = json.loads(transcript_json)
    else:
        transcript = transcript_json

    transcript_text = ""
    for item in transcript:
        transcript_text += f"Question: {item['question']}\nOptions: {item.get('options', '')}\nType: {item['type']}"

        if "follow_up" in item:
            transcript_text += "\nQuestion Type: Follow Up\n"
        else:
            transcript_text += "\nQuestion Type: Main Question\n"

        transcript_text += f"Response: {item['response']}\n"

    return transcript_text


personas = parse_persona_text(latest_experiment_dir + "/survey_personas.txt")

persona_prompts = []

for i, persona in enumerate(personas, start=0):
    persona_prompt = PERSONA_SYSTEM_PROMPT
    for k, v in persona.items():
        persona_prompt += f"{k}: {v}\n"

    persona_prompt += """
    You will be asked a series of questions based on the survey questionnaire. 
    Please answer them strictly following the details above and the chat history so far below. 
    If the question has options strictly pick just the option. For open-ended questions, answer in maximum 2-3 sentences.
    If the question is in a language other than English, please answer in that respective language.
    """
    persona_prompt += "Please stick strictly to the details provided above and do not deviate from them."

    persona_prompts.append(persona_prompt)

    with open(f"{PERSONA_PROMPTS_DIR}/persona_{i+1}_prompt.txt", "w") as f:
        f.write(persona_prompt)

print("=" * 50)


for i, persona_prompt in enumerate(persona_prompts, start=0):
    print(f"Persona {i + 1}\n")
    interview_transcript = []

    for j, q in enumerate(QUESTIONNAIRE):
        PROMPT = ""

        PROMPT += f'{j}. {q["question"]}'

        if q["question_type"] == "matrix_style":
            PROMPT += "    Statements:"
            for c, s in zip(string.ascii_lowercase, q["statements"]):
                PROMPT += f"\n    ({c}) {s}" + "(" + ", ".join(q["options"]) + ")"
        else:
            PROMPT += "    Options:"
            for c, o in zip(string.ascii_lowercase, q["options"]):
                PROMPT += f"\n    {c}) {o}"

        print(f'Question: {j}. {q["question"]}')
        print(f'Options: {q["options"]}')

        logging.info(f"Using model: {MODEL}")

        # Add chat history to the persona prompt
        persona_prompt_with_chat_history = (
            persona_prompt
            + f"\n<chat_history>\n{prepare_transcript(interview_transcript)}</chat_history>"
        )

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": persona_prompt,
                },
                {"role": "user", "content": PROMPT},
            ],
            # response_format={"type": "json_object"},
            temperature=1.1,
        )

        response_text = response.choices[0].message.content

        print(f"Response: {response_text}")

        interview_transcript.append(
            {
                "question": q["question"],
                "type": q["question_type"],
                "options": q["options"],
                "response": response_text,
            }
        )

        print("=" * 50)

        follow_up_question = get_follow_up_question(
            chat_history=prepare_transcript(interview_transcript)
        )

        if follow_up_question != "n/a":
            print(f"Follow-up Question: {follow_up_question}")

            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": persona_prompt,
                    },
                    {"role": "user", "content": follow_up_question},
                ],
                # response_format={"type": "json_object"},
                temperature=1.1,
            )

            response_text = response.choices[0].message.content

            print(f"Response: {response_text}")

            interview_transcript.append(
                {
                    "question": follow_up_question,
                    "response": response_text,
                    "type": "open-ended",
                    "follow_up": True,
                }
            )

            print("=" * 50)

    open(
        INTERVIEW_TRANSCRIPTS_DIR + f"interview_transcript_persona_{i+1}.txt", "w"
    ).write(json.dumps(interview_transcript, indent=4))

    print("=" * 50)
