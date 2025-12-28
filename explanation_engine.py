# explanation_engine.py

def generate_explanation(resume_name, matched_skills, missing_skills, final_score):
    explanation = f"Resume **{resume_name}** scored **{round(final_score,2)}%**.\n"
    if matched_skills:
        explanation += f"✅ Strong match in skills: {', '.join(matched_skills)}.\n"
    if missing_skills:
        explanation += f"⚠️ Missing key skills: {', '.join(missing_skills)}.\n"
    if not matched_skills and not missing_skills:
        explanation += "No specific skills matched the JD.\n"
    return explanation
