import json
import os
import logging
import time
from typing import List, Dict, Any
from confluent_kafka import Producer


class KonnectStreamProducer:
    def __init__(self, config: str, topic: str):
        self.config = config
        self.topic = topic
        self.last_position = 0
        self.producer = self.create_producer()

    def create_producer(self) -> Producer:
        """
        Creates and returns a Kafka producer.
        :return: Producer: The Kafka producer instance.
        """
        return Producer({"bootstrap.servers": self.config})

    def delivery_callback(self, err, msg):
        """
        Callback method for logging error/delivery of the message.
        :param: err: The error that occurred on delivery or None on success.
        :param: msg: The message that was produced.
        """
        if err is not None:
            logging.error(f"Failed to deliver message: {err}")
        else:
            logging.info(
                f"Message delivered to topic: {msg.topic()} message: {msg.key()}"
            )

    def read_events(self, file: str) -> List[Dict[str, Any]]:
        """
        Reads new CDC events from given JSONL file.

        :param: jsonl_file: The path to the JSONL file containing CDC events.
        :returns: A list of new CDC events read from the file.
        """
        events = []
        try:
            with open(file, "r") as file:
                file.seek(self.last_position)
                for line in file:
                    event = json.loads(line)
                    events.append(event)
                self.last_position = file.tell()
            return events
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
        except Exception as e:
            logging.error(
                f"An unexpected error occurred while reading events: {e}"
            )

    def produce_events(self, events: List[Dict[str, Any]]):
        """
        Produces CDC events to a Kafka topic.
        :param: events: List of CDC events to be produced.
        Bench-Test: takes 0.3ms roughly to produce one msg
        """
        try:
            for event in events:
                key = event["after"]["key"]
                value = json.dumps(event)
                self.producer.produce(
                    self.topic,
                    key=key,
                    value=value,
                    callback=self.delivery_callback,
                )
                self.producer.poll(0)
            self.producer.flush()
        except Exception as e:
            logging.error(
                f"An unexpected error occurred while producing events: {e}"
            )

    def run(self, file):
        """
        Continuously reads new events from a JSONL file and produces
        them to a Kafka topic every 5 seconds.
        :param: file: The path to the JSONL file containing CDC events.
        """
        while True:
            events = self.read_events(file)
            if events:
                self.produce_events(events)
            time.sleep(os.getenv("POLL_FREQ", 5))
