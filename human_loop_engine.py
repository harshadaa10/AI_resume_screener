# human_loop_engine.py

import json
import os

FEEDBACK_FILE = "recruiter_feedback.json"

def save_feedback(resume_name, ai_score, ai_rec, human_score, human_rec, notes):
    entry = {
        "resume": resume_name,
        "ai_score": ai_score,
        "ai_recommendation": ai_rec,
        "human_score": human_score,
        "human_recommendation": human_rec,
        "notes": notes
    }

    data = []
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            data = json.load(f)

    data.append(entry)

    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f, indent=4)


def analyze_feedback_trends():
    if not os.path.exists(FEEDBACK_FILE):
        return {}

    with open(FEEDBACK_FILE, "r") as f:
        data = json.load(f)

    score_deltas = [d["human_score"] - d["ai_score"] for d in data]

    return {
        "avg_score_adjustment": round(sum(score_deltas) / len(score_deltas), 2),
        "total_overrides": len(data)
    }
