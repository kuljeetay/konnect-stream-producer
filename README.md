# Konnect Stream Producer

This repository implements a Kafka producer for CDC (Change Data Capture) events. The producer reads CDC events from a JSONL file every 5 seconds (adjustable using POLL_FREQ Environment Variable) and publishes them to Kafka topic.

## Prerequisites

- Docker and Docker Compose installed.
- Konnect Stream Processor Consumer should be up in order to consume these events, refer to this github repo for details [Konnect Stream Processor Consumer](https://github.com/kuljeetay/konnect-stream-processor.git).

## Setup

### 1. Clone the Repository.
```sh
git clone https://github.com/kuljeetay/konnect-stream-producer.git
cd konnect-stream-producer
```


### 2. Build and Run with Docker Compose.

To build and start the services defined in docker-compose.yml, run:
```sh
docker-compose up -d
```

## Configuration

Configuration for Kafka, Poll Freq, File path is managed through environment variables in the dockerfile:

    KAFKA_TOPIC: The Kafka topic to produce to (default: cdc-events).
    KAFKA_HOST: The Kafka broker address (default: kafka:29092).
    EVENTS_FILE_PATH: Path to Jsonl File to be read.
    POLL_FREQ: Time to poll the file for changes in seconds (default: 5)

These can be adjusted as needed.

## Running the Application

After starting the services with Docker Compose, the *konnect-stream-producer* container will come up and start producing events from the specified JSONL File. Application logs can be seen using docker logs -f konnect-stream-producer container