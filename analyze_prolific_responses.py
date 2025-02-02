import pickle
from models.openai import client, MODEL

SYSTEM_PROMPT = """
You will be given a list of responses for the question 'Why did you prefer this question group?'. You then analyze the responses for thematic analysis.

You then list the top 5 themes with 10 responses in each theme. You will also provide a brief description of each theme.
"""

reasons = pickle.load(
    open("reasons_experts.pkl", "rb")
)
labels = pickle.load(
    open("labels_experts.pkl", "rb")
)

PROMPT = f"""
Do thematic analysis for the following responses:
"""

for reason in reasons:
    PROMPT += f"{reason}\n"

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {"role": "user", "content": PROMPT},
    ],
    # response_format={"type": "json_object"},
    temperature=1.0,
)

review_text = response.choices[0].message.content

with open("thematic_analysis_experts.txt", "w") as f:
    f.write(review_text)
