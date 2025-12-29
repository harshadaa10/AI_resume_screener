import os

from resume_parser import extract_resume_text, clean_resume_text
from ai_engine import get_embedding
from similarity_engine import calculate_similarity
from skill_engine import extract_skills
from jd_skill_engine import evaluate_jd_skills
from experience_engine import experience_score
from certification_engine import certification_score
from confidence_engine import confidence_level
from domain_engine import detect_domain
from domain_penalty_engine import calculate_domain_penalty
from feedback_engine import generate_candidate_feedback
from recommendation_engine import hiring_recommendation



def rank_resumes(resume_folder, jd_text, mode="test", weights=None):
    """
    Rank resumes in a folder against a Job Description.

    mode:
        test   -> resumes deleted after ranking
        stored -> permanent dataset

    weights:
        dict with keys: skill, experience, cert, domain_penalty
    """

    # --------------------------
    # Default weights
    # --------------------------
    if weights is None:
        weights = {
            "skill": 1.0,
            "experience": 1.0,
            "cert": 1.0,
            "domain_penalty": 1.0
        }

    results = []

    print("JD TEXT LENGTH:", len(jd_text))

    # --------------------------
    # JD Intelligence
    # --------------------------
    jd_embedding = get_embedding(jd_text)
    jd_domain = detect_domain(jd_text)
    jd_skills = extract_skills(jd_text)

    print("📌 JD Domain Detected:", jd_domain)

    # --------------------------
    # Process resumes
    # --------------------------
    for resume_file in os.listdir(resume_folder):
        if not resume_file.lower().endswith(".pdf"):
            continue

        resume_path = os.path.join(resume_folder, resume_file)

        try:
            # --------------------------
            # Resume parsing
            # --------------------------
            raw_text = extract_resume_text(resume_path)
            resume_text = clean_resume_text(raw_text)

            if not resume_text.strip():
                continue

            # --------------------------
            # Embeddings & similarity
            # --------------------------
            resume_embedding = get_embedding(resume_text)
            similarity = calculate_similarity(resume_embedding, jd_embedding)
            similarity = max(similarity, 0)

            # --------------------------
            # Domain detection
            # --------------------------
            resume_domain = detect_domain(resume_text)
            domain_penalty, penalty_reason = calculate_domain_penalty(
                jd_domain, resume_domain
            )

            # --------------------------
            # Skill matching
            # --------------------------
            skill_boost, matched_skills, missing_skills = evaluate_jd_skills(
                jd_text, resume_text
            )

            # --------------------------
            # Experience scoring
            # --------------------------
            exp_boost, years_exp = experience_score(jd_text, resume_text)

            # --------------------------
            # Certification scoring
            # --------------------------
            cert_boost, certifications = certification_score(jd_text, resume_text)

            # --------------------------
            # Final score calculation
            # --------------------------
            final_score = (
                similarity * 100
                + (skill_boost * weights["skill"])
                + (exp_boost * weights["experience"])
                + (cert_boost * weights["cert"])
                - (abs(domain_penalty) * weights["domain_penalty"])
            )

            final_score = round(max(final_score, 0), 2)

            # --------------------------
            # Confidence & feedback
            # --------------------------
            confidence = confidence_level(final_score)

            feedback = generate_candidate_feedback(
                matched_skills,
                missing_skills,
                final_score,
                confidence
            )
            # 🔹 Hiring Recommendation
            recommendation_data = hiring_recommendation({
                       "final_score": final_score,
                       "confidence": confidence,
                       "resume_domain": resume_domain,
                       "jd_domain": jd_domain,
                       "matched_skills": matched_skills,
                       "experience_years": years_exp,
                       "certifications": certifications
   })

            # --------------------------
            # Store result
            # --------------------------
            results.append({
                "resume": resume_file,
                "base_score": round(similarity * 100, 2),
                "final_score": final_score,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "confidence": confidence,
                "resume_domain": resume_domain,
                "jd_domain": jd_domain,
                "domain_penalty": domain_penalty,
                "domain_penalty_reason": penalty_reason,
                "experience_years": years_exp,
                "experience_boost": exp_boost,
                "certifications": certifications,
                "certification_boost": cert_boost,
                "feedback": feedback,
                "recommendation": recommendation_data["recommendation"],
                "recommended_action": recommendation_data["action"],
                "recommendation_reasoning": recommendation_data["reasoning"],

            })

        finally:
            # --------------------------
            # Delete test resumes
            # --------------------------
            if mode == "test":
                try:
                    os.remove(resume_path)
                except:
                    pass

    # --------------------------
    # Sort by final score
    # --------------------------
    results.sort(key=lambda x: x["final_score"], reverse=True)
    return results
