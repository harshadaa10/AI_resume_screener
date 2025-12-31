def generate_explainability(res):
    """
    Generates recruiter-friendly explanation
    for why a candidate was shortlisted or rejected.
    """

    reasons = []
    concerns = []

    # --------------------------
    # 1️⃣ Skill Explanation
    # --------------------------
    if res["matched_skills"]:
        reasons.append(
            f"Matched key skills: {', '.join(res['matched_skills'][:5])}"
        )

    if res["missing_skills"]:
        concerns.append(
            f"Missing important skills: {', '.join(res['missing_skills'][:5])}"
        )

    # --------------------------
    # 2️⃣ Experience Explanation
    # --------------------------
    if res["experience_years"] >= 3:
        reasons.append(
            f"Relevant experience: {res['experience_years']} years"
        )
    else:
        concerns.append(
            f"Limited experience ({res['experience_years']} years)"
        )

    # --------------------------
    # 3️⃣ Domain Fit
    # --------------------------
    if res["resume_domain"] == res["jd_domain"]:
        reasons.append("Strong domain alignment with JD")
    else:
        concerns.append(
            f"Domain mismatch: Resume ({res['resume_domain']}) vs JD ({res['jd_domain']})"
        )

    # --------------------------
    # 4️⃣ Certifications
    # --------------------------
    if res["certifications"]:
        reasons.append(
            f"Relevant certifications: {', '.join(res['certifications'])}"
        )

    # --------------------------
    # 5️⃣ Bias Transparency
    # --------------------------
    if res.get("bias_flags"):
        reasons.append(
            "Bias-neutral evaluation applied (college/gender ignored)"
        )

    # --------------------------
    # 6️⃣ Final Verdict
    # --------------------------
    verdict = (
        "Shortlisted"
        if res["final_score"] >= 60
        else "Not Shortlisted"
    )

    return {
        "verdict": verdict,
        "strengths": reasons,
        "concerns": concerns
    }
