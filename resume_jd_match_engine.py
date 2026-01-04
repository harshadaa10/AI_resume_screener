from skill_engine import extract_skills
from domain_engine import detect_domain
from domain_penalty_engine import calculate_domain_penalty
from skill_weights import SKILL_WEIGHTS, MUST_HAVE_SKILLS


def calculate_resume_jd_match(jd_text, resume_text):
    jd_text = jd_text.lower()
    resume_text = resume_text.lower()

    jd_skills = extract_skills(jd_text)
    resume_skills = extract_skills(resume_text)

    jd_domain = detect_domain(jd_text)
    resume_domain = detect_domain(resume_text)

    matched_skills = list(set(jd_skills) & set(resume_skills))
    missing_skills = list(set(jd_skills) - set(resume_skills))

    # ==========================
    # 1️⃣ SKILL MATCH SCORE (50)
    # ==========================
    if jd_skills:
        skill_match_score = (len(matched_skills) / max(len(jd_skills), 1)) * 60
    else:
        skill_match_score = 0

# ==========================
# 2️⃣ WEIGHTED SKILL SCORE (20)
# ==========================
    weighted_score = 0
    for skill in matched_skills:
     if skill in SKILL_WEIGHTS:
        weighted_score += SKILL_WEIGHTS[skill]

    weighted_score = min(weighted_score, 20)


    # ==========================
    # 3️⃣ MUST-HAVE PENALTY (-30)
    # ==========================
    must_haves = MUST_HAVE_SKILLS.get(jd_domain.lower(), [])
    missing_must_haves = [
    s for s in must_haves
    if s not in resume_text and s in jd_text
]
    must_have_penalty = min(len(missing_must_haves) * 5, 20)

    # ==========================
    # 4️⃣ DOMAIN PENALTY (-20)
    # ==========================
    domain_penalty, domain_reason = calculate_domain_penalty(
        jd_domain, resume_domain
    )

    # ==========================
    # FINAL SCORE
    # ==========================
    final_score = (
        skill_match_score
        + weighted_score
        - must_have_penalty
        + domain_penalty
    )

    final_score = max(min(round(final_score), 100), 0)

    return {
        "match_score": final_score,
        "jd_domain": jd_domain,
        "resume_domain": resume_domain,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "missing_must_have_skills": missing_must_haves,
        "domain_reason": domain_reason
    }
