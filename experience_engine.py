# experience_engine.py
import re

def extract_experience(text):
    text = text.lower()

    patterns = [
        r'(\d+)\+?\s*years?',
        r'(\d+)\s*-\s*(\d+)\s*years?',
        r'(\d+)\s*yrs?'
    ]

    years = []

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):
                years.append(int(match[0]))
            else:
                years.append(int(match))

    return max(years) if years else 0


def experience_score(jd_text, resume_text):
    jd_exp = extract_experience(jd_text)
    resume_exp = extract_experience(resume_text)

    score = 0

    if jd_exp == 0:
        return 0, resume_exp

    if resume_exp >= jd_exp + 2:
        score = 15
    elif resume_exp >= jd_exp:
        score = 10
    elif resume_exp >= jd_exp - 1:
        score = -5
    else:
        score = -10

    return score, resume_exp
