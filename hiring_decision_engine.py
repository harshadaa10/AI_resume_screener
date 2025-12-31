# hiring_decision_engine.py

def make_hiring_decision(
    skill_score,
    domain_penalty,
    drift_penalty,
    transfer_bonus,
    confidence_score,
    jd_quality_score,
    fraud_result=None
):
    """
    Final hiring decision engine.
    All inputs are numeric and normalized.
    """

    # =========================
    # 1️⃣ Final Score Calculation
    # =========================
    final_score = (
        skill_score
        + transfer_bonus
        + jd_quality_score
        + domain_penalty
        + drift_penalty
    )

    # Confidence acts as multiplier (truth signal)
    final_score *= confidence_score

    # =========================
    # 2️⃣ Decision Thresholds
    # =========================
    if final_score >= 75:
        decision = "SHORTLIST"
        reason = "Strong skill match with acceptable domain alignment"

    elif 55 <= final_score < 75:
        decision = "REVIEW"
        reason = "Moderate fit with transferable skills or domain shift"

    else:
        decision = "REJECT"
        reason = "Insufficient skills or major domain mismatch"

    if fraud_result and isinstance(fraud_result, dict) and fraud_result.get("risk_level") == "HIGH RISK":
        decision = "REJECT"

    # =========================
    # 3️⃣ Explainability Output
    # =========================
    return {
        "final_score": round(final_score, 2),
        "decision": decision,
        "reason": reason
    }
