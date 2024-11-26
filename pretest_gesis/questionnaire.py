# Only the question that were pretested in the GESIS pretesting
# https://pretest.gesis.org/pretestProjekt/European-Commission-Hernández-Pretesting-of-special-module-on-ICT-at-work%2C-working-conditions-%26-learning-digital-skills-(English-Version)


QUESTIONNAIRE = [
    {
        "question": "How often on average did you use the Internet in the last 3 months? Please tick one answer option.",
        "question_type": "single_choice",
        "options": [
            "Every day or almost every day",
            "At least once a week (but not every day)",
            "Less than once a week",
        ],
        "q_number": "C1",
        "conditions": "Go to C2",
    },
    {
        "question": "Did you use any of the following mobile devices to access the Internet away from home or work in the last 3 months? Please tick all that apply or the last answer option",
        "question_type": "multiple_choice",
        "options": [
            "Mobile phone (or smart phone) via mobile phone network",
            "Mobile phone (or smart phone) via wireless network (e.g. WiFi)",
            "Portable computer (e.g. laptop, tablet) via mobile phone network, using USB key or (SIM) card or mobile phone or smart phone as modem",
            "Portable computer (e.g. laptop, tablet) via wireless network (e.g. WiFi)",
            "Other devices",
            "I didn't access the internet via any mobile device away from home or work",
        ],
        "q_number": "C2",
        "conditions": "Go to C3",
    },
    {
        "question": "For which of the following activities did you use the internet in the last 3 months for private purpose?",
        "options": [
            "Sending/receiving e-mails",
            "Telepohning over the internet / video calls (via webcam) over the internet (using applications, e.g. Skype, Facetime)",
            "Participating in social networks (creating user profile, posting messages or other contributions to Facebook, twitter, Instagram, Snapchat, etc.)",
            "Finding information about goods or services",
            "Listening to music (e.g. web radio, music streaming)",
            "Watching Internet streamed TV (live or catch-up) from TV broadcasters",
            "Watching Video on Demand from commercial services",
            "Watching video content from sharing services",
            "Playing or downloading games",
            "Seeking health-related information (e.g. injuries, diseases, nutrition, improving health, etc.)",
            "Making an appointment with a practitioner via a website or apps (e.g. of a hospital or a health care centre)",
            "Selling of goods or services, e.g. via auctions (e.g. eBay)",
            "Internet Banking",
        ],
        "question_type": "multiple_choice",
        "q_number": "C3",
        "conditions": "Go to C4",
    },
    {
        "question": "Have you conducted any of the following learning activities over the Internet for educational, professional or private purposes in the last 3 months? (Please tick all that apply)",
        "options": [
            "Doing an online course",
            "Using online learning material other than a complete online course (e.g. audio-visual materials, online learning software, electronic textbooks)",
            "Communicating with instructors or students using educational websites/portals",
        ],
        "question_type": "multiple_choice",
        "q_number": "C4",
        "conditions": "Go to C5",
    },
    {
        "question": "Have you used any website or app to arrange an accommodation (room, apartment, house, holiday cottage, etc.) from another individual in the last 12 months? (Please tick all that apply or ”No, I have not”)",
        "options": [
            "Yes, dedicated websites or apps (such as AIRBNB)",
            "Yes, other websites or apps (including social networks)",
            "No, I have not.",
        ],
        "question_type": "multiple_choice",
        "q_number": "C5",
        "conditions": "Go to C6",
    },
    {
        "question": "Have you used any website or app to arrange a transport service (e.g. by car) from another individual in the last 12 months?",
        "question_type": "multiple_choice",
        "options": [
            "Yes, dedicated websites or apps (e.g. UBER, Blabla car)",
            "Yes, other websites or apps (including social networks)",
            "No, I have not.",
        ],
        "q_number": "C6",
        "conditions": "If a) or b) in C6, Go to probe_1; otherwise, go to C7",
    },
    {
        "question": "In the previous question you answered that you used websites or apps to arrange a transport service from another individual. Which websites or apps did you have in mind when answering this question?",
        "question_type": "open_ended",
        "options": [],
        "q_number": "probe_1",
        "conditions": "Go to C7",
    },
    {
        "question": "In the last 12 months, have you used any internet platform/app (e.g. Upwork, TaskRabbit, Amazon Mechanical Turk…) as an intermediary for you to obtain regular or occasional paid work to carry out in a self-employed capacity?",
        "question_type": "single_choice",
        "options": [
            "Yes, as my main job",
            " Yes, as a secondary or occasional job",
            " No, never",
        ],
        "q_number": "C7",
        "conditions": "Go to E1",
    },
    {
        "question": "In the previous question you answered that you have used an internet platform or app to obtain work. What platforms or applications did you consider when answering?",
        "question_type": "open_ended",
        "options": [],
        "q_number": "probe_2",
        "conditions": "Go to E1",
    },
    {
        "question": "When did you last buy or order goods or services for private use over the Internet?",
        "question_type": "single_choice",
        "options": [
            "Within the last 3 months",
            "Between 3 and a year ago",
            "More than 1 year ago",
            "Never bought or ordered",
        ],
        "q_number": "E1",
        "conditions": 'If "Within the last 3 months" or "Between 3 and a year ago" go to E2, else go to Q1',
    },
    {
        "question": "What types of goods or services did you buy or order over the Internet for private use in the last 12 months? (Please tick all that apply)",
        "question_type": "multiple_choice",
        "options": [
            "Food or groceries",
            "Household goods (e.g. furniture, toys, etc; excluding consumer electronics)",
            "Medicine",
            "Clothes, sports goods",
            "Computer hardware",
            "Electronic equipment (incl. cameras)",
            "Telecommunication services (e.g. TV, broadband subscriptions, fixed line or mobile phone subscriptions, uploading money on prepaid phone cards, etc.)",
            "Holiday accommodation (hotel, etc.)",
            "Other travel arrangements (e.g. transport tickets, car hire, etc.)",
            "Tickets for events",
            "Films, music",
            "Books, magazines, newspapers",
            "e-learning material",
            "Video games software, other computer software and software upgrades",
            "Other",
        ],
        "q_number": "E2",
        "conditions": "Go to E3",
    },
    {
        "question": "From whom did you buy or order goods or services for private purpose over the Internet in the last 12 months?",
        "options": [
            "National sellers",
            "Sellers from other EU countries",
            "Sellers from the rest of the world",
            "Country of origin of sellers is not known",
        ],
        "question_type": "multiple_choice",
        "q_number": "E3",
        "conditions": "Go to Q1",
    },
    {
        "question": "Think about your main paid job: Do you use computers, laptops, smartphones, or other computerised equipment at work?",
        "question_type": "single_choice",
        "options": ["Yes", "No"],
        "q_number": "Q1",
        "conditions": "If Yes, go to Q2, else go to Q11",
    },
    {
        "question": "How often do you actively use such equipment at work? Please tick one.",
        "question_type": "single_choice",
        "options": [
            "Every day or almost every day",
            "At least once a week (but not every day)",
            "Less than once a week",
        ],
        "q_number": "Q2",
        "conditions": "Go to probe_3",
    },
    {
        "question": "How often do you actively use the following devices for working activities?",
        "question_type": "matrix_style",
        "options": [
            "Daily",
            "Less than daily",
            "Never",
        ],
        "statements": [
            "Desktop computers",
            "Laptops",
            "Tablets",
            "Smartphones",
            "Other",
        ],
        "q_number": "probe_3",
        "conditions": "Go to probe_4",
    },
    {
        "question": "In one of the previous questions, we asked about computerised equipment. Which tools do you consider to be computerised equipment?",
        "question_type": "open_ended",
        "options": [],
        "q_number": "probe_4",
        "conditions": "Go to Q3",
    },
    {
        "question": "For your main paid job: Which of these portable devices (e.g. laptop, netbook, smartphone, tablet) do you use? (Please tick all that apply)",
        "question_type": "multiple_choice",
        "options": [
            "Your own personal device",
            "A portable device provided by your employer",
        ],
        "q_number": "Q3",
        "conditions": "Go to Q4",
    },
    {
        "question": "How often have the following activities been part of your main paid job, in the last 12 months? Please tick all that apply",
        "question_type": "matrix_style",
        "options": [
            "Daily",
            "Less than daily",
            "Never",
        ],
        "statements": [
            "Exchange emails",
            "Use social media to work",
            "Browse the internet to get work-related information",
            "Conduct online transactions (e.g. commercial, financial, transport, etc.)",
            "Enter data into business software or databases (e.g. for customer relations management)",
            "Create or edit electronic documents",
            "Use specialised software for design or simulation (e.g. CAD)",
            "Use specialised software to analyse data (e.g. technical, financial, etc.)",
            "Use computerised equipment to control, operate or repair machines (e.g. car electronics, CNC, etc.)",
            "Design or maintain computer networks, servers, websites, security functionalities",
            "Programming and software development",
        ],
        "q_number": "Q4",
        "conditions": 'If "Daily" or "less than daily" for "Enter data into business software or databases (e.g. for customer relations management)", Go to probe_5; else go to probe_6',
    },
    {
        "question": "In the previous question you answered that you enter data into business software or databases (e.g. for customer relations management). Could you please explain your tasks in this context a bit further?",
        "question_type": "open_ended",
        "options": [],
        "q_number": "probe_5",
        "conditions": "Go to Q5",
    },
    {
        "question": "Do you perform any further digital activities that were not mentioned in the previous question? Please describe briefly.",
        "question_type": "open_ended",
        "options": [],
        "q_number": "probe_6",
        "conditions": "Go to Q5",
    },
    {
        "question": "In the last 12 months, did you have to learn how to use new software (programmes and applications)?",
        "question_type": "single_choice",
        "options": ["Yes", "No"],
        "q_number": "Q5",
        "conditions": "If Yes, Go to probe_7; If No, Go to Q6",
    },
    {
        "question": "Please describe the new software (programmes and applications) you had to learn.",
        "question_type": "open_ended",
        "options": [],
        "q_number": "probe_7",
        "conditions": "Go to Q6",
    },
    {
        "question": "In the last 12 months, have the main tasks of your job changed as a result of the introduction of new software (programmes and applications)?",
        "question_type": "single_choice",
        "options": ["Yes", "No"],
        "q_number": "Q6",
        "conditions": "If Yes, Go to probe_8; If No, Go to Q7",
    },
    {
        "question": "Could you please tell us how you felt about these changes?",
        "question_type": "open_ended",
        "options": [],
        "q_number": "probe_8",
        "conditions": "Go to Q7",
    },
    {
        "question": "Over the past year, have you been involved in choosing, improving or otherwise modifying the software (programmes and applications) used for work in your department or organisation?",
        "question_type": "single_choice",
        "options": ["Yes", "No", "Not applicable"],
        "q_number": "Q7",
        "conditions": "If Yes, Go to probe_9; If No, Go to Q8",
    },
    {
        "question": "Please describe how you have been involved in the selection, improvement or modification of the software programmes or applications used for work in your department or organisation.",
        "question_type": "open_ended",
        "options": [],
        "q_number": "probe_9",
        "conditions": "Go to Q8",
    },
    {
        "question": "Which of the following statements would best describe your digital skills at work? Please tick one answer value.",
        "question_type": "single_choice",
        "options": [
            "I need further training to cope well with my duties",
            " My actual digital skills correspond well with my duties",
            " I have the digital skills to cope with more demanding duties",
        ],
        "q_number": "Q8",
        "conditions": "If a) or c), Go to probe_10; If b), Go to Q9",
    },
    {
        "question": "What skills you consider to be digital skills?",
        "question_type": "open_ended",
        "options": [],
        "q_number": "probe_10",
        "conditions": 'If "Yes" to either options in Q3, Go to Q9; otherwise Go to Q10',
    },
    {
        "question": "In the last 12 months, did the usage of computers, laptops, smartphones, or other computerised equipment at work increase or reduce any of the following job characteristics, if any? Please tick all that apply",
        "question_type": "matrix_style",
        "options": [
            "Increase",
            "Decrease",
            "No relevant change",
        ],
        "statements": [
            "The time spent on repetitive and routine tasks",
            "My work productivity",
            "The opportunities to be creative",
            "The freedom and independence in organising my tasks",
            "The monitoring of my performance at work",
            "The need to learn new things",
            "The collaboration and cooperation with colleagues or business partners",
            "The amount of irregular working hours (night, weekend, shift work)",
        ],
        "q_number": "Q9",
        "conditions": 'If "Increase" or "Decrease" to "The amount of irregular working hours" in Q9, Go to probe_11; otherwise Go to Q10',
    },
    {
        "question": "You answered that the usage of computers etc. increased/decreased the amount of irregular working hours. Please explain your answer a little further. Why did you select this answer?",
        "question_type": "open_ended",
        "options": [],
        "q_number": "probe_11",
        "conditions": "Go to Q10",
    },
    {
        "question": "In the last 12 months, did the usage of computers, laptops, smartphones, or other computerised equipment have a positive or a negative effect on your work-life balance, if any?",
        "question_type": "single_choice",
        "options": ["A positive effect", "A negative effect", "No relevant change"],
        "q_number": "Q10",
        "conditions": 'If "A positive effect", Go to probe_12; If "A negative effect", Go to probe_13; Else, Go to Q11',
    },
    {
        "question": "Please describe the most important positive changes you have experienced thanks to the usage of computers or similar devices",
        "question_type": "open_ended",
        "options": [],
        "q_number": "probe_12",
        "conditions": "Go to Q11",
    },
    {
        "question": "Please describe the negative changes you have experienced due to the usage of computers or similar devices",
        "question_type": "open_ended",
        "options": [],
        "q_number": "probe_13",
        "conditions": "Go to Q11",
    },
    {
        "question": "In which of the following locations, on average, do you spend the majority of your working time? Please tick one answer value.",
        "question_type": "single_choice",
        "options": [
            "Your employer’s/your own business’ premises (e.g. office, factory, shop, school, etc.)",
            "Clients’ premises or premises of business/commercial partners",
            "Your own home",
            "On the move, in a vehicle, an outside site (e.g. construction site, agricultural field, streets of a city) or public spaces.",
        ],
        "q_number": "Q11",
        "conditions": "Go to R1",
    },
    {
        "question": "Have you undergone any of the following learning activities to improve your digital skills during the past 12 months? Please tick all that apply",
        "question_type": "multiple_choice",
        "options": [
            "Training courses paid by yourself",
            "Training courses paid or provided by your employer",
            "Training courses paid or provided by public programs or organisations other than your employer",
            "On-the-job training (e.g. co-workers, supervisors)",
            "Self-study using free online courses",
        ],
        "q_number": "R1",
        "conditions": "Go to probe_14",
    },
    {
        "question": "In the previous list, did you miss any further relevant type of learning activities that you have undertaken? If so, please describe them.",
        "question_type": "open_ended",
        "options": [],
        "q_number": "probe_14",
        "conditions": "Go to R2",
    },
    {
        "question": "In which of the following domains did you undertake the training? Please tick all that apply",
        "question_type": "multiple_choice",
        "options": [
            "The specific software applications I have to use at work (e.g. office suites, accounting software inventory management, internal planning software, etc.)",
            "Online marketing and e-Commerce techniques",
            "Social media for cooperation with colleagues or external partners (e.g. google groups, facebook, Jive)",
            "Programming languages, including design and management of websites",
            "Data analysis, business intelligence and management of databases",
            "Maintenance of computer networks, servers, websites, security functionalities",
            "Cyber security and privacy management",
            "Other",
        ],
        "q_number": "R2",
        "conditions": 'If "Other" is selected, Go to probe_15; Else, return "End of questionnaire"',
    },
    {
        "question": "The training you have undertaken did not match any of the domains listed in the previous question. Please describe the type of training you took.",
        "question_type": "open_ended",
        "options": [],
        "q_number": "probe_15",
        "conditions": 'Return to "End of questionnaire"',
    },
]


