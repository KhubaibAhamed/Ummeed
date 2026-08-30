import time

from fastapi import APIRouter, Depends

from app.dependencies import (
    get_embedding_provider,
    get_llm_provider,
    get_mandi_provider,
    get_vector_store,
    get_weather_provider,
)
from app.models.schemas import QueryRequest, QueryResponse
from app.services.generation import generate_answer
from app.services.intent import detect_intent
from app.services.live_data import fetch_live_data
from app.services.retrieval import retrieve_relevant_chunks

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query(
    request: QueryRequest,
    embedding_provider=Depends(get_embedding_provider),
    vector_store=Depends(get_vector_store),
    llm_provider=Depends(get_llm_provider),
    weather_provider=Depends(get_weather_provider),
    mandi_provider=Depends(get_mandi_provider),
):
    start = time.perf_counter()

    intent = detect_intent(request.text)
    live_data = fetch_live_data(intent, request.location, weather_provider, mandi_provider)

    retrieved_chunks = retrieve_relevant_chunks(
        request.text, embedding_provider, vector_store
    )

    result = generate_answer(
        query=request.text,
        language=request.language,
        retrieved_chunks=retrieved_chunks,
        live_data=live_data,
        llm_provider=llm_provider,
    )

    elapsed_ms = int((time.perf_counter() - start) * 1000)

    return QueryResponse(
        answer=result["answer"],
        citations=result["citations"],
        live_data=result["live_data"],
        response_time_ms=elapsed_ms,
        grounded=result["grounded"],
    )
