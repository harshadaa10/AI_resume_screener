import pandas as pd
from collections import Counter

def generate_ats_analytics(ranked_results):
    if not ranked_results:
        return {}

    df = pd.DataFrame(ranked_results)

    analytics = {}

    # ==========================
    # SCORE DISTRIBUTION
    # ==========================
    analytics["score_distribution"] = df["final_score"].tolist()

    # ==========================
    # DOMAIN MATCH STATS
    # ==========================
    analytics["domain_match"] = {
        "Matched": (df["resume_domain"] == df["jd_domain"]).sum(),
        "Mismatched": (df["resume_domain"] != df["jd_domain"]).sum()
    }

    # ==========================
    # CONFIDENCE LEVELS
    # ==========================
    analytics["confidence_levels"] = dict(
        Counter(df["confidence"])
    )

    # ==========================
    # SKILL ANALYTICS
    # ==========================
    analytics["matched_skills"] = Counter(
        skill for skills in df["matched_skills"] for skill in skills
    )

    analytics["missing_skills"] = Counter(
        skill for skills in df["missing_skills"] for skill in skills
    )

    # ==========================
    # EXPERIENCE VS SCORE
    # ==========================
    analytics["experience_vs_score"] = df[
        ["experience_years", "final_score"]
    ].to_dict(orient="records")

    # ==========================
    # 🧠 RECOMMENDATION ANALYTICS (NEW)
    # ==========================
    analytics["recommendation_distribution"] = dict(
        Counter(df["recommendation"])
    )

    analytics["action_distribution"] = dict(
        Counter(df["recommended_action"])
    )

    analytics["recommendation_vs_confidence"] = (
        df.groupby(["recommendation", "confidence"])
        .size()
        .unstack(fill_value=0)
        .to_dict()
    )

    analytics["recommendation_vs_domain"] = {
        "Matched": df[df["resume_domain"] == df["jd_domain"]]["recommendation"].value_counts().to_dict(),
        "Mismatched": df[df["resume_domain"] != df["jd_domain"]]["recommendation"].value_counts().to_dict()
    }

    analytics["recommendation_vs_score"] = df[
        ["recommendation", "final_score"]
    ].to_dict(orient="records")

    return analytics
