def recommend_jobs(resume_text):

    text = resume_text.lower()

    jobs = []

    # Programming
    if "python" in text:
        jobs.append("Python Developer")

    if "java" in text:
        jobs.append("Java Developer")

    if "c++" in text or "c programming" in text:
        jobs.append("Software Developer")

    # Web Development
    if ("html" in text or
        "css" in text or
        "javascript" in text or
        "react" in text):
        jobs.append("Web Developer")
        jobs.append("Frontend Developer")

    # Database
    if "sql" in text or "mysql" in text:
        jobs.append("Database Developer")
        jobs.append("Data Analyst")

    # Data Science
    if ("pandas" in text or
        "numpy" in text or
        "machine learning" in text):
        jobs.append("Data Scientist")

    # AI
    if ("artificial intelligence" in text or
        "deep learning" in text or
        "tensorflow" in text):
        jobs.append("AI Engineer")

    # Cloud
    if ("aws" in text or
        "azure" in text or
        "cloud" in text):
        jobs.append("Cloud Engineer")

    # Cyber Security
    if ("security" in text or
        "cyber" in text):
        jobs.append("Cyber Security Analyst")

    # Testing
    if ("testing" in text or
        "selenium" in text):
        jobs.append("QA Engineer")

    # Remove duplicates
    jobs = list(set(jobs))

    if not jobs:
        jobs.append("Software Engineer")
        jobs.append("Graduate Trainee")
        jobs.append("Entry Level Developer")

    return jobs