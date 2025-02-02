import os
import glob
from collections import defaultdict

import numpy as np
import pandas as pd
from tqdm import tqdm

from models.openai import client, MODEL
from modules.sqp_retriever import get_ranked_questions
from modules.relevant_articles import get_summarized_relevant_articles
from parsers.questionnaire import parse_questionnaire_text
from evaluation.questionnaire import compute_similarity

# prompts_dir = glob.glob("tests/prompts/*.txt")
prompts_dir = "questionnaire_generation_tests/prompts/"
output_dir = "questionnaire_generation_tests/out"

questionnaire = None


def read_prompt(prompt_file):
    if not prompt_file:
        return ""

    with open(prompt_file, "r") as f:
        return f.read()


# Configuration
# =================================================================

research_questions = [
    """
    How does telemedicine affect patient satisfaction and adherence to treatment among urban adults?
    Target Demographics: Adults aged 18-65 in urban areas who have used telemedicine services at least once in the past year.
    Topics in Survey:

        Frequency and purpose of telemedicine use
        Perceived accessibility and ease of use of telemedicine
        Levels of satisfaction with virtual consultations compared to in-person visits
        Adherence to prescribed treatments following telemedicine consultations
        Concerns or limitations faced when using telemedicine services

    """,
    """
    What factors influence the shift from in-store to online shopping among millennials and Gen Z consumers in North America?
    Target Demographics: Millennials (25-40) and Gen Z (18-24) in North America, who have made at least one online purchase in the past six months.
    Topics in Survey:

        Frequency of online vs. in-store shopping
        Primary motivations for choosing online over in-store shopping (convenience, price, variety, etc.)
        Importance of factors like user reviews, brand loyalty, and delivery speed in purchasing decisions
        Preferences for specific product categories (e.g., clothing, electronics, groceries)
        Likelihood of returning to in-store shopping post-COVID-19 pandemic
    """,
    """
    What impact has the rise of digital gaming had on social engagement and mental health among teenagers in urban areas?
    Target Demographics: Teenagers aged 13-18 living in urban settings who actively engage in digital gaming (at least 5 hours per week).
    Topics in Survey:

        Types and frequency of games played (single-player, multiplayer, mobile, console, etc.)
        Social interactions facilitated through gaming (with friends, strangers, online communities)
        Perceived benefits and drawbacks of gaming on social skills and relationships
        Impact of gaming on mental well-being (stress relief, potential addiction, feelings of isolation, etc.)
        Parent or guardian attitudes toward the respondent's gaming habits
    """,
    """
    How do EU citizens perceive the effectiveness of the EU's environmental policies in combating climate change?
    Target Demographics: European Union citizens aged 18 and above, especially those in countries highly affected by climate-related changes.
    Topics in Survey:

        Awareness of specific EU environmental policies (e.g., the European Green Deal)
        Perceived effectiveness of these policies on national and global levels
        Personal importance placed on climate change as a political issue
        Trust in the EU’s commitment to environmental goals versus individual member states
        Willingness to support future policy changes or regulations aimed at reducing carbon footprint
    """,
    """
    How do work-from-home arrangements impact the work-life balance and interpersonal relationships of parents?
    Target Demographics: Parents with children under 18 who have been working remotely for at least 6 months.
    Topics in Survey:

        Daily work-from-home routines and challenges
        Perceived effects on time spent with family versus time spent on work
        Impact on relationship quality with spouse/partner and children
        Coping strategies or practices to maintain work-life balance
        Desire to continue working from home, return to the office, or a hybrid model in the future
    """,
]

configs = [
    # Here, the prompt just contains the output format but no specific instructions
    {
        "prompt": prompts_dir + "base_system_prompt_just_the_output_format.txt",
        "news": False,
        "sqp": False,
    },
    {
        "prompt": prompts_dir + "base_system_prompt_just_the_output_format.txt",
        "news": True,
        "sqp": False,
    },
    {
        "prompt": prompts_dir + "base_system_prompt_just_the_output_format.txt",
        "news": False,
        "sqp": True,
    },
    {
        "prompt": prompts_dir + "base_system_prompt_just_the_output_format.txt",
        "news": True,
        "sqp": True,
    },
    # Here, the prompt includes specific instructions for generating a survey questionnaire
    {
        "prompt": prompts_dir + "base_system_prompt.txt",
        "news": False,
        "sqp": False,
    },
    {
        "prompt": prompts_dir + "base_system_prompt.txt",
        "news": True,
        "sqp": False,
    },
    {
        "prompt": prompts_dir + "base_system_prompt.txt",
        "news": False,
        "sqp": True,
    },
    {
        "prompt": prompts_dir + "base_system_prompt.txt",
        "news": True,
        "sqp": True,
    },
]

# random seed for reproducibility
# See: https://platform.openai.com/docs/advanced-usage/reproducible-outputs
# random_seeds = [42, 111, 7, 1111, 2025]
random_seeds = [
    53691737,
    191541319,
    258644394,
    118516851,
    204132357,
    1998791,
    83660131,
    65493133,
    33166798,
    112032729,
]

# temperature
temperatures = np.linspace(0.8, 1.2, 5)

# =================================================================

scores = defaultdict(list)
errors = []

