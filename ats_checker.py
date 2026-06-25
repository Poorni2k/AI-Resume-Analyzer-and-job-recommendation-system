import re

def calculate_ats_score(resume_text, job_description):

    resume_words = set(
        re.findall(r'\w+', resume_text.lower())
    )

    jd_words = set(
        re.findall(r'\w+', job_description.lower())
    )

    if len(jd_words) == 0:
        return 0

    matched = resume_words.intersection(jd_words)

    score = int(
        (len(matched) / len(jd_words)) * 100
    )

    return score


def get_missing_keywords(resume_text, job_description):

    resume_words = set(
        re.findall(r'\w+', resume_text.lower())
    )

    jd_words = set(
        re.findall(r'\w+', job_description.lower())
    )

    missing = list(
        jd_words - resume_words
    )

    return missing[:20]


def ai_resume_suggestions(score, missing_keywords):

    suggestions = []

    if score < 30:

        suggestions.append(
            "ATS score is very low."
        )

        suggestions.append(
            "Add Technical Skills section."
        )

        suggestions.append(
            "Add internship experience."
        )

        suggestions.append(
            "Add certifications."
        )

        suggestions.append(
            "Add relevant projects."
        )

    elif score < 60:

        suggestions.append(
            "Resume needs improvement."
        )

        suggestions.append(
            "Add missing skills from job description."
        )

        suggestions.append(
            "Improve project descriptions."
        )

    elif score < 80:

        suggestions.append(
            "Good ATS score."
        )

        suggestions.append(
            "Optimize keywords further."
        )

    else:

        suggestions.append(
            "Excellent ATS score."
        )

        suggestions.append(
            "Resume is ATS friendly."
        )

    if len(missing_keywords) > 0:

        suggestions.append(
            "Important missing keywords:"
        )

        for keyword in missing_keywords[:10]:

            suggestions.append(keyword)

    return suggestions