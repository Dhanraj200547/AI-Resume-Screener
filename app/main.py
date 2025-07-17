from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.TextExtractor import extract_text_from_pdf
from app.JDMatcher import matcher
from app.Scorer import scorer
from app.Summarize import summarize_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze/")
async def analyze_resume(resume: UploadFile = File(...), jd: UploadFile = File(...)):
    resume_text = await extract_text_from_pdf(resume)
    jd_text = await extract_text_from_pdf(jd)
    
    score = scorer(resume_text, jd_text)
    summary = summarize_text(resume_text)
    match = matcher(resume_text, jd_text)

    return {
        "score": score,
        "summary": summary,  # send full dict
        "match": match
    }
