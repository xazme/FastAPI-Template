from typing import Annotated
from fastapi import APIRouter, Body, status
from .kafka_demo_dependencies import KafkaDemoServiceDep

router = APIRouter()


@router.post(
    path="/kafka-sent-event",
    status_code=status.HTTP_201_CREATED,
)
async def send_message(
    msg: Annotated[str, Body],
    kafka_demo_service: KafkaDemoServiceDep,
):
    await kafka_demo_service.create_useless_smth(payload={"msg": msg})
    return {"msg": "zaebis"}
