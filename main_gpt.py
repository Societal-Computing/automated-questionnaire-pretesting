import os
import logging
from datetime import datetime

import streamlit as st


from models.openai import client, MODEL
from modules.relevant_articles import get_summarized_relevant_articles
from modules.sqp_retriever import get_ranked_questions
from parsers.questionnaire import parse_questionnaire_text
from evaluation.questionnaire import compute_similarity
from prompts.questionnaire import (
    QUESTIONNNAIRE_GENERATOR_SYSTEM_PROMPT,
    PERSONA_GENERATOR_SYSTEM_PROMPT,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

questionnaire = None


with st.form("gen_form"):
    research_question = st.text_area(
        "Write the research question below for which you want to generate a survey questionnaire. Try to make it as detailed as possible and include all the details you'd want the survey to include."
    )

    n_questions = st.number_input(
        "How many questions do you want to generate?",
        min_value=3,
        max_value=20,
        value=10,
    )

    SURVEY_GENERATION_PROMPT = f"""
    Generate a survey questionnaire with {n_questions} number of questions for the following research question:
     
    <question>{research_question}</question>

    """

    PERSONA_GENERATION_PROMPT = f"""
    Generate a list of persona based on the following information:
     
    <question>{research_question}</question>
    """

    submitted = st.form_submit_button("Submit")

    st.write("Generated questionnaire:")

    logger.info(f"Using model: {MODEL}")

    if submitted and research_question and MODEL:
        # Create a time-based directory for the experiment
        experiment_dir = f"experiments/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
        os.makedirs(experiment_dir, exist_ok=True)

        with st.spinner("Getting 5 recent relevant news articles..."):
            # Get relevant news articles
            articles_summary = get_summarized_relevant_articles(
                research_question, experiment_dir
            )

            SURVEY_GENERATION_PROMPT += "<relevant_articles>\n"
            SURVEY_GENERATION_PROMPT += articles_summary
            SURVEY_GENERATION_PROMPT += "</relevant_articles>\n"

            # save news summary
            with open(f"{experiment_dir}/exa_articles_summary.txt", "w") as f:
                f.write(articles_summary)

        with st.spinner("Getting 10 relevant questions from the SQP database..."):
            relevant_questions = get_ranked_questions(
                research_question, num_questions=10
            )

            SURVEY_GENERATION_PROMPT += "<relevant_questions>\n"
            for q in relevant_questions:
                SURVEY_GENERATION_PROMPT += f"* {q}\n"
            SURVEY_GENERATION_PROMPT += "</relevant_questions>\n"

        # save survey generation prompt
        with open(f"{experiment_dir}/survey_generation_prompt.txt", "w") as f:
            f.write(SURVEY_GENERATION_PROMPT)

        # save research question
        with open(f"{experiment_dir}/research_question.txt", "w") as f:
            f.write(research_question)

        with st.spinner("Generating survey questionnaire..."):
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": QUESTIONNNAIRE_GENERATOR_SYSTEM_PROMPT,
                    },
                    {"role": "user", "content": SURVEY_GENERATION_PROMPT},
                ],
                # response_format={"type": "json_object"},
                temperature=1.1,
            )

            questionnaire = response.choices[0].message.content

        st.write(questionnaire)

        st.divider()
    else:
        st.write(
            "Please enter a research question and select a model to generate a survey questionnaire."
        )

if questionnaire:
    # Save the survey questionnaire to a file
    logger.info("Saving the survey questionnaire...")

    with open(f"{experiment_dir}/survey_questionnaire.txt", "w") as f:
        f.write(questionnaire)

    with st.spinner("Generating personas..."):
        # Save persona prompt
        with open(f"{experiment_dir}/persona_generation_prompt.txt", "w") as f:
            f.write(PERSONA_GENERATION_PROMPT)

        # Get the output from Ollama API
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": PERSONA_GENERATOR_SYSTEM_PROMPT},
                {"role": "user", "content": PERSONA_GENERATION_PROMPT},
            ],
            # response_format={"type": "json_object"},
            temperature=1.1,
        )

        personas = response.choices[0].message.content

    st.write("Generated personas:")

    st.write(personas)

    # Save the survey questionnaire to a file
    logger.info("Saving the survey personas...")

    with open(f"{experiment_dir}/survey_personas.txt", "w") as f:
        f.write(personas)

    st.divider()

if questionnaire:
    parsed_questions = parse_questionnaire_text(
        f"{experiment_dir}/survey_questionnaire.txt"
    )

    st.write("Metrics:")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.write(
            "How relevant is the generated questionnaire, given the research question? (Rouge-L):"
        )
        rouge_l_score = compute_similarity(
            [q["question"] for q in parsed_questions],
            research_question,
            metric="rouge-l",
        )
        st.write(rouge_l_score)

    with col2:
        st.write(
            "How relevant is the generated questionnaire, given the research question? (Cosine):"
        )
        semantic_similarity = compute_similarity(
            [q["question"] for q in parsed_questions],
            research_question,
            metric="semantic",
        )
        st.write(semantic_similarity)

    with col3:
        st.write("How specific are the generated questions? (n-gram proportion)")
        repetition_proportion = compute_similarity(
            [q["question"] for q in parsed_questions],
            research_question,
            metric="repetition",
        )
        st.write(repetition_proportion)

    with col4:
        st.write(
            "How specific are the generated questions? (no. of similar questions, 95% cosine similarity):"
        )
        question_similarity = compute_similarity(
            [q["question"] for q in parsed_questions],
            research_question,
            metric="question-similarity",
        )
        st.write(question_similarity)
