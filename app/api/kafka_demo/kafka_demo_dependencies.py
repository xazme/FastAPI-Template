from typing import Annotated
from fastapi import Depends
from app.infastructure.kafka import GetKafkaBrokerDep
from .kafka_demo_service import KafkaDemoService
from .kafka_demo_producer import KafkaDemoProducer


def get_kafka_demo_service(broker: GetKafkaBrokerDep):
    producer = KafkaDemoProducer(broker=broker)
    return KafkaDemoService(producer=producer)


KafkaDemoServiceDep = Annotated[KafkaDemoService, Depends(get_kafka_demo_service)]
