from typing import Annotated
from fastapi import APIRouter, Body, status
from .kafka_demo_dependencies import KafkaProducerDep

router = APIRouter()


@router.post(
    path="/kafka-sent-event",
    status_code=status.HTTP_201_CREATED,
)
async def send_message(
    msg: Annotated[str, Body],
    topic: Annotated[str, Body],
    producer: KafkaProducerDep,
):
    await producer.send(message=msg, topic=topic)
    return {"msg": "zaebis"}
