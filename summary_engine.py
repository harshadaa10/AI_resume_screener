def generate_summary(results):
    summary = {}

    total = len(results)
    if total == 0:
        return {
            "total_resumes": 0,
            "average_score": 0,
            "best_candidate": None,
            "consider_count": 0,
            "reject_count": 0
        }

    avg_score = round(
        sum(r["final_score"] for r in results) / total, 2
    )

    best_candidate = results[0]["resume"]

    consider_count = len([r for r in results if r["final_score"] >= 60])
    reject_count = total - consider_count

    summary["total_resumes"] = total
    summary["average_score"] = avg_score
    summary["best_candidate"] = best_candidate
    summary["consider_count"] = consider_count
    summary["reject_count"] = reject_count

    return summary
