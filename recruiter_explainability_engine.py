# recruiter_explainability_engine.py

def generate_recruiter_explanation(
    candidate_name,
    jd_domain,
    resume_domain,
    skill_score,
    matched_skills,
    missing_skills,
    domain_penalty,
    fraud_result,
    final_score,
    decision
):
    explanation = {
        "candidate": candidate_name,
        "decision": decision,
        "summary": [],
        "strengths": [],
        "gaps": [],
        "risks": []
    }
    
    # ----------------------------
    # Domain reasoning
    # ----------------------------
    if domain_penalty == 0:
        explanation["summary"].append(
            f"Candidate has a direct domain match with JD ({jd_domain})."
        )
    elif domain_penalty > -10:
        explanation["summary"].append(
            f"Candidate comes from a related domain ({resume_domain})."
        )
    else:
        explanation["summary"].append(
            f"Candidate domain ({resume_domain}) differs significantly from JD ({jd_domain})."
        )

    # ----------------------------
    # Skill reasoning
    # ----------------------------
    explanation["summary"].append(
        f"Skill match score contributed {skill_score} points."
    )

    if matched_skills:
        explanation["strengths"].append(
            "Strong skills detected: " + ", ".join(matched_skills[:6])
        )

    if missing_skills:
        explanation["gaps"].append(
            "Missing key skills: " + ", ".join(missing_skills[:6])
        )
     
    # ----------------------------
    # Fraud / Inflation reasoning
    # ----------------------------
    if fraud_result["risk_level"] != "LOW RISK":
        explanation["risks"].append(
            f"Resume flagged as {fraud_result['risk_level']} for potential skill inflation."
        )
        explanation["risks"].extend(fraud_result["red_flags"])

    # ----------------------------
    # Final decision explanation
    # ----------------------------
    explanation["summary"].append(
        f"Final ATS score: {round(final_score, 2)}."
    )

    explanation["summary"].append(
        f"System recommendation: {decision}."
    )

    return explanation
