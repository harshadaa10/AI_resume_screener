from collections import defaultdict

def analyze_fairness(ranked_results):
    # ---------- DEFAULT SAFE STRUCTURE ----------
    fairness = {
        "acceptance_rate": 0.0,
        "domain_avg_scores": {},
        "experience_avg_scores": {
            "Junior (0-2)": 0,
            "Mid (3-5)": 0,
            "Senior (6+)": 0,
        },
        "top_dominant_skills": {},
        "fairness_flag": "✅ No Major Bias Detected",
    }

    if not ranked_results:
        return fairness

    # ==========================
    # 1️⃣ Acceptance Rate
    # ==========================
    accepted = [
        r for r in ranked_results
        if r.get("recommendation") in ["Hire", "Strong Hire"]
    ]
    fairness["acceptance_rate"] = round(
        (len(accepted) / len(ranked_results)) * 100, 2
    )

    # ==========================
    # 2️⃣ Domain Bias
    # ==========================
    domain_scores = defaultdict(list)
    for r in ranked_results:
        domain_scores[r["resume_domain"]].append(float(r["final_score"]))

    fairness["domain_avg_scores"] = {
        d: round(sum(scores) / len(scores), 2)
        for d, scores in domain_scores.items()
    }

    # ==========================
    # 3️⃣ Experience Bias
    # ==========================
    exp_groups = {"Junior (0-2)": [], "Mid (3-5)": [], "Senior (6+)": []}

    for r in ranked_results:
        y = r["experience_years"]
        if y <= 2:
            exp_groups["Junior (0-2)"].append(float(r["final_score"]))
        elif y <= 5:
            exp_groups["Mid (3-5)"].append(float(r["final_score"]))
        else:
            exp_groups["Senior (6+)"].append(float(r["final_score"]))

    fairness["experience_avg_scores"] = {
        g: round(sum(v) / len(v), 2) if v else 0
        for g, v in exp_groups.items()
    }

    # ==========================
    # 4️⃣ Skill Dominance Bias
    # ==========================
    skill_count = defaultdict(int)
    for r in ranked_results:
        for s in r["matched_skills"]:
            skill_count[s] += 1

    fairness["top_dominant_skills"] = dict(
        sorted(skill_count.items(), key=lambda x: x[1], reverse=True)[:5]
    )

    # ==========================
    # 5️⃣ Fairness Flag
    # ==========================
    if fairness["domain_avg_scores"]:
        max_score = max(fairness["domain_avg_scores"].values())
        min_score = min(fairness["domain_avg_scores"].values())
        if max_score - min_score > 25:
            fairness["fairness_flag"] = "⚠️ Potential Bias Detected"

    return fairness
