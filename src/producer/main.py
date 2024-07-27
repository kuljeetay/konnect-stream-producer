import logging
from utils import configure_logging
from config import KAFKA_HOST, KAFKA_TOPIC, EVENTS_FILE_PATH
from kafka_producer import KonnectStreamProducer


def main():
    try:
        configure_logging()
        producer = KonnectStreamProducer(KAFKA_HOST, KAFKA_TOPIC)
        producer.run(EVENTS_FILE_PATH)
    except Exception as ex:
        logging.exception(str(ex))


if __name__ == "__main__":
    main()
