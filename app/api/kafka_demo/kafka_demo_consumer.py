from faststream import AckPolicy
from faststream.kafka import KafkaBroker, KafkaMessage, TopicPartition


def register_kafka_demo_consumers(broker: KafkaBroker):

    kafka_demo_consumer_0_partition = broker.subscriber(
        partitions=[TopicPartition("kafka-demo-topic", 0)],
        ack_policy=AckPolicy.MANUAL,
        auto_offset_reset="earliest",
        group_id="kafka-demo-group",
    )

    kafka_demo_consumer_1_partition = broker.subscriber(
        partitions=[TopicPartition("kafka-demo-topic", 0)],
        ack_policy=AckPolicy.MANUAL,
        auto_offset_reset="earliest",
        group_id="kafka-demo-group",
    )

    @kafka_demo_consumer_0_partition
    async def handle_demo_message_from_0_partition(msg: KafkaMessage):
        print("First Partition Income Message")
        # some business logic
        print(msg)
        await msg.ack()

    @kafka_demo_consumer_1_partition
    async def handle_demo_message_from_1_partition(msg: KafkaMessage):
        print("Second Partition Income Message")
        # some business logic
        print(msg)
        await msg.ack()

    # typechecking bypass
    _, _ = handle_demo_message_from_0_partition, handle_demo_message_from_1_partition
