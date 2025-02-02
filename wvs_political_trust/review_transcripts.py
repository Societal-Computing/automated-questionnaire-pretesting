import os
import json

from parsers.persona import parse_persona_text
from models.openai import client, MODEL
from prompts.reviewer import REVIEWER_SYSTEM_PROMPT
from wvs_political_trust.questionnaire import get_questionnaire

MODEL = "gpt-4o"

latest_experiment_dir = "./wvs_political_trust/experiments"

INTERVIEW_TRANSCRIPTS_DIR = latest_experiment_dir + "/" + "interview_transcripts/"

REVIEWER_SYSTEM_PROMPT = """
As a reviewer, you have been provided with the transcripts of a survey pilot study interviews, along with the original research question. 
Your task is to evaluate the survey questionnaire based on several criteria, including clarity, comprehension, and sensitivity. 
Select a statement from the interview transcript where the participant encountered difficulties or misunderstandings.
Check for any contradictions or inconsistencies in the participant's responses. 

Some of the possible issues that you need to look for are:
double statements
ambiguous statements
ambiguous word meanings
loaded or leading statements or phrase
level of statement difficulty
lopsided response categories
missing response categories
missing statements
necessity and relevance of individual statements
discriminating statements (between certain groups within the target group)
non-response rates
effect of ordinal position of multiple responses
perceptions of pictures
degree of attention


Provide a detailed review of the survey questionnaire, highlighting any areas that need improvement or revision as shown in following example. 
Then, suggest the corrected statements as well. The suggestions should only be a statement and not a question.
Consider only the main statements when suggesting improvements and ignore follow up questions when suggesting corrections. 
Think carefully about the participant's responses to the statements and how they could be improved.
When describing issues, mention the Statement as well as the participant number (e.g. Persona 1) and what problem you found with it.

Example output:

Statement: Statement from the survey questionnaire.
Problem: Describe the problem with the statement. Relate it to the above points.
Sources: Mention the participant number and the transcript where the issue was observed.
Suggestion: Suggest a corrected version of the statement.

Statement: Statement from the survey questionnaire.
Problem: Describe the problem with the statement. Relate it to the above points.
Sources: Mention the participant number and the transcript where the issue was observed.
Suggestion: Suggest a corrected version of the statement.

"""

# Get the list of personas for the prompt
personas = parse_persona_text(latest_experiment_dir + "/survey_personas.txt")

# Review survey questionnaire in parts due to context length limit
start = 1
end = 21
review_no = 1

while start < len(personas):
    print("Start: ", start, "End: ", end)

    prompt_content = ""

    for i in range(start - 1, end - 1):
        # prepare the persona
        persona_text = f"Participant {i+1}:\n"
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
                transcript_text += f"Question: {item['q_number']}. {item['question']}\nStatement: {item['statement']}\nOptions: {item.get('options', '')}\nType: {item['type']}"

                if "follow_up" in item:
                    transcript_text += "\nQuestion Type: Follow Up\n"
                else:
                    transcript_text += "\nQuestion Type: Main Question\n"

                transcript_text += f"Response: {item['response']}\n\n"

        prompt_content += f"<interview_{i+1}>\n{persona_text}\n\n{transcript_text}\n</interview_{i+1}>\n\n"

    questions_text = get_questionnaire(convert_to_text=True)
    PROMPT = f"""
    You are a survey researcher. Analyze the following interview transcripts from a Pilot study and look for potential issues in the survey questionnaire. Ignore the follow-up questions and focus on the main questions.
    For each problem that you find, the output should have the following topics: question, problem, sources, suggestion.

    <questionnaire>
    {questions_text}
    </questionnaire>

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
        temperature=1.0,
    )

    review_text = response.choices[0].message.content
    print("REVIEW:", review_text)

    with open(
        latest_experiment_dir + f"/reviews/survey_questionnaire_review_{review_no}.txt",
        "w",
    ) as f:
        f.write(review_text)

    review_no += 1

    start = end
    end += 20
    end = min(end, len(personas) + 1)
