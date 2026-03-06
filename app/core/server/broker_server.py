from faststream.kafka import KafkaBroker

from app.api import init_consumers
from app.core.ioc import init_faststream_ioc


def create_faststream(broker: KafkaBroker):
    init_faststream_ioc(broker=broker)
    init_consumers(broker=broker)
