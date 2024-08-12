import os
from datetime import datetime

from dotenv import load_dotenv
from exa_py import Exa

from models.openai import client, MODEL

load_dotenv()

exa = Exa(api_key=os.getenv("EXA_API_KEY"))

SUMMARIZER_SYSTEM_PROMPT = """
You will be provided excerpts from 5 news articles. Summarize each article in 1 sentences i.e. 5 sentences in total.
"""

PROMPT = """
Generate summary for the following articles:

{}
"""


# Get relevant news article excerpts and summarize them
def get_summarized_relevant_articles(research_question, experiment_dir):
    result = exa.search_and_contents(
        research_question,
        type="neural",
        num_results=5,
        text=True,
        category="news",
        start_published_date="2023-01-01T13:39:57.791Z",
        end_published_date=datetime.now().isoformat(),
    )

    with open(f"{experiment_dir}/exa_relevant_articles.txt", "w") as f:
        f.write(str(result))

    results = result.results

    articles = "<relevant_articles>\n"
    articles += "".join([f"<article>{r.text}</article>\n" for r in results])
    articles += "</relevant_articles>\n"

    prompt = PROMPT.format(articles)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SUMMARIZER_SYSTEM_PROMPT,
            },
            {"role": "user", "content": prompt},
        ],
    )

    summary = response.choices[0].message.content

    # save the summarized articles
    with open(f"{experiment_dir}/exa_relevant_articles.txt", "w") as f:
        f.write(str(result))

    return summary
