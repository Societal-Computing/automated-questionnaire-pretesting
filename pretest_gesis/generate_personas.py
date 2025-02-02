import json
import pandas as pd
from models.openai import client, MODEL
from pretest_gesis.questionnaire import get_questionnaire

from tqdm import tqdm

experiment_dir = "./pretest_gesis/experiments"
persona_description_file = f"{experiment_dir}/original_persona_desc.csv"

# Load the original persona descriptions
persona_descriptions = pd.read_csv(persona_description_file)
persona_descriptions = persona_descriptions.to_records(index=False)

PERSONA_GENERATOR_SYSTEM_PROMPT = """
You are a researcher working on Survey research.
You will be given a part of the persona details and the survey questionnaire. 
Try to be diverse with the names. They need to be from Great Britain.
For the preferences, base it on the survey questionnaire. Make it as detailed as possible and a single line.
Use the exact keywords: Name and Preferences

The persona will take part in the following survey questionnaire:
<questionnaire>
Q1. What diet do you follow?
    Options:
    - Vegan
    - Gluten-free
</questionnaire>

Example 1:
Generate the details for the following persona information:

<persona_partial_details>
Gender: male
Education: high
Age: 30
Job description: Engineer
Self-employed: X
</persona_partial_details>

The persona will take part in the following survey questionnaire:
<questionnaire>
The full survey questionnaire on a specific topic.
</questionnaire>

Name: a fictional name of a person from Great Britain.
Preferences: preferences based on the survey questionnaire in a single line.
"""

personas = []

for i, partial_details in enumerate(tqdm(persona_descriptions)):
    partial_details_text = f"Gender: {partial_details[1]}\nEducation: {partial_details[2]}\nAge: {partial_details[3]}\nJob description: {partial_details[4]}\nSelf-employed: {partial_details[5]}\nLocation: Great Britain"

    PERSONA_GENERATION_PROMPT = f"""
    Generate the details for the following persona information:
        
    <persona_partial_details>
    {partial_details_text}
    </persona_partial_details>

    The personas will take part in the following survey questionnaire:
    <questionnaire>
    {get_questionnaire(convert_to_text=True)}
    </questionnaire>
    """

    # Save persona prompt
    with open(
        f"{experiment_dir}/persona_generation_prompts/persona_generation_prompt_{i+1}.txt",
        "w",
    ) as f:
        f.write(PERSONA_GENERATION_PROMPT)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": PERSONA_GENERATOR_SYSTEM_PROMPT},
            {"role": "user", "content": PERSONA_GENERATION_PROMPT},
        ],
        # response_format={"type": "json_object"},
        temperature=1.1,
    )

    remaining_persona_details = response.choices[0].message.content

    with open(f"{experiment_dir}/survey_personas/survey_personas_{i+1}.txt", "w") as f:
        f.write(remaining_persona_details)

    for line in remaining_persona_details.split("\n"):
        if "Name:" in line:
            name = line.split(":")[1].strip()
        if "Preferences:" in line:
            preferences = line.split(":")[1].strip()

    persona = {
        "Name": name,
        "Gender": partial_details[1],
        "Education": partial_details[2],
        "Age": partial_details[3],
        "Job description": partial_details[4],
        "Self-employed": partial_details[5],
        "Preferences": preferences,
    }

    personas.append(persona)

import pickle

pickle.dump(
    personas, open(f"{experiment_dir}/survey_personas/survey_personas.pkl", "wb")
)

open(f"{experiment_dir}/survey_personas/survey_personas.json", "w").write(
    json.dumps(personas, indent=4)
)