NEXT_QUESTION_SELECTOR_SYSTEM_PROMPT = """You will be provided with a questionnaire and the chat history. The questionnaire contains the conditions to follow after the participant has answered the survey questions in a specific way. Your task is to select the appropriate next question based on the chat history.

Example:
Get the next question based on the chat history.
<chat_history>
Question: A1. Do you or anyone in your household have access to the internet at home?
Options: ['Yes', 'No', 'Don't know']
Type: single_choice
Question Type: Main question
Response: Yes
Next question: If yes, go to A2; If no, go to B1; If don't know, go to B1
</chat_history>

Output:
A2
"""

NEXT_QUESTION_SELECTOR_PROMPT = """
Get the next question based on the chat history.
<chat_history>
{}
</chat_history>"""


def get_questionnaire(convert_to_text=False):
    if not convert_to_text:
        return QUESTIONNAIRE

    import string

    questionnaire_text = ""
    for question in QUESTIONNAIRE:
        questionnaire_text += f'{question["q_number"]}. {question["question"]}'
        questionnaire_text += (
            " (select one)\n"
            if question["question_type"] == "single_choice"
            else " (select all that apply)\n"
        )
        questionnaire_text += "    Options:"
        for c, o in zip(string.ascii_lowercase, question["options"]):
            questionnaire_text += f"\n    {c}) {o}"

        questionnaire_text += f'\n    Next question: {question["conditions"]}\n\n'

    return questionnaire_text
