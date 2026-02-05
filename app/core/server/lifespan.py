from typing import AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.infastructure.database.db_helper import create_db_helper
from app.infastructure.kafka.kafka_broker import create_kafka_broker
from app.api.kafka_demo.kafka_demo_consumer import register_kafka_demo_consumers


@asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    db_helper = create_db_helper()
    broker = create_kafka_broker()

    app.state.db_helper = db_helper
    app.state.broker = broker
    await db_helper.create_tables()
    register_kafka_demo_consumers(broker=broker)
    await broker.start()
    yield
    # await db_helper.drop_tables()
    await broker.stop()
    # await db_helper.dispose()
