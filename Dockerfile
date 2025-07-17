FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


RUN python -m spacy download en_core_web_sm

# Copy app code

COPY . .

# Run Gradio app, which internally starts FastAPI
CMD ["python", "gradio_ui.py"]
