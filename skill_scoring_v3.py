from skills_config import SKILL_CONFIG
from skill_weights import SKILL_WEIGHTS


def calculate_smart_skill_score(
    matched_skills,
    missing_skills,
    resume_domain
):
    boost = 0
    penalty = 0

    domain_skills = SKILL_CONFIG.get(resume_domain)

    # If domain not configured → fallback
    if not domain_skills:
        penalty += len(missing_skills) * 5
        return boost, penalty

    core_skills = domain_skills["core"]
    optional_skills = domain_skills["optional"]

    # Core skill penalties
    for skill in core_skills:
        if skill in missing_skills:
            penalty += 10   # heavy penalty

    # Optional skill penalties
    for skill in optional_skills:
        if skill in missing_skills:
            penalty += 3    # light penalty

    # Bonus if all core skills matched
    if all(skill in matched_skills for skill in core_skills):
        boost += 20

    return boost, penalty
