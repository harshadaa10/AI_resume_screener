# confidence_engine.py

def confidence_level(final_score):
    if final_score >= 80:
        return "High Match"
    elif final_score >= 50:
        return "Medium Match"
    else:
        return "Low Match"
