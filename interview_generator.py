def generate_questions(
        role,
        company,
        job_description):

    questions = []

    # HR Questions

    questions.extend([

        "Tell me about yourself.",

        "Why should we hire you?",

        "What are your strengths?",

        "What are your weaknesses?",

        "Where do you see yourself in 5 years?"
    ])

    role = role.lower()

    # Python Questions

    if "python" in role:

        questions.extend([

            "What is Python?",

            "Difference between List and Tuple?",

            "Explain OOP concepts.",

            "What is Flask?",

            "What is Exception Handling?"
        ])

    # Java Questions

    elif "java" in role:

        questions.extend([

            "What is JVM?",

            "Difference between JDK and JRE?",

            "Explain Inheritance.",

            "Explain Polymorphism.",

            "What is Collection Framework?"
        ])

    # Data Science Questions

    elif "data" in role:

        questions.extend([

            "What is Machine Learning?",

            "Difference between AI and ML?",

            "Explain Regression.",

            "What is Overfitting?"
        ])

    # Company Based Questions

    company = company.lower()

    if company == "tcs":

        questions.append(
            "What do you know about TCS?"
        )

    elif company == "infosys":

        questions.append(
            "Why do you want to join Infosys?"
        )

    elif company == "zoho":

        questions.append(
            "Explain your project architecture."
        )

    elif company == "amazon":

        questions.append(
            "Explain Amazon Leadership Principles."
        )

    elif company == "google":

        questions.append(
            "Why Google?"
        )

    # JD Based Questions

    if job_description:

        words = job_description.split()

        for word in words[:5]:

            questions.append(
                f"Explain your experience with {word}."
            )

    return questions