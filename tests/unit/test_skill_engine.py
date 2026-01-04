from skill_engine import extract_skills

def test_skill_extraction_basic():
    text = "Experienced in Python, Machine Learning and AWS"
    skills = extract_skills(text)

    assert "python" in skills
    assert "machine learning" in skills
    assert "aws" in skills
