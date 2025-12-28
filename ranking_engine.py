import os
from resume_parser import extract_resume_text, clean_resume_text
from ai_engine import get_embedding
from similarity_engine import calculate_similarity
from skill_engine import extract_skills
from skill_scoring_v2 import calculate_weighted_score
from feedback_engine import generate_candidate_feedback
from confidence_engine import confidence_level
from domain_engine import detect_domain


def rank_resumes(resume_folder, jd_text, mode="test"):
    """
    Rank resumes in a folder against a job description.
    
    mode:
        "test"   → temporary resumes (auto-delete after ranking)
        "stored" → permanent dataset (do not delete)
    """
    results = []

    print("JD TEXT LENGTH:", len(jd_text))

    # 🔹 JD intelligence
    jd_embedding = get_embedding(jd_text)
    jd_skills = extract_skills(jd_text)
    jd_domain = detect_domain(jd_text)

    print("📌 JD Domain Detected:", jd_domain)

    for resume_file in os.listdir(resume_folder):
        if resume_file.endswith(".pdf"):
            resume_path = os.path.join(resume_folder, resume_file)

            try:
                # Extract & clean resume text
                raw_text = extract_resume_text(resume_path)
                cleaned_text = clean_resume_text(raw_text)

                print(f"{resume_file} text length: {len(cleaned_text)}")

                # Resume intelligence
                resume_embedding = get_embedding(cleaned_text)
                resume_domain = detect_domain(cleaned_text)

                # 🔹 Similarity score
                similarity_score = calculate_similarity(resume_embedding, jd_embedding)
                similarity_score = max(similarity_score, 0)

                # 🔹 Skill analysis
                resume_skills = extract_skills(cleaned_text)
                matched_skills = list(set(resume_skills) & set(jd_skills))
                missing_skills = list(set(jd_skills) - set(resume_skills))

                boost, penalty = calculate_weighted_score(matched_skills, missing_skills)

                # 🔹 Domain penalty
                domain_penalty = 0
                if resume_domain != "Unknown" and jd_domain != "Unknown":
                    if resume_domain != jd_domain:
                        domain_penalty = 15
                elif resume_domain == "Unknown":
                    domain_penalty = 5

                # 🔹 Final score
                final_score = (similarity_score * 100) + boost - penalty - domain_penalty
                final_score = round(max(final_score, 0), 2)

                # 🔹 Confidence & feedback
                confidence = confidence_level(final_score)
                candidate_feedback = generate_candidate_feedback(
                    matched_skills,
                    missing_skills,
                    final_score,
                    confidence
                )

                # Add to results
                results.append({
                    "resume": resume_file,
                    "base_score": round(similarity_score * 100, 2),
                    "boost": boost,
                    "penalty": penalty + domain_penalty,
                    "final_score": final_score,
                    "matched_skills": matched_skills,
                    "missing_skills": missing_skills,
                    "confidence": confidence,
                    "resume_domain": resume_domain,
                    "jd_domain": jd_domain,
                    "feedback": candidate_feedback
                })

            finally:
                # 🧪 DELETE ONLY TEST RESUMES
                if mode == "test":
                    try:
                        os.remove(resume_path)
                    except:
                        pass

    # 🔹 Sort by final ATS score
    results.sort(key=lambda x: x["final_score"], reverse=True)
    return results
