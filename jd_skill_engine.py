# jd_skill_engine.py

HR_CORE_SKILLS = [
    "recruitment",
    "employee relations",
    "performance management",
    "compliance",
    "labor law",
    "benefits administration"
]

HR_OPTIONAL_SKILLS = [
    "hr software",
    "analytics",
    "leadership",
    "communication"
]

HR_CERTIFICATIONS = [
    "shrm",
    "phr",
    "shrm-cp",
    "shrm-scp"
]

def evaluate_jd_skills(jd_text, resume_text):
    jd_text = jd_text.lower()
    resume_text = resume_text.lower()

    matched = []
    missing = []
    score = 0

    for skill in HR_CORE_SKILLS:
        if skill in resume_text:
            score += 5
            matched.append(skill)
        else:
            score -= 3
            missing.append(skill)

    for skill in HR_OPTIONAL_SKILLS:
        if skill in resume_text:
            score += 2
            matched.append(skill)

    for cert in HR_CERTIFICATIONS:
        if cert in resume_text:
            score += 3
            matched.append(cert)

    return score, matched, missing
