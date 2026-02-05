from typing import Any
from .kafka_demo_producer import KafkaDemoProducer


class KafkaDemoService:
    def __init__(
        self,
        producer: KafkaDemoProducer,
    ) -> None:
        self.producer = producer

    async def create_useless_smth(
        self,
        payload: dict[str, Any],
        key: str | None = None,
        partition: int | None = None,
    ) -> None:
        await self.producer.publish(payload=payload, key=key, partition=partition)
