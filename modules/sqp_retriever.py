import os
import json

from dotenv import load_dotenv

from models.openai import client, MODEL
from prompts.rq_to_filter_criteria import (
    RQ_TO_FILTER_CRITERIA_SYSTEM_PROMPT,
    RQ_TO_FILTER_CRITERIA_USER_PROMPT,
)

from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

QUESTIONS_BANK_FILE = "data/sqp_reduced.csv"
VECTOR_STORE_FILE = "data/faiss_index"  # FAISS creates a directory with this name


load_dotenv()


# Load FAISS index from disk if available
def load_faiss_index(index_file):
    if os.path.exists(index_file):
        embeddings = OpenAIEmbeddings()
        return FAISS.load_local(
            index_file, embeddings, allow_dangerous_deserialization=True
        )
    return None


def generate_function_parameters(research_question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": RQ_TO_FILTER_CRITERIA_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": RQ_TO_FILTER_CRITERIA_USER_PROMPT.format(research_question),
            },
        ],
    )

    out = response.choices[0].message.content

    assert json.loads(out), "The output is not in JSON format."

    out = json.loads(out)

    return out


def filter_questions(research_question):
    params = generate_function_parameters(research_question)
    print("RAG params:", params)

    # loading the dataset here for now
    import pandas as pd

    df = pd.read_csv("data/sqp_reduced.csv")

    # filtering the dataset based on the parameters
    filtered_df = df[
        (df["Language"] == params["language"]) & (df["Domain"] == params["domain"])
    ]

    questions = filtered_df["Question"].tolist()

    return questions


def get_ranked_questions(research_question, num_questions=10):
    questions = filter_questions(research_question)

    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(questions, embeddings)

    # # Load FAISS index if it exists
    # vector_store = load_faiss_index(VECTOR_STORE_FILE)

    # if vector_store is None:
    #     embeddings = OpenAIEmbeddings()
    #     vector_store = FAISS.from_texts(questions, embeddings)

    #     vector_store.save_local(VECTOR_STORE_FILE)

    # Get the relevant questions
    filtered_questions = vector_store.similarity_search(
        research_question, k=num_questions
    )

    # Get the text only
    filtered_questions = [q.page_content for q in filtered_questions]

    return filtered_questions
