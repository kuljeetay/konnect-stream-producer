import os

KAFKA_HOST = os.getenv("KAFKA_HOST", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "cdc-events")
EVENTS_FILE_PATH = os.getenv("EVENTS_FILE_PATH", "stream.jsonl")

LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s %(levelname)s %(message)s",
    "handlers": [
        {"class": "logging.StreamHandler", "stream": "ext://sys.stdout"},
        {
            "class": "logging.FileHandler",
            "filename": "producer.log",
            "mode": "a",
        },
    ],
}
