from typing import Annotated
from fastapi import Depends, Request
from faststream.kafka import KafkaBroker


def get_broker(request: Request) -> KafkaBroker:
    return request.app.state.broker


GetKafkaBrokerDep = Annotated[KafkaBroker, Depends(get_broker)]
