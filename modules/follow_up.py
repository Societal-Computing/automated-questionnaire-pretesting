from models.openai import client, MODEL

FOLLOW_UP_SYSTEM_PROMPT = """
You will be given a chat history with a participant and you generate a probing question to probe the participant.
The probing question should focus on how the participant interpreted the question and how they came to the answer.

Some examples of the cognitive probing questions are:
- What does the term <term> mean to you?
- How did you come up with your answer?
- Can you repeat the question I just asked you in your own words?
- How sure are you that <answer>?
- How do you remember that you have <answer>?
- Why do you say that you think it is <answer>?
- Was that easy or hard to answer?
- I see you have <answer>. Can you tell me more about that?
- What do you think the purpose of this question is?
- I noticed that you hesitated before answering. Tell me what you were thinking.
- Tell me more about that.

Use above template along with the chat history to generate specific probing questions.
Detect the appropriate language to use based on the context of the chat history. Otherwise, use English.
The output should be just the question without any numbering or additional text. 
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
