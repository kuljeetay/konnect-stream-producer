FROM python:3.9-slim

ENV KAFKA_TOPIC="cdc-events"
ENV KAFKA_HOST="kafka:29092"
ENV EVENTS_FILE_PATH="stream.jsonl"
ENV POLL_FREQ = "5"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "src/producer/main.py"]