# Only the question that were pretested in the GESIS pretesting
# https://pretest.gesis.org/pretestProjekt/European-Commission-Hernández-Pretesting-of-special-module-on-ICT-at-work%2C-working-conditions-%26-learning-digital-skills-(English-Version)


QUESTIONNAIRE = [
    {
        "question": "Have you used any website or app to arrange a transport service (e.g. by car) from another individual in the last 12 months?",
        "question_type": "multiple_choice",
        "options": [
            "Yes, dedicated websites or apps (e.g. UBER, Blabla car)",
            " Yes, other websites or apps (including social networks)",
            "No, I have not.",
        ],
    },
    {
        "question": "In the last 12 months, have you used any internet platform/app (e.g. Upwork, TaskRabbit, Amazon Mechanical Turk…) as an intermediary for you to obtain regular or occasional paid work to carry out in a self-employed capacity?",
        "question_type": "single_choice",
        "options": [
            "Yes, as my main job",
            " Yes, as a secondary or occasional job",
            " No, never",
        ],
    },
    {
        "question": "The following questions concern the usage of information and communication technologies (computers and the internet) for your working activities. In case of multiple activities, please refer always to your main paid job.\nThink about your main paid job: Do you use computers, laptops, smartphones, or other computerised equipment at work?",
        "question_type": "single_choice",
        "options": ["Yes", "No"],
    },
    {
        "question": "How often do you actively use such equipment at work? Please tick one.",
        "question_type": "single_choice",
        "options": [
            "Every day or almost every day",
            "At least once a week (but not every day)",
            "Less than once a week",
        ],
    },
    {
        "question": "How often have the following activities been part of your main paid job, in the last 12 months? Please tick all that apply",
        "question_type": "multiple_choice",
        "options": [
            "Exchange emails",
            "Use social media to work",
            "Browse the internet to get work-related information",
            "Conduct online transactions (e.g. commercial, financial, transport, etc.)",
            "Enter data into business software or databases (e.g. for customer relations management) ",
            "Create or edit electronic documents",
            "Use specialised software for design or simulation (e.g. CAD)",
            "Use specialised software to analyse data (e.g. technical, financial, etc.)",
            "Use computerised equipment to control, operate or repair machines (e.g. car electronics, CNC, etc.)",
            "Design or maintain computer networks, servers, websites, security functionalities",
            "Programming and software development",
        ],
    },
    {
        "question": "In the last 12 months, did you have to learn how to use new software (programmes and applications)?",
        "question_type": "single_choice",
        "options": ["Yes", "No"],
    },
    {
        "question": "In the last 12 months, have the main tasks of your job changed as a result of the introduction of new software (programmes and applications)?",
        "question_type": "single_choice",
        "options": ["Yes", "No"],
    },
    {
        "question": "Over the past year, have you been involved in choosing, improving or otherwise modifying the software (programmes and applications) used for work in your department or organisation?",
        "question_type": "single_choice",
        "options": ["Yes", "No", "Not applicable"],
    },
    {
        "question": "Which of the following statements would best describe your digital skills at work? Please tick one answer value.",
        "question_type": "single_choice",
        "options": [
            "I need further training to cope well with my duties",
            " My actual digital skills correspond well with my duties",
            " I have the digital skills to cope with more demanding duties",
        ],
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
    },
    {
        "question": "In the last 12 months, did the usage of computers, laptops, smartphones, or other computerised equipment have a positive or a negative effect on your work-life balance, if any?",
        "question_type": "single_choice",
        "options": ["A positive effect", "A negative effect", "No relevant change"],
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
    },
]
