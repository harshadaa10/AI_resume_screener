import os

from resume_parser import extract_resume_text, clean_resume_text
from ai_engine import get_embedding
from similarity_engine import calculate_similarity
from jd_skill_engine import evaluate_jd_skills
from experience_engine import experience_score
from certification_engine import certification_score
from confidence_engine import confidence_level
from domain_engine import detect_domain
from domain_penalty_engine import calculate_domain_penalty
from feedback_engine import generate_candidate_feedback
from recommendation_engine import hiring_recommendation
from bias_engine import analyze_bias
from explanation_engine import generate_explainability

try:
    from resume_fraud_engine import detect_resume_fraud
except:
    detect_resume_fraud = None

try:
    from bias_engine import neutralize_bias_factors
except:
    neutralize_bias_factors = None


def rank_resumes(resume_folder, jd_text, mode="test", weights=None):

    if weights is None:
        weights = {
            "skill": 1.0,
            "experience": 1.0,
            "cert": 1.0,
            "domain_penalty": 1.0
        }

    results = []

    jd_embedding = get_embedding(jd_text)
    jd_domain = detect_domain(jd_text)

    for resume_file in os.listdir(resume_folder):

        if not resume_file.lower().endswith((".pdf", ".txt")):
            continue

        resume_path = os.path.join(resume_folder, resume_file)

        try:
            raw_text = extract_resume_text(resume_path)
            resume_text = clean_resume_text(raw_text)

            if not resume_text.strip():
                continue

            if neutralize_bias_factors:
                resume_text = neutralize_bias_factors(resume_text)

            resume_embedding = get_embedding(resume_text)
            similarity = max(calculate_similarity(resume_embedding, jd_embedding), 0)

            resume_domain = detect_domain(resume_text)
            domain_penalty, penalty_reason = calculate_domain_penalty(
                jd_domain, resume_domain
            )

            skill_boost, matched_skills, missing_skills = evaluate_jd_skills(
                jd_text, resume_text
            )

            exp_boost, years_exp = experience_score(jd_text, resume_text)
            cert_boost, certifications = certification_score(jd_text, resume_text)

            final_score = (
                similarity * 100
                + skill_boost * weights["skill"]
                + exp_boost * weights["experience"]
                + cert_boost * weights["cert"]
                - abs(domain_penalty) * weights["domain_penalty"]
            )

            fraud_score = 0
            fraud_flags = []

            if detect_resume_fraud:
                fraud_result = detect_resume_fraud(resume_text, jd_text)
                fraud_score = fraud_result.get("penalty", 0)
                fraud_flags = fraud_result.get("flags", [])

            final_score = round(max(final_score - fraud_score, 0), 2)

            if mode == "test" and final_score <= 0:
                final_score = 10

            confidence = confidence_level(final_score)

            feedback = generate_candidate_feedback(
                matched_skills,
                missing_skills,
                final_score,
                confidence
            )

            recommendation_data = hiring_recommendation({
                "final_score": final_score,
                "confidence": confidence,
                "resume_domain": resume_domain,
                "jd_domain": jd_domain,
                "matched_skills": matched_skills,
                "experience_years": years_exp,
                "certifications": certifications
            })

            bias_result = analyze_bias(resume_text)
            bias_flags = bias_result.get("bias_flags", [])

            explainability = generate_explainability({
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "experience_years": years_exp,
                "resume_domain": resume_domain,
                "jd_domain": jd_domain,
                "certifications": certifications,
                "final_score": final_score,
                "bias_flags": bias_flags,
                "fraud_flags": fraud_flags
            })

            results.append({
                "resume": resume_file,
                "base_score": round(similarity * 100, 2),
                "final_score": final_score,
                "verdict": explainability["verdict"],  # ✅ FIX
                "confidence": confidence,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "resume_domain": resume_domain,
                "jd_domain": jd_domain,
                "domain_penalty": domain_penalty,
                "domain_penalty_reason": penalty_reason,
                "experience_years": years_exp,
                "experience_boost": exp_boost,
                "certifications": certifications,
                "certification_boost": cert_boost,
                "fraud_penalty": fraud_score,
                "fraud_flags": fraud_flags,
                "feedback": feedback,
                "recommendation": recommendation_data["recommendation"],
                "recommended_action": recommendation_data["action"],
                "recommendation_reasoning": recommendation_data["reasoning"],
                "bias_flags": bias_flags,
                "explainability": explainability
            })

        finally:
            if mode == "prod":
                try:
                    os.remove(resume_path)
                except:
                    pass

    results.sort(key=lambda x: x["final_score"], reverse=True)
    return results
