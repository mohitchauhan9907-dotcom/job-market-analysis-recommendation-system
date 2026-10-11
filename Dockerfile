# Job Market Analysis & Recommendation System
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ ./templates/
COPY dashboard_data/ ./dashboard_data/
COPY job_market_model/ ./job_market_model/

EXPOSE 5000

CMD ["python", "app.py"]
