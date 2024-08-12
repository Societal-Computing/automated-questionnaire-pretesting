import evaluate
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer

rouge = evaluate.load("rouge")
model = SentenceTransformer("all-mpnet-base-v2")

# Question-level metrics

# Relevance metrics


# Word-level similarity (Rouge-L)
def _compute_rouge_l(questions, research_question):
    research_questions = [research_question] * len(questions)

    rouge_l_score = rouge.compute(
        predictions=questions,
        references=research_questions,
        rouge_types=["rougeL"],
        use_aggregator=True,
    )

    return round(rouge_l_score["rougeL"], 5)


# Sentence-level (Semantic) similarity
def _compute_semantic_similarity(questions, research_question):
    research_questions = [research_question] * len(questions)

    question_embeddings = model.encode(questions)
    research_question_embeddings = model.encode(research_questions)

    similarities = model.similarity(question_embeddings, research_question_embeddings)

    similarities = [sims[0] for sims in similarities]

    return round(np.mean(similarities), 5)


# Specificity metrics


# Word-level repetition
def _compute_repetition_proportion(questions, n=1):
    cv = CountVectorizer(ngram_range=(n, n))
    ngram_counts = cv.fit_transform(questions)

    n_unique_ngrams = len(cv.get_feature_names_out())
    total_ngrams = ngram_counts.sum()

    return round((1 - n_unique_ngrams / total_ngrams), 5)


def _compute_question_similarity(questions):
    similar_question_count = 0
    for i in range(len(questions)):
        for j in range(i + 1, len(questions)):
            e_q1 = model.encode(questions[i])
            e_q2 = model.encode(questions[j])

            sim = model.similarity(e_q1, e_q2).numpy()[0]

            if sim > 0.95:
                similar_question_count += 1

    return round(similar_question_count / len(questions), 5)


def compute_similarity(questions, research_question, metric="rouge-l"):
    if metric == "rouge-l":
        return _compute_rouge_l(questions, research_question)
    elif metric == "semantic":
        return _compute_semantic_similarity(questions, research_question)
    elif metric == "repetition":
        return _compute_repetition_proportion(questions)
    elif metric == "question-similarity":
        return _compute_question_similarity(questions)
    else:
        raise ValueError(f"Metric '{metric}' not recognized.")
