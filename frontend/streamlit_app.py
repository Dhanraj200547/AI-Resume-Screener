import streamlit as st
import requests

st.title("AI Resume Screener")

resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])

if resume and jd:
    with st.spinner("Analyzing..."):
        response = requests.post(
            "http://127.0.0.1:8000/analyze/",
            files={"resume": resume.getvalue(), "jd": jd.getvalue()},
        )
        if response.ok:
            result = response.json()
            st.success(f"Match Score: {result['match']}%")
            st.info("Summary:")
            st.json(result["summary"])
            st.metric("ATS Score", f"{result['score']}%")
        else:
            st.error("Error in analysis. Check backend logs.")