from fastapi import FastAPI
from faststream.kafka import KafkaBroker
from app.core.config import settings
from app.infastructure.database.db_helper import DataBaseHelper
from app.infastructure.kafka.kafka_producer import KafkaProducer, Serializer
from app.infastructure.kafka.kafka_consumer import KafkaConsumer, Deserializer
from app.core.consumer_handlers.consumer_handler import consumer_handler


async def init_db(app: FastAPI) -> DataBaseHelper:
    db_helper = DataBaseHelper(
        db_url=settings.postgres_connection,
        echo=True,
    )
    app.state.db_helper = db_helper
    return db_helper


async def init_kafka(app: FastAPI) -> KafkaBroker:
    broker = KafkaBroker(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        enable_idempotence=True,
    )

    producer = KafkaProducer(broker=broker, serializer=Serializer())
    consumer = KafkaConsumer(
        broker=broker,
        deserializer=Deserializer(),
        topic_handler_map={"aboba": consumer_handler},
    )
    consumer.subscribe_to_topics(enable_dlq=True)

    app.state.broker = broker
    app.state.producer = producer
    app.state.consumer = consumer
    return broker
