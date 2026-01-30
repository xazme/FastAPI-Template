import logging
from typing import Any
from faststream.kafka import KafkaBroker
from .serializer import Serializer

logger = logging.getLogger(__name__)


class KafkaProducer:
    def __init__(
        self,
        broker: KafkaBroker,
        serializer: Serializer,
    ):
        self.broker = broker
        self._serializer = serializer

    async def send(
        self,
        message: Any,
        topic: str,
        key: str | bytes | None = None,
    ) -> None:
        try:
            await self.broker.publish(
                topic=topic,
                key=self._serializer.serialize_key(key=key),
                message=self._serializer.serialize(data=message),
            )
            logger.info(f"Message sent to topic '{topic}': {message}")
        except Exception as e:
            logger.error(f"Failed to send message to {topic}: {e}")
            raise

    async def send_batch(
        self,
        messages: list[Any],
        topic: str,
    ) -> None:
        for msg in messages:
            await self.send(msg, topic)
        logger.info(f"Sent batch of {len(messages)} messages to {topic}")
