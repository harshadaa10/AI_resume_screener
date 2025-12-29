"""
Recommendation Engine
---------------------
Provides hiring recommendations based on ATS signals.
"""

def hiring_recommendation(resume_data):
    """
    Generate hiring recommendation based on resume evaluation.

    Input:
        resume_data (dict) – one ranked resume entry

    Output:
        dict with:
            - recommendation
            - action
            - reasoning
    """

    score = resume_data.get("final_score", 0)
    confidence = resume_data.get("confidence", "Low Match")
    domain_match = resume_data.get("resume_domain") == resume_data.get("jd_domain")
    matched_skills_count = len(resume_data.get("matched_skills", []))
    experience_years = resume_data.get("experience_years", 0)
    certifications = resume_data.get("certifications", [])

    reasoning = []

    # --------------------------
    # STRONG HIRE
    # --------------------------
    if (
        score >= 75 and
        domain_match and
        matched_skills_count >= 5 and
        experience_years >= 3
    ):
        recommendation = "Strong Hire"
        action = "Immediate Shortlist"
        reasoning.append("Excellent ATS score")
        reasoning.append("Strong domain alignment")
        reasoning.append("High skill match")
        reasoning.append("Relevant experience")

    # --------------------------
    # HIRE / CONSIDER
    # --------------------------
    elif (
        score >= 60 and
        matched_skills_count >= 3 and
        confidence in ["Medium Match", "High Match"]
    ):
        recommendation = "Hire / Consider"
        action = "Proceed to Interview"
        reasoning.append("Good overall ATS score")
        reasoning.append("Adequate skill alignment")
        if domain_match:
            reasoning.append("Domain aligned")
        if certifications:
            reasoning.append("Relevant certifications present")

    # --------------------------
    # HOLD
    # --------------------------
    elif (
        score >= 40 and
        matched_skills_count >= 1
    ):
        recommendation = "Hold"
        action = "Keep for Future Roles"
        reasoning.append("Partial skill match")
        reasoning.append("Moderate ATS score")
        if not domain_match:
            reasoning.append("Domain mismatch")

    # --------------------------
    # REJECT
    # --------------------------
    else:
        recommendation = "Reject"
        action = "Do Not Proceed"
        reasoning.append("Low ATS score")
        reasoning.append("Insufficient skill match")
        if not domain_match:
            reasoning.append("Domain mismatch")

    return {
        "recommendation": recommendation,
        "action": action,
        "reasoning": reasoning
    }
