import os
import json
import string
import logging

from models.openai import client, MODEL

from parsers.persona import parse_persona_text
from modules.follow_up import get_follow_up_question
from prompts.pretest import PERSONA_SYSTEM_PROMPT
from questionnaire import get_questionnaire

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

latest_experiment_dir = "./wvs_political_trust/experiments"


# replacement variables (let's say we are pretesting in the EU)
replacement_map = {
    "<name of the national parliament or national congress>": "parliament",
    "<parliament>": "parliament",
    "<head of state>": "President",
}

INTERVIEW_TRANSCRIPTS_DIR = latest_experiment_dir + "/" + "interview_transcripts/"
os.makedirs(INTERVIEW_TRANSCRIPTS_DIR, exist_ok=True)

PERSONA_PROMPTS_DIR = latest_experiment_dir + "/" + "persona_prompts/"
os.makedirs(PERSONA_PROMPTS_DIR, exist_ok=True)

QUESTIONNAIRE = get_questionnaire()


def prepare_transcript(transcript_json):
    if isinstance(transcript_json, str):
        transcript = json.loads(transcript_json)
    else:
        transcript = transcript_json

    transcript_text = ""
    for item in transcript:
        transcript_text += f"Question: {item['q_number']}. {item['question']}\nStatement: {item['statement']}\nOptions: {item.get('options', '')}\nScale description: {item['scale_description']}\nType: {item['type']}"

        if "follow_up" in item:
            transcript_text += "\nQuestion Type: Follow Up\n"
        else:
            transcript_text += "\nQuestion Type: Main Question\n"

        transcript_text += f"Response: {item['response']}\n"

    return transcript_text


personas = parse_persona_text(latest_experiment_dir + "/survey_personas.txt")

persona_prompts = []

for i, persona in enumerate(personas, start=1):
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

    with open(f"{PERSONA_PROMPTS_DIR}/persona_{i}_prompt.txt", "w") as f:
        f.write(persona_prompt)

print("=" * 50)


for i, persona_prompt in enumerate(persona_prompts, start=1):
    print(f"Persona {i}\n")
    interview_transcript = []
    for q_no, question in enumerate(QUESTIONNAIRE, start=1):
        PROMPT = ""

        for k, v in replacement_map.items():
            question["question"] = question["question"].replace(k, v)

        question["statement"] = question["statement"].replace(
            "<parliament>", replacement_map["<parliament>"]
        )

        PROMPT += f'{q_no}. {question["question"]}'

        PROMPT += f"\n    Options: {', '.join(question['options'])}"

        PROMPT += f"\n    Scale Description: {question['scale_description']}"

        print(f'Question: {q_no}. {question["question"]}')
        print(f'Statement: {question["statement"]}')
        print(f'Options: {question["options"]}')

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
            temperature=1.1,
        )

        response_text = response.choices[0].message.content

        print(f"Response: {response_text}")

        interview_transcript.append(
            {
                "question": question["question"],
                "type": question["question_type"],
                "options": question["options"],
                "response": response_text,
                "q_number": q_no,
                "scale_description": question["scale_description"],
                "statement": question["statement"],
            }
        )

        print("=" * 50)

        follow_up_question = get_follow_up_question(
            chat_history=prepare_transcript(interview_transcript)
        )

        if follow_up_question != "n/a":
            print(f"Follow-up Question: {follow_up_question}")

            follow_up_question = f"""
                <chat_history>
                {prepare_transcript(interview_transcript)}
                </chat_history>

                {follow_up_question}
"""

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
                    "q_number": f"{q_no}.follow_up",
                    "scale_description": "n/a",
                    "statement": [],
                }
            )

            print("=" * 50)

    open(
        INTERVIEW_TRANSCRIPTS_DIR + f"interview_transcript_persona_{i}.txt", "w"
    ).write(json.dumps(interview_transcript, indent=4))

    print("=" * 50)
