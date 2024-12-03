from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from opentelemetry.instrumentation.aiokafka import AIOKafkaInstrumentor


class KafkaManager:
    def __init__(self, bootstrap_servers: str, instrumented: bool = False):
        if not instrumented:
            AIOKafkaInstrumentor().instrument()
        self.bootstrap_servers = bootstrap_servers

    async def get_producer(self):
        producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            max_request_size=104857600,
            max_batch_size=104857600,
        )
        await producer.start()
        return producer

    async def get_consumer(self, topic: list, group_id: str):
        consumer = AIOKafkaConsumer(
            *topic,  # Unpacking list into multiple arguments
            group_id=group_id,
            bootstrap_servers=self.bootstrap_servers,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            max_partition_fetch_bytes=209715200
        )
        await consumer.start()
        return consumer
