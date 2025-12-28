def generate_candidate_feedback(
    matched_skills,
    missing_skills,
    final_score,
    confidence_level
):
    feedback = ""

    # Overall assessment
    if final_score >= 75:
        feedback += "✅ Your resume is a strong match for this job.\n"
    elif final_score >= 50:
        feedback += "⚠️ Your resume partially matches the job requirements.\n"
    else:
        feedback += "❌ Your resume does not sufficiently match the job requirements.\n"

    # Skill feedback
    if missing_skills:
        feedback += "\n🔧 Skills to Improve:\n"
        for skill in missing_skills:
            feedback += f"- Learn or strengthen **{skill}**\n"

    if matched_skills:
        feedback += "\n💪 Your Strengths:\n"
        for skill in matched_skills:
            feedback += f"- {skill}\n"

    # Guidance
    feedback += "\n📈 Improvement Suggestions:\n"
    feedback += "- Add measurable project experience\n"
    feedback += "- Highlight tools & certifications\n"
    feedback += "- Align resume keywords with job description\n"

    return feedback
