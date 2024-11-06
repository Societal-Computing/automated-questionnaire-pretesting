# Research Question to filter criteria for the SQP dataset
RQ_TO_FILTER_CRITERIA_SYSTEM_PROMPT = """
You are given a research question based on which you will define the parameters for a function call. You return the parameters in JSON format. The details of the parameters are as follows:

* Language
   Type: String
   Options:  'German', 'French', 'Dutch', 'Czech', 'Danish', 'Swedish', 'Finnish', 'Greek', 'Hungarian', 'English', 'Hebrew', 'Arabic',  'Russian', 'Italian', 'Norwegian', 'Polish', 'Portuguese', 'Slovene', 'Spanish', 'Catalan', 'Estonian', 'Icelandic', 'Slovak', 'Turkish', 'Ukrainian', 'Bulgarian', 'Latvian', 'Romanian', 'Croatian', 'Lithuanian', 'Albanian'
   Note: If the required option isn't available, select 'English' as the option.

* Domain
   Type: String
   Options: 'Leisure activities', 'Other domains', 'National politics',  'Living conditions and background variables', 'International politics', 'Family', 'Personal relations', 'Work', 'Health', 'European Union politics', 'Consumer behaviour'

Example:
Generate the parameters for the following research question:
<research_question>
What is the perspective of people in Germany about European politics?
</research_question>

Output:
{"language": "German", "domain": "European Union politics"}
"""

RQ_TO_FILTER_CRITERIA_USER_PROMPT = """
Generate the function parameters for the following research question:
<research_question>
{}
</research_question>
"""
