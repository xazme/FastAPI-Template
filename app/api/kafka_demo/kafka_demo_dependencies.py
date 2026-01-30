from typing import Annotated
from fastapi import Depends, Request
from app.infastructure.kafka.kafka_producer import KafkaProducer


def get_kafka_producer(request: Request) -> KafkaProducer:
    return request.app.state.producer


KafkaProducerDep = Annotated[KafkaProducer, Depends(get_kafka_producer)]