for idx, research_question in enumerate(research_questions, start=1):
    print(f"Research Question: {research_question}")

    articles_summary = get_summarized_relevant_articles(research_question, output_dir)

    # Save the relevant articles to a file
    with open(f"{output_dir}/relevant_news/relevant_articles_RQ=RQ{idx}.txt", "w") as f:
        f.write(articles_summary)

    relevant_questions = get_ranked_questions(research_question, num_questions=10)

    # Save the relevant questions to a file
    with open(f"{output_dir}/relevant_questions/relevant_questions_RQ=RQ{idx}.txt", "w") as f:
        for q in relevant_questions:
            f.write(f"* {q}\n")

    print("=" * 50)

    for random_seed in random_seeds:
        for temperature in temperatures:
            for config in tqdm(configs):
                prompt_file = config["prompt"]
                prompt_name = (
                    prompt_file.split("/")[-1].split(".")[0] if prompt_file else ""
                )
                sqp_status = config["sqp"]
                news_status = config["news"]

                scores["research_question"].append(research_question)
                scores["prompt"].append(config["prompt"])
                scores["sqp"].append(config["sqp"])
                scores["news"].append(config["news"])

                print(
                    f"Testing: RQ=RQ{idx}, prompt={prompt_name}, news={news_status}, sqp={sqp_status}, seed={random_seed}, temperature={temperature}"
                )

                QUESTIONNNAIRE_GENERATOR_SYSTEM_PROMPT = read_prompt(config["prompt"])

                SURVEY_GENERATION_PROMPT = f"""
                Generate a survey questionnaire with 10 number of questions for the following information:
                    
                <question>{research_question}</question>

                """

                if news_status:
                    SURVEY_GENERATION_PROMPT += "<relevant_articles>\n"
                    SURVEY_GENERATION_PROMPT += articles_summary
                    SURVEY_GENERATION_PROMPT += "</relevant_articles>\n"

                if sqp_status:
                    SURVEY_GENERATION_PROMPT += "<relevant_questions>\n"
                    for q in relevant_questions:
                        SURVEY_GENERATION_PROMPT += f"* {q}\n"
                    SURVEY_GENERATION_PROMPT += "</relevant_questions>\n"

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
                    temperature=temperature,
                    seed=random_seed,
                )

                questionnaire = response.choices[0].message.content
                system_fingerprint = response.system_fingerprint

                survey_file_name = f"{output_dir}/generated_questionnaires/survey_questionnaire_rq=RQ{idx}_prompt={prompt_name}_sqp={sqp_status}_news={news_status}_seed={random_seed}_temperature={temperature}.txt"

                with open(survey_file_name, "w") as f:
                    f.write(questionnaire)

                try:
                    parsed_questions = parse_questionnaire_text(survey_file_name)

                    rouge_l_score = compute_similarity(
                        [q["question"] for q in parsed_questions],
                        research_question,
                        metric="rouge-l",
                    )
                    scores["rouge_l"].append(rouge_l_score)

                    semantic_similarity = compute_similarity(
                        [q["question"] for q in parsed_questions],
                        research_question,
                        metric="semantic",
                    )
                    scores["semantic_similarity"].append(semantic_similarity)

                    repetition_proportion = compute_similarity(
                        [q["question"] for q in parsed_questions],
                        research_question,
                        metric="repetition",
                        n=2,
                    )
                    scores["bigram_overlap"].append(repetition_proportion)

                    repetition_proportion_unigram = compute_similarity(
                        [q["question"] for q in parsed_questions],
                        research_question,
                        metric="repetition",
                        n=1,
                    )
                    scores["unigram_overlap"].append(repetition_proportion_unigram)

                    question_similarity = compute_similarity(
                        [q["question"] for q in parsed_questions],
                        research_question,
                        metric="question-similarity",
                    )
                    scores["question_similarity"].append(question_similarity)

                    # add system fingerprint
                    scores["system_fingerprint"].append(system_fingerprint)

                    # add random seed
                    scores["random_seed"].append(random_seed)

                    # add temperature
                    scores["temperature"].append(temperature)

                    print("=" * 50)
                except:
                    print(
                        f"Error in parsing the questionnaire: RQ=RQ{idx}, prompt={prompt_name}, news={news_status}, sqp={sqp_status}, seed={random_seed}, temperature={temperature}"
                    )
                    errors.append(
                        {
                            "research_question": research_question,
                            "prompt": prompt_name,
                            "news": news_status,
                            "sqp": sqp_status,
                            "seed": random_seed,
                            "temperature": temperature,
                        }
                    )

                    scores["rouge_l"].append(np.nan)
                    scores["semantic_similarity"].append(np.nan)
                    scores["bigram_overlap"].append(np.nan)
                    scores["unigram_overlap"].append(np.nan)
                    scores["question_similarity"].append(np.nan)
                    scores["system_fingerprint"].append(system_fingerprint)
                    scores["random_seed"].append(random_seed)
                    scores["temperature"].append(temperature)

                    continue

# save errors
errors_df = pd.DataFrame(errors)
errors_df.to_csv(
    f"{output_dir}/questionnaire_generation_errors.csv",
    index=False,
)

scores_df = pd.DataFrame(scores)
scores_df.to_csv(
    f"{output_dir}/questionnaire_generation_scores_advanced.csv",
    index=False,
)
