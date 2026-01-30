import logging
from typing import Any, Awaitable, Callable
from faststream.kafka import KafkaBroker, KafkaMessage
from .deserializer import Deserializer

logger = logging.getLogger(__name__)


class KafkaConsumer:
    def __init__(
        self,
        broker: KafkaBroker,
        deserializer: Deserializer,
        topic_handler_map: dict[str, Callable[[Any], Awaitable[Any]]],
        auto_offset_reset: str = "earliest",
    ):
        self.broker = broker
        self._deserializer = deserializer
        self._auto_offset_reset = auto_offset_reset
        self._dlq_suffix = "-dlq"
        self._topic_handler_map = topic_handler_map

    def subscribe_to_topics(self, enable_dlq: bool = False) -> None:
        async def process_message(message: KafkaMessage):
            msg_data = message.body
            topic = message.raw_message.topic  # type: ignore

            try:
                handler = self._topic_handler_map.get(topic)  # type: ignore
                if handler:
                    await handler(self._deserializer.deserialize(data=msg_data))
                    await message.ack()
                else:
                    logger.warning("No handler for topic: %s", topic)  # type: ignore

            except Exception as e:
                logger.error("Error processing message: %s", e)

                if enable_dlq:
                    dlq_topic = f"{topic}{self._dlq_suffix}"
                    await self.broker.publish(msg_data, dlq_topic)

                await message.ack()

        for topic, _ in self._topic_handler_map.items():
            self.broker.subscriber(
                topic,
                auto_offset_reset=self._auto_offset_reset,  # type: ignore[literal]
                ack_policy="manual",  # type: ignore[literal]
                group_id="testing",
            )(process_message)
            logger.info(f"Subscribed to topic: {topic}")
