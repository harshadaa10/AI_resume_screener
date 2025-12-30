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
    analytics["score_distribution"] = [float(s) for s in df["final_score"].tolist()]

    # ==========================
    # DOMAIN MATCH STATS
    # ==========================
    analytics["domain_match"] = {
        "Matched": int((df["resume_domain"] == df["jd_domain"]).sum()),
        "Mismatched": int((df["resume_domain"] != df["jd_domain"]).sum())
    }

    # ==========================
    # CONFIDENCE LEVELS
    # ==========================
    analytics["confidence_levels"] = {k: int(v) for k, v in dict(Counter(df["confidence"])).items()}

    # ==========================
    # SKILL ANALYTICS
    # ==========================
    analytics["matched_skills"] = {k: int(v) for k, v in Counter(skill for skills in df["matched_skills"] for skill in skills).items()}
    analytics["missing_skills"] = {k: int(v) for k, v in Counter(skill for skills in df["missing_skills"] for skill in skills).items()}

    # ==========================
    # EXPERIENCE VS SCORE
    # ==========================
    analytics["experience_vs_score"] = [
        {"experience_years": r["experience_years"], "final_score": float(r["final_score"])}
        for r in ranked_results
    ]

    # ==========================
    # RECOMMENDATION ANALYTICS
    # ==========================
    analytics["recommendation_distribution"] = {k: int(v) for k, v in dict(Counter(df["recommendation"])).items()}
    analytics["action_distribution"] = {k: int(v) for k, v in dict(Counter(df["recommended_action"])).items()}

    analytics["recommendation_vs_confidence"] = {
        rec: {conf: int(count) for conf, count in conf_dict.items()}
        for rec, conf_dict in df.groupby(["recommendation", "confidence"]).size().unstack(fill_value=0).to_dict().items()
    }

    analytics["recommendation_vs_domain"] = {
        "Matched": {k: int(v) for k, v in df[df["resume_domain"] == df["jd_domain"]]["recommendation"].value_counts().to_dict().items()},
        "Mismatched": {k: int(v) for k, v in df[df["resume_domain"] != df["jd_domain"]]["recommendation"].value_counts().to_dict().items()}
    }

    analytics["recommendation_vs_score"] = [
        {"recommendation": r["recommendation"], "final_score": float(r["final_score"])}
        for r in ranked_results
    ]

    return analytics
