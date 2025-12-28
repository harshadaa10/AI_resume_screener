from skills_config import SKILLS
from skill_weights import SKILL_WEIGHTS, MUST_HAVE_SKILLS

def calculate_skill_score(matched_skills, missing_skills):
    boost = 0
    penalty = 0

    # Boost for matched skills
    for category, skills in SKILLS.items():
        weight = SKILL_WEIGHTS.get(category, 1)
        for skill in skills:
            if skill in matched_skills:
                boost += weight

    # Penalty for missing must-have skills
    for skill in MUST_HAVE_SKILLS:
        if skill in missing_skills:
            penalty += 5

    return boost, penalty
