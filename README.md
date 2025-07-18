```markdown
# ⚡ AI Resume Screener – Streamlit + FastAPI App on Google Cloud Run

An end-to-end application that uses **Streamlit** as the frontend and **FastAPI** as the backend to screen resumes against job descriptions. It is containerized using **Docker** and deployed to **Google Cloud Run** for scalable and serverless deployment.

---

## 📸 Live App

👉 [Launch the App](https://ai-resume-screener-885446706784.europe-west1.run.app)

---

## 🧠 Features

- 📝 Upload resumes (PDF)
- 📄 Upload Job Descriptions (PDF)
- 🧠 Smart matching using spaCy
- 🎯 Streamlit UI for interaction
- ⚙️ FastAPI for backend logic (text extraction, similarity scoring)
- 🚀 Deployed on Google Cloud Run

---

## 🗂️ Project Structure

```

📦 AI-Resume-Screener
├── app/
│   ├── JDMatcher.py
│   ├── Scorer.py
│   ├── TextExtractor.py
|   ├── Summarize.py
|   └── main.py      # FastAPI app
├── frontend/
|   ├── streamlit_app.py     # Streamlit frontend
├── requirements.txt
├── Dockerfile
└── README.md

````

---

## 🚀 Run Locally

### 1. Clone the Repo

```bash
git clone https://github.com/Dhanraj200547/AI-Resume-Screener.git
cd AI-Resume-Screener
````

### 2. Create a Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Run Both Servers (Locally)

```bash
# In one terminal
uvicorn main:app --reload --port 8000

# In another terminal
streamlit run streamlit_app.py
```

---

## 📦 Docker Deployment

### Dockerfile

```dockerfile
# Base Image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Expose ports
EXPOSE 7860

# Run FastAPI & Streamlit using a script
CMD ["bash", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & sleep 3 && streamlit run frontend/streamlit_app.py --server.port 7860 --server.address 0.0.0.0"]

---

## ✅ Requirements

python-multipart
scikit-learn
fastapi
uvicorn
streamlit
requests
PyMuPDF
spacy

---

## 🛡️ Tips for Optimization

* Use Streamlit ≥ 1.19 to reduce health check load
* Minimize Docker image size (`slim` base)
* Set `min_instances=0` on Cloud Run to reduce cost
* Secure backend endpoints (e.g. with API keys or auth later)

---

## 🧠 Future Enhancements

* ✨ AI-based resume ranking
* 📧 Email shortlisted candidates
* 🧑‍💼 Employer login dashboard
* 📊 Analytics and insights

---

## 🙌 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 💬 Contact

Built by [O Dhanraj](https://github.com/Dhanraj200547)
Feel free to reach out on [LinkedIn](www.linkedin.com/in/odeti-dhanraj-2972b3273) or GitHub.

```
