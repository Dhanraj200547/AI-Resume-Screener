import spacy
nlp = spacy.load("en_core_web_sm")

SKILL_KEYWORDS = [
    "python", "java", "sql", "tensorflow", "keras", "pytorch",
    "docker", "firebase", "nlp", "streamlit", "ml", "react"
]

def summarize_text(text):
    doc = nlp(text.lower())
    summary = {
        "skills": [],
        "education": [],
        "experience": []
    }

    for token in doc:
        if token.text in SKILL_KEYWORDS and token.text not in summary["skills"]:
            summary["skills"].append(token.text)

    for sent in doc.sents:
        if any(word in sent.text for word in ["education", "bachelor", "university", "college"]):
            summary["education"].append(sent.text.strip())

    for sent in doc.sents:
        if any(word in sent.text for word in ["experience", "developer", "intern"]):
            summary["experience"].append(sent.text.strip())

    return summary
