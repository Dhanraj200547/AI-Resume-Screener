import os
import subprocess
import time
import requests
import streamlit as st

# Launch FastAPI backend
subprocess.Popen(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"])
time.sleep(3)

API_URL = "http://localhost:8000/analyze/"

def analyze_resume(resume_file, jd_file):
    if resume_file is None or jd_file is None:
        return "Please upload both files.", None, None

    files = {
        "resume": ("resume.pdf", resume_file.read(), "application/pdf"),
        "jd": ("jd.pdf", jd_file.read(), "application/pdf")
    }

    try:
        response = requests.post(API_URL, files=files)
        if response.status_code == 200:
            result = response.json()
            match_score = f"{result['match']}%"
            ats_score = f"{result['score']}%"
            summary = result["summary"]
            return f"Match Score: {match_score}", ats_score, summary
        else:
            return "Error: Could not analyze resume.", "", ""
    except Exception as e:
        return f"Exception: {str(e)}", "", ""

# Streamlit UI
st.title("AI Resume Screener")
resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])

if resume and jd:
    with st.spinner("Analyzing..."):
        match, ats, summary = analyze_resume(resume, jd)
        st.success(match)
        st.info(ats)
        st.json(summary)
