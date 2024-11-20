import os
import json

from parsers.persona import parse_persona_text
from models.openai import client, MODEL
from prompts.reviewer import REVIEWER_SYSTEM_PROMPT


# Get the latest experiment directory

latest_experiment_dir = "./pretest_gesis/experiments"

INTERVIEW_TRANSCRIPTS_DIR = latest_experiment_dir + "/" + "interview_transcripts/"

# Get the list of personas for the prompt
personas = parse_persona_text(latest_experiment_dir + "/survey_personas.txt")

start = 1
end = (len(personas) + 1) // 2
review_no = 1

while start < len(personas):
    print("Start: ", start, "End: ", end)

    prompt_content = ""

    for i in range(start - 1, end - 1):
        # prepare the persona
        persona_text = f"Participant {i+1}:\n"
        # print("PERSONA: ", persona_text)
        for key, value in personas[i].items():
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

                if "statements" in item:
                    transcript_text += f"Statements: {item['statements']}\n"

                if "follow_up" in item:
                    transcript_text += "Question Type: Follow Up\n\n"
                else:
                    transcript_text += "Question Type: Main Question\n\n"

        prompt_content += f"<interview_{i+1}>\n{persona_text}\n\n{transcript_text}\n</interview_{i+1}>\n\n"

    PROMPT = f"""
    Analyze the following interview transcripts and look for potential issues in the survey questionnaire. Do not suggest changes for the follow-up questions.

    <interview_transcripts>
    {prompt_content}
    </interview_transcripts>
    """

    with open(
        latest_experiment_dir + f"/review_prompts/prompt_{review_no}.txt", "w"
    ) as f:
        f.write(PROMPT)

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

    with open(
        latest_experiment_dir + f"/reviews/survey_questionnaire_review_{review_no}.txt",
        "w",
    ) as f:
        f.write(review_text)

    review_no += 1

    start = end
    end += 50
    end = min(end, len(personas) + 1)
