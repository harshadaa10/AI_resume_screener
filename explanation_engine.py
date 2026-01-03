def generate_explainability(res):
    """
    Generates recruiter-friendly explanation
    explaining WHY a candidate was shortlisted or rejected.
    Safe against missing keys.
    """

    reasons = []
    concerns = []

    # --------------------------
    # 1️⃣ Skill Explanation
    # --------------------------
    matched_skills = res.get("matched_skills", [])
    missing_skills = res.get("missing_skills", [])

    if matched_skills:
        reasons.append(
            f"Matched key skills: {', '.join(matched_skills[:5])}"
        )
    else:
        concerns.append("No strong skill match found")

    if missing_skills:
        concerns.append(
            f"Missing important skills: {', '.join(missing_skills[:5])}"
        )

    # --------------------------
    # 2️⃣ Experience Explanation
    # --------------------------
    experience_years = res.get("experience_years", 0)

    if experience_years >= 3:
        reasons.append(
            f"Relevant experience: {experience_years} years"
        )
    else:
        concerns.append(
            f"Limited experience ({experience_years} years)"
        )

    # --------------------------
    # 3️⃣ Domain Fit
    # --------------------------
    resume_domain = res.get("resume_domain", "Unknown")
    jd_domain = res.get("jd_domain", "Unknown")

    if resume_domain == jd_domain:
        reasons.append("Strong domain alignment with Job Description")
    else:
        concerns.append(
            f"Domain mismatch: Resume ({resume_domain}) vs JD ({jd_domain})"
        )

    # --------------------------
    # 4️⃣ Certifications
    # --------------------------
    certifications = res.get("certifications", [])

    if certifications:
        reasons.append(
            f"Relevant certifications: {', '.join(certifications)}"
        )

    # --------------------------
    # 5️⃣ Fraud / Inflation Signals
    # --------------------------
    fraud_flags = res.get("fraud_flags", [])

    if fraud_flags:
        concerns.append(
            f"Potential resume inflation detected: {', '.join(fraud_flags)}"
        )

    # --------------------------
    # 6️⃣ Bias Transparency
    # --------------------------
    bias_flags = res.get("bias_flags", [])

    if bias_flags:
        reasons.append(
            "Bias-neutral evaluation applied (college, gender, name ignored)"
        )

    # --------------------------
    # 7️⃣ Final Verdict
    # --------------------------
    final_score = res.get("final_score", 0)

    if final_score >= 75:
        verdict = "Strongly Shortlisted"
    elif final_score >= 60:
        verdict = "Shortlisted"
    elif final_score >= 40:
        verdict = "Consider with Caution"
    else:
        verdict = "Not Shortlisted"

    return {
        "verdict": verdict,
        "strengths": reasons,
        "concerns": concerns
    }
