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
