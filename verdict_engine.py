def recruiter_verdict(final_score):
    if final_score >= 75:
        return "Strong Hire"
    elif final_score >= 50:
        return "Consider"
    elif final_score >= 30:
        return "Weak Match"
    else:
        return "Reject"
