# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY travel_planner.py .
COPY config.yaml .

RUN mkdir -p /app/output

CMD ["python", "travel_planner.py", "--help"]

