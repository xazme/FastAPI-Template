from typing import Any
from faststream.kafka import KafkaBroker


class KafkaDemoProducer:
    def __init__(
        self,
        broker: KafkaBroker,
    ) -> None:
        self.producer = broker.publisher(topic="kafka-demo-topic")

    async def publish(
        self,
        payload: dict[str, Any],
        key: str | None = None,
        partition: int | None = None,
    ) -> None:
        await self.producer.publish(
            message=payload,
            key=b"key" if isinstance(key, str) else key,
            partition=partition,
        )
