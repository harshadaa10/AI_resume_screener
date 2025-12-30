# =========================================================
# JD SKILL ENGINE (DOMAIN-AWARE)
# =========================================================

from skills_config import SKILL_CONFIG
from skill_weights import SKILL_WEIGHTS, MUST_HAVE_SKILLS


# =========================================================
# NORMALIZATION
# =========================================================
def normalize_text(text: str) -> str:
    return text.lower()


# =========================================================
# SKILL CATEGORY INFERENCE
# =========================================================
def infer_skill_weight(skill: str, domain: str) -> int:
    """
    Assigns weight to a skill based on domain relevance
    """

    domain_key = domain.lower()

    if domain_key in ["hr", "human resources"]:
        return SKILL_WEIGHTS.get("core_hr", 5)

    if domain_key in ["information-technology", "it"]:
        return SKILL_WEIGHTS.get("core_it", 5)

    if domain_key in ["engineering", "civil", "construction"]:
        return SKILL_WEIGHTS.get("core_engineering", 5)

    if domain_key in ["accountant", "finance", "banking"]:
        return SKILL_WEIGHTS.get("core_accounting", 5)

    if domain_key in ["advocate", "legal"]:
        return SKILL_WEIGHTS.get("core_legal", 5)

    if domain_key in ["sales", "marketing", "digital-media"]:
        return SKILL_WEIGHTS.get("core_sales", 5)

    if domain_key in ["management", "consultant", "business-analyst"]:
        return SKILL_WEIGHTS.get("core_management", 5)

    return 3  # default medium importance


# =========================================================
# MAIN JD SKILL EVALUATION
# =========================================================
def evaluate_jd_skills(jd_text: str, resume_text: str, jd_domain: str):
    """
    Returns:
        score (float)
        matched_skills (list)
        missing_skills (list)
    """

    jd_text = normalize_text(jd_text)
    resume_text = normalize_text(resume_text)

    matched_skills = []
    missing_skills = []
    score = 0.0

    domain_key = jd_domain.lower()

    # =====================================================
    # DOMAIN SKILLS
    # =====================================================
    domain_skills = SKILL_CONFIG.get(domain_key, [])

    for skill in domain_skills:
        weight = infer_skill_weight(skill, domain_key)

        if skill in resume_text:
            score += weight
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    # =====================================================
    # MUST-HAVE SKILLS (HEAVY PENALTY)
    # =====================================================
    must_have = MUST_HAVE_SKILLS.get(domain_key, [])

    for skill in must_have:
        if skill not in resume_text:
            score -= 10
            if skill not in missing_skills:
                missing_skills.append(skill)

    # =====================================================
    # SCORE FLOOR
    # =====================================================
    score = max(score, 0)

    return round(score, 2), matched_skills, missing_skills
