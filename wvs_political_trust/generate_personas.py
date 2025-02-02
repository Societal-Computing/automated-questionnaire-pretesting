from models.openai import client, MODEL
from prompts.questionnaire import PERSONA_GENERATOR_SYSTEM_PROMPT
from wvs_political_trust.prompt import QUESTIONNAIRE_GENERATION_PROMPT

experiment_dir = "./wvs_political_trust/experiments"

research_question = QUESTIONNAIRE_GENERATION_PROMPT

PERSONA_GENERATION_PROMPT = f"""
Generate a list of 50 personas from countries around the United States based on the following research question:
    
<question>{research_question}</question>
"""

# Save persona prompt
with open(f"{experiment_dir}/persona_generation_prompt.txt", "w") as f:
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

personas = response.choices[0].message.content


with open(f"{experiment_dir}/survey_personas.txt", "w") as f:
    f.write(personas)
