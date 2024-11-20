from models.openai import client, MODEL
from prompts.questionnaire import PERSONA_GENERATOR_SYSTEM_PROMPT

experiment_dir = "./pretest_gesis/experiments"

persona_instructions = """
The survey on ICT usage at work is conducted in Great Britain. All the participants are British. The target population is employees and self-employed respondents.
The selection of the target population is based on the quotas age (18 to 65 years in three groups: 18-30; 31-50; 51-65), gender (male; female), and education (lower; higher education). 
In addition, a minimum of 20 percent of respondents in each country was expected to be self-employed.
"""

PERSONA_GENERATION_PROMPT = f"""
Generate a list of 75 personas based on the following information:
    
<question>{persona_instructions}</question>
"""

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


with open(f"{experiment_dir}/survey_personas.txt", "w") as f:
    f.write(personas)
