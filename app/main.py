from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.TextExtractor import extract_text_from_pdf
from app.JDMatcher import matcher
from app.Scorer import scorer
from app.Summarize import summarize_text

import gradio as gr
import asyncio
import uvicorn
import os

app = FastAPI()

# CORS
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
    return {"score": score, "summary": summary, "match": match}

# --- Gradio UI wrapped in function ---
def launch_gradio():
    import requests

    def analyze(resume_file, jd_file):
        if resume_file is None or jd_file is None:
            return "Please upload both files.", None, None

        files = {
            "resume": ("resume.pdf", resume_file.read(), "application/pdf"),
            "jd": ("jd.pdf", jd_file.read(), "application/pdf")
        }

        url = f"http://0.0.0.0:{PORT}/analyze/"
        try:
            response = requests.post(url, files=files)
            if response.status_code == 200:
                result = response.json()
                return f"{result['match']}%", f"{result['score']}%", result['summary']
            else:
                return "Error analyzing resume.", "", ""
        except Exception as e:
            return f"Exception: {str(e)}", "", ""

    resume_input = gr.File(label="Upload Resume (PDF)", type="binary")
    jd_input = gr.File(label="Upload Job Description (PDF)", type="binary")

    match_score_output = gr.Textbox(label="Match Score")
    ats_score_output = gr.Textbox(label="ATS Score")
    summary_output = gr.JSON(label="Resume Summary")

    ui = gr.Interface(
        fn=analyze,
        inputs=[resume_input, jd_input],
        outputs=[match_score_output, ats_score_output, summary_output],
        title="AI Resume Screener",
        description="Upload a resume and JD to get an ATS score and summary.",
    )
    ui.launch(server_name="0.0.0.0", server_port=PORT, show_api=False)

# --- Unified launcher ---
if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 7860))

    # Run FastAPI and Gradio together using asyncio
    async def start():
        config = uvicorn.Config("app.main:app", host="0.0.0.0", port=PORT, log_level="info")
        server = uvicorn.Server(config)
        await asyncio.gather(
            server.serve(),
            asyncio.to_thread(launch_gradio)
        )

    asyncio.run(start())
