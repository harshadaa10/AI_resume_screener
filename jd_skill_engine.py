from jd_llm_engine import extract_skills_from_jd


def evaluate_jd_skills(jd_text, resume_text):
    jd_skills = extract_skills_from_jd(jd_text)
    resume_text = resume_text.lower()

    matched = []
    missing = []
    score = 0

    for skill in jd_skills:
        if skill in resume_text:
            matched.append(skill)
            score += 4
        else:
            missing.append(skill)
            score -= 2

    return score, matched, missing
