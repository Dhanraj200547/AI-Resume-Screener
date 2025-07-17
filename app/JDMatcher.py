import spacy

def matcher(text, job_description):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    jd_doc = nlp(job_description)
    
    return round(doc.similarity(jd_doc) * 100, 2)