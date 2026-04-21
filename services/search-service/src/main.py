import os
from fastapi import FastAPI, Query, HTTPException, APIRouter
from elasticsearch import AsyncElasticsearch, NotFoundError
from .worker import start_search_worker
from contextlib import asynccontextmanager
import asyncio
from fastapi.middleware.cors import CORSMiddleware

ES_URL = os.environ.get("ELASTICSEARCH_URL", "http://elasticsearch:9200")

es = AsyncElasticsearch(ES_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    task = loop.create_task(start_search_worker())
    yield
    task.cancel()
    await es.close()


app = FastAPI(title="Fast Queue - Search Service", lifespan=lifespan)
api_router = APIRouter(prefix="/v1/search", redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://fastq.site", "https://fast-queue-493301.web.app", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"], # Use "*" nos headers para evitar erros de preflight
)

@api_router.get("")
async def search(q: str = Query(..., min_length=2)):
    print(f"🔎 [SEARCH] Recebendo busca para o termo: {q}")
    query = {
        "query": {
            "multi_match": {
                "query": q,
                "fields": ["display_name^3", "queue_title"],
                "fuzziness": "AUTO",
            }
        }
    }

    try:
        response = await es.search(index="streamers", body=query)

        results = [hit["_source"] for hit in response["hits"]["hits"]]

        return {"total": len(results), "results": results}
    except NotFoundError:
        return {"total": 0, "results": []}


app.include_router(api_router)
