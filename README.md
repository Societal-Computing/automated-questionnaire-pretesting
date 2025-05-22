# Exploring LLMs for Automated Generation and Adaptation of Questionnaires

This repository contains the code for the experiments in the paper titled "Exploring LLMs for Automated Generation and Adaptation of Questionnaires" accepted at CUI 2025.

## Structure

```
├── data/ - the questions from the SQP database used in RAG
├── evaluation/ - functions to evaluate the questionnaire
├── models/ - initializes OpenAI API module
├── modules/ - modules for follow-up question, questions & relevant articles retrieval 
├── parsers/ - functions to parse generated questionnaire and list of personas
├── pretest_gesis/ - scripts for the GESIS pretest experiment
├── prompts/ - prompts for questionnaire generation, pretesting and reviewing
├── questionnaire_generation_experiment/ - scripts for the questionnaire generation ablation experiment
├── wvs_political_trust/ - scripts for the Political trust survey generation experiment
├── agents_interaction_gpt.py - Run the simulated Pilot study
├── analyze_prolific_responses.py - Analyze responses from Prolific
├── env.example - Example environment file (change to .env when running the scripts)
├── main_gpt.py - script to generate questionnaire
├── review_transcripts_gpt.py - script to review the interview transcripts
```
