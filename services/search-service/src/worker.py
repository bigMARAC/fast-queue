import json
import os
from aiokafka import AIOKafkaConsumer
from elasticsearch import AsyncElasticsearch, NotFoundError

KAFKA_TOPIC = "dbserver1.public.queues"
KAFKA_SERVER = os.environ.get("KAFKA_SERVER", "kafka:9092")
ES_URL = os.environ.get("ELASTICSEARCH_URL", "http://elasticsearch:9200")

async def process_event(msg_value: dict, es_client: AsyncElasticsearch):
    payload = msg_value.get("payload", {})
    op = payload.get("op")
    after = payload.get("after")
    before = payload.get("before")

    # 1. CREATE ou UPDATE
    if op in ("c", "u"):
        queue_id = str(after.get("id"))
        await es_client.index(
            index="streamers",
            id=queue_id,
            document={
                "queue_id": after.get("id"),
                "queue_title": after.get("title"),
                "streamer_id": after.get("streamer_id"),
                "display_name": after.get("streamer_name"),
                "is_live": after.get("status") == "OPEN",
                "entry_fee": after.get("entry_fee"),
                "updated_at": payload.get("source", {}).get("ts_ms")
            }
        )
        print(f"🔎 [CDC] Fila {queue_id} sincronizada via Debezium (op: {op})")

    # 2. DELETE
    elif op == "d":
        queue_id = str(before.get("id"))
        try:
            await es_client.delete(index="streamers", id=queue_id)
            print(f"🗑️ [CDC] Fila {queue_id} removida da busca.")
        except NotFoundError:
            pass

async def start_search_worker():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC, # Ouvindo o tópico do Debezium
        bootstrap_servers=KAFKA_SERVER,
        group_id="search_cdc_group",
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    es = AsyncElasticsearch(ES_URL)
    await consumer.start()
    
    try:
        async for msg in consumer:
            if msg.value:
                await process_event(msg.value, es)
    finally:
        await consumer.stop()