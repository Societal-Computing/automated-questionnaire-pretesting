import os
import json
import glob
import string
import logging

from models.openai import client, MODEL

from parsers.persona import parse_persona_text
from prompts.pretest import PERSONA_SYSTEM_PROMPT
from questionnaire import (
    get_questionnaire,
    NEXT_QUESTION_SELECTOR_SYSTEM_PROMPT,
    NEXT_QUESTION_SELECTOR_PROMPT,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

latest_experiment_dir = "./pretest_gesis/experiments"

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
        transcript_text += f"Question: {item['q_number']}. {item['question']}\nOptions: {item.get('options', '')}\nType: {item['type']}"

        if "follow_up" in item:
            transcript_text += "\nQuestion Type: Follow Up\n"
        else:
            transcript_text += "\nQuestion Type: Main Question\n"

        transcript_text += f"Response: {item['response']}\n"

        transcript_text += f"Next question: {item['conditions']}\n"

    return transcript_text


def get_next_question(chat_history=None):
    questionnaire_text = get_questionnaire()
    questionnaire = get_questionnaire(convert_to_text=False)

    if chat_history:
        # Determines the next question to ask based on the chat history
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": NEXT_QUESTION_SELECTOR_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": NEXT_QUESTION_SELECTOR_PROMPT.format(
                        prepare_transcript(chat_history)
                    ),
                },
            ],
            temperature=1.0,
        )

        next_question_number = response.choices[0].message.content
    else:
        # if no chat history, start from the beginning
        next_question_number = "C1"

    if next_question_number.endswith("."):
        next_question_number = next_question_number[:-1]

    if next_question_number == "End of questionnaire":
        return None

    for question in questionnaire:
        if question["q_number"] == next_question_number:
            return question
    return None


# this is the questionnaire in text form
questionnnaire_text = get_questionnaire()
questionnaire = get_questionnaire(convert_to_text=False)

personas = []

for f in glob.glob(latest_experiment_dir + "/survey_personas/*.txt"):
    personas.extend(parse_persona_text(f))

persona_prompts = []

for i, persona in enumerate(personas, start=0):
    persona_prompt = PERSONA_SYSTEM_PROMPT
    for k, v in persona.items():
        persona_prompt += f"{k}: {v}\n"

    persona_prompt += """
    You will be asked a series of questions based on the survey questionnaire. 
    Please answer them strictly following the details above and the chat history so far below. 
    If the question has options strictly pick an option from the provided options.
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

    next_question = get_next_question(chat_history=None)

    while next_question:
        next_question["question"] = next_question["question"].replace(
            "tick", "select"
        )  # maybe asking to select is better

        PROMPT = ""

        PROMPT += f'{next_question["q_number"]}. {next_question["question"]}'

        if next_question["question_type"] == "matrix_style":
            PROMPT += "    Statements:"
            for c, s in zip(string.ascii_lowercase, next_question["statements"]):
                PROMPT += (
                    f"\n    ({c}) {s}" + "(" + ", ".join(next_question["options"]) + ")"
                )
        elif (
            next_question["question_type"] == "single_choice"
            or next_question["question_type"] == "multiple_choice"
        ):
            PROMPT += "\n    Options:"
            for c, o in zip(string.ascii_lowercase, next_question["options"]):
                PROMPT += f"\n    {c}) {o}"
        else:
            PROMPT += "\n    This is an open-ended question. Respond accordingly."

        print(f'Question: {next_question["q_number"]}. {next_question["question"]}')
        print(f'Options: {next_question["options"]}')

        logging.info(f"Using model: {MODEL}")

        # Add chat history to the persona prompt
        prompt_with_chat_history = (
            f"\n<chat_history>\n{prepare_transcript(interview_transcript)}</chat_history>\n"
            + f"<question>\n{PROMPT}</question>"
        )

        prompt_with_chat_history += "\n" + "Select the exact option from above options."

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": persona_prompt,
                },
                {"role": "user", "content": prompt_with_chat_history},
            ],
            temperature=1.1,
        )

        response_text = response.choices[0].message.content

        print(f"Response: {response_text}")

        interview_transcript.append(
            {
                "question": next_question["question"],
                "type": next_question["question_type"],
                "options": next_question["options"],
                "response": response_text,
                "conditions": next_question["conditions"],
                "q_number": next_question["q_number"],
            }
        )

        print("=" * 50)

        # Get the next question
        next_question = get_next_question(chat_history=interview_transcript)

    open(
        INTERVIEW_TRANSCRIPTS_DIR + f"interview_transcript_persona_{i+1}.txt", "w"
    ).write(json.dumps(interview_transcript, indent=4))

    print("=" * 50)
