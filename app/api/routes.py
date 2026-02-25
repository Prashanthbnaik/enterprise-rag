from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.api.schemas import QueryRequest, QueryResponse
from app.pipeline import rag_pipeline
from app.core.cache import redis_client
from app.ingestion.ingest import ingest_file, ingest_url

import json


router = APIRouter()



# QUERY ENDPOINT
@router.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):

    question = request.question.strip()

    # CACHE CHECK 
    try:
        if redis_client:
            cached = redis_client.get(question)

            if cached:
                cached_data = json.loads(cached)

                # Ensure contexts exists (fix old cache format)
                if "contexts" not in cached_data:
                    cached_data["contexts"] = []

                if "latency" not in cached_data:
                    cached_data["latency"] = 0

                return cached_data

    except Exception:
        pass


    # RUN RAG PIPELINE 
    result = rag_pipeline(question)

    #  SAFE RESPONSE FORMAT 
    response = {
        "answer": result.get("answer", ""),
        "contexts": result.get("contexts", []),
        "latency": result.get("latency", 0)
    }


    # SAVE CACHE 
    try:
        if redis_client:
            redis_client.setex(
                question,
                3600,  # 1 hour cache
                json.dumps(response)
            )

    except Exception:
        pass


    return response




# FILE / URL INGESTION
@router.post("/upload")
async def upload(
    file: UploadFile = File(None),
    url: str = Form(None)
):

    try:

        if file is not None:

            count = ingest_file(file)

            return {
                "status": "file indexed",
                "chunks": count
            }


        if url is not None:

            count = ingest_url(url)

            return {
                "status": "url indexed",
                "chunks": count
            }


        raise HTTPException(
            status_code=400,
            detail="Provide file or url"
        )


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )



# HEALTH CHECK
@router.get("/health")
def health():

    return {
        "status": "ok"
    }