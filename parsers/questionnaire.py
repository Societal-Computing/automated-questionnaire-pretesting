import regex as re


def parse_questionnaire_text(questionnaire_file: str) -> str:
    questionnaire = open(questionnaire_file).read()

    question_pattern = r"(\d+)\.\s*(.*?)\n\s*(.*?):\s*(.*?)\n\s*(.*?):\s*(.*)"

    # Find all matches
    matches = re.findall(question_pattern, questionnaire)

    # Process the matches
    questions_list = []
    for match in matches:
        options = [option.strip() for option in match[5].split(",")]

        if options[0] == "-":
            # If the options are empty, set the options list to an empty list
            options = []

        question_dict = {
            "question": match[1].strip(),
            "type": "closed-ended" if options else "open-ended",
            "options": options,
        }
        questions_list.append(question_dict)

    return questions_list
