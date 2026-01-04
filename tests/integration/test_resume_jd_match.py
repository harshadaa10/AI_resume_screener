from resume_jd_match_engine import calculate_resume_jd_match

def test_resume_matches_jd():
    # Mock or sample data for testing
    jd_text = """
We are looking for a Python Developer with 5+ years of experience.
Required skills: Python, Django, PostgreSQL, REST APIs, Git.
Must have: Machine Learning experience.
"""

    resume_text = """
Experienced Python Developer with expertise in Django and Flask.
Skills: Python, Django, PostgreSQL, REST APIs, Git, Docker.
Background in web development and backend systems.
"""

    # Now call the function
    result = calculate_resume_jd_match(jd_text, resume_text)
    print(result)

    assert result["match_score"] >= 40

