import regex as re

# QUESTION_REGEX = re.compile(
#     r"\d[.] (.+[?]) ?\n\s*Type: (\bclosed-ended\b|\bopen-ended\b) ?\n\s*Options: (.+)",
#     re.IGNORECASE
# )

QUESTION_REGEX = re.compile(
    r"\d[.] (.+[?]) ?\n\s*Type: (\b[C|c]losed-ended\b|\b[O|o]pen-ended\b) ?\n(?:\s*Options: (.+))?"
)


def parse_questionnaire_text(questionnaire_file: str) -> str:
    questionnaire = open(questionnaire_file).read()

    questions = QUESTION_REGEX.findall(questionnaire)

    # Prepare the questionnaire as a JSON/dictionary
    questions_out = []
    for question in questions:
        q = question[0]
        q_type = question[1]
        options = question[2].split(", ")
        questions_out.append({"question": q, "type": q_type, "options": options})

    return questions_out
