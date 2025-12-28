from skills_config import SKILLS

def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    return list(set(found_skills))
