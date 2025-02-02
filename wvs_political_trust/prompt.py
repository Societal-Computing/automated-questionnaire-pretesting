QUESTIONNAIRE_GENERATION_PROMPT = """
Generate a questionnaire for a survey on political trust for the United States. The questionnaire should evaluate political trust as a latent concept so instead of directly asking the participants, the questionnaire should measure political trust using other aspects based on the following theory.

Beliefs are shaped by a mix of cognitive and affective processes, adapting to new information or stabilizing as enduring political attitudes. 
Cognitive processes involve using knowledge and experience to form expectations about political actors or institutions based on benevolence (caring for others), integrity (keeping promises), and competence (ability to deliver). 
Affective processes are driven by emotions tied to shared values, norms, and group identities. 
These influences guide "intentions to act," where individuals take actions that demonstrate trust by making themselves vulnerable to political actors or institutions. 
Cognitive, affective, and intention-based trust interact dynamically, with their relative impact varying by individual and context.

There are different sections in the questionnaire. Generate each section based on the following instructions.

1. Generate 6 statements to rate on a likert scale (1-5, 1 meaning Agree strongly and 5 meaning disagree strongly) on the question "How you feel about the national congress in your country?". Number it from P1 to P6.
2. Generate 6 statements to rate on a likert scale (1-5, 1 meaning Agree strongly and 5 meaning disagree strongly) on the question "How do you feel about the government in your country?". Number it from G1 to G6.
3. Generate 6 statements to rate on a likert scale (1-5, 1 meaning Agree strongly and 5 meaning disagree strongly) on the question "How do you feel about the United Nations?". Number it from UN1 to UN6.
4. Generate 15 statements to rate on a likert scale (1-5, 1 meaning Agree strongly and 5 meaning disagree strongly) related to trust on Politicians and the government. Number it from A to O.
5. Generate a question asking about their trust on the <head of state> in their country. Replace <head of state> with the respective head of state in the country. Make sure to use a likert scale of 0-10, 0 meaning no trust at all and 10 meaning a great deal of trust.
"""
