import os
import json
import logging

# import streamlit as st
from models.openai import client, MODEL

from parsers.questionnaire import parse_questionnaire_text
from parsers.persona import parse_persona_text
from modules.follow_up import get_follow_up_question
from prompts.pretest import PERSONA_SYSTEM_PROMPT

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
        transcript_text += (
            f"Question: {item['question']}\nResponse: {item['response']}\n"
        )

        if "follow_up" in item:
            transcript_text += f"\nis_followup: {item['follow_up']}\n"
            
    return transcript_text


questions = parse_questionnaire_text(
    latest_experiment_dir + "/survey_questionnaire.txt"
)
personas = parse_persona_text(latest_experiment_dir + "/survey_personas.txt")

persona_prompts = []

for i, persona in enumerate(personas):
    persona_prompt = PERSONA_SYSTEM_PROMPT
    for k, v in persona.items():
        persona_prompt += f"{k}: {v}\n"

    persona_prompt += """
    You will be asked a series of questions based on the survey questionnaire. 
    Please answer them strictly following the details above and the chat history so far below. 
    If the question has options strictly pick just the option. For open-ended questions, answer in maximum 2-3 sentences.
    """
    # persona_prompt += "You are free to extrapolate any details relevant to the question for the given persona if the details are not provided."
    persona_prompt += "Please stick strictly to the details provided above and do not deviate from them."

    persona_prompts.append(persona_prompt)

    with open(f"{PERSONA_PROMPTS_DIR}/persona_{i+1}_prompt.txt", "w") as f:
        f.write(persona_prompt)

print("=" * 50)


for i, persona_prompt in enumerate(persona_prompts):
    print(f"Persona {i + 1}\n")
    interview_transcript = []
    persona_prompt_with_chat_history = persona_prompt

    for question in questions:
        if question["type"] == "closed-ended":
            q = question["question"]
            options = question["options"]
        elif question["type"] == "multiple-choice":
            q = question["question"] + " (You can select multiple options.)"
            options = question["options"]
        else:
            q = question["question"]
            options = None

        print(f"Question: {q}")
        print(f"Options: {options}" if options else "")

        logging.info(f"Using model: {MODEL}")

        PROMPT = f"""
        Question: {q}
        """

        if options:
            PROMPT += f"Options: {', '.join(options)}"

        # Add chat history to the persona prompt
        persona_prompt_with_chat_history += f"\n<chat_history>\n{prepare_transcript(interview_transcript)}</chat_history>"

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

        # response_text = response["message"]["content"]

        print(f"Response: {response_text}")

        interview_transcript.append(
            {"question": question["question"], "response": response_text}
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
                {"question": follow_up_question, "response": response_text, "follow_up": True}
            )

            print("=" * 50)

    open(
        INTERVIEW_TRANSCRIPTS_DIR + f"interview_transcript_persona_{i+1}.txt", "w"
    ).write(json.dumps(interview_transcript, indent=4))

    print("=" * 50)

# transcript = prepare_transcript(interview_transcript)

# response = ollama.chat(
#     model=MODEL,
#     messages=[
#         {"role": "system", "content": REVIEWER_SYSTEM_PROMPT},
#         {"role": "user", "content": transcript},
#     ],
# )
# review = response["message"]["content"]

# print("Review:", review)


# open("review.txt", "w").write(review)
