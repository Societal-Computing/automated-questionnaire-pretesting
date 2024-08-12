from models.openai import client, MODEL

FOLLOW_UP_SYSTEM_PROMPT = """
You are a researcher who uses Cognitive Interviewing techniques in survey research.
You will be given a chat history with a participant who has answered a survey questionnaire.
Based on the last question and the response given by the participant, along with the chat history, you decide if a follow-up question is necessary. 
If it's necessary, you need to generate a follow-up question to probe the participant's response further. 
The output needs to be just the question without any numbering or additional text. 
If a follow-up question isn't necessary, you simply reply "n/a".
"""

FOLLOW_UP_PROMPT = """
Generate a follow-up question based on the following chat history:

<chat_history>
{}
</chat_history>
"""


def get_follow_up_question(chat_history):
    prompt = FOLLOW_UP_PROMPT.format(chat_history)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": FOLLOW_UP_SYSTEM_PROMPT,
            },
            {"role": "user", "content": prompt},
        ],
    )

    follow_up_question = response.choices[0].message.content

    return follow_up_question
