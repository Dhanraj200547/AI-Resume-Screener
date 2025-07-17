def scorer(resume_text, Jd_text):
    Resume_keywords = set(resume_text.lower().split())
    Jd_keywords = set(Jd_text.lower().split())
    
    matched = 0
    for word in Resume_keywords:
        if word in Jd_keywords:
            matched += 1

    score = round((matched / len(Jd_keywords)) * 100, 2) if Jd_keywords else 0
    return score