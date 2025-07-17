import os
import asyncio
import uvicorn
import requests
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from app.TextExtractor import extract_text_from_pdf
from app.JDMatcher import matcher
from app.Scorer import scorer
from app.Summarize import summarize_text

import gradio as gr

PORT = int(os.getenv("PORT", 7860))

# === FASTAPI BACKEND ===
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@app.post("/analyze/")
async def analyze_resume(resume: UploadFile = File(...), jd: UploadFile = File(...)):
    resume_text = await extract_text_from_pdf(resume)
    jd_text = await extract_text_from_pdf(jd)
    score = scorer(resume_text, jd_text)
    summary = summarize_text(resume_text)
    match = matcher(resume_text, jd_text)
    return {"score": score, "summary": summary, "match": match}


# === GRADIO FRONTEND ===
def analyze(resume_file, jd_file):
    if resume_file is None or jd_file is None:
        return "Upload both files", "", ""

    files = {
        "resume": ("resume.pdf", resume_file.read(), "application/pdf"),
        "jd": ("jd.pdf", jd_file.read(), "application/pdf")
    }

    try:
        response = requests.post(f"http://127.0.0.1:{PORT}/analyze/", files=files)
        if response.status_code == 200:
            result = response.json()
            return f"{result['match']}%", f"{result['score']}%", result["summary"]
        else:
            return "❌ Failed to analyze", "", ""
    except Exception as e:
        return f"❌ Error: {e}", "", ""

resume_input = gr.File(label="Resume (PDF)", type="binary")
jd_input = gr.File(label="Job Description (PDF)", type="binary")
match_score_output = gr.Textbox(label="Match Score")
ats_score_output = gr.Textbox(label="ATS Score")
summary_output = gr.JSON(label="Summary")

ui = gr.Interface(
    fn=analyze,
    inputs=[resume_input, jd_input],
    outputs=[match_score_output, ats_score_output, summary_output],
    title="AI Resume Screener",
    description="Upload resume + JD to view ATS match % and summary."
)


# === START BOTH FastAPI + Gradio TOGETHER ===
if __name__ == "__main__":
    async def run_all():
        config = uvicorn.Config("app.main:app", host="0.0.0.0", port=PORT)
        server = uvicorn.Server(config)
        await asyncio.gather(
            asyncio.to_thread(ui.launch, server_name="0.0.0.0", server_port=PORT, show_api=False),
            server.serve()
        )

    asyncio.run(run_all())
