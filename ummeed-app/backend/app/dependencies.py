from functools import lru_cache

from app.config import settings
from app.services.embeddings import GeminiEmbeddingProvider
from app.services.generation import GeminiLLMProvider
from app.services.mandi import AgmarknetProvider
from app.services.transcription import SarvamSTTProvider
from app.services.vector_store import QdrantVectorStore
from app.services.weather import OpenWeatherMapProvider


@lru_cache
def get_embedding_provider() -> GeminiEmbeddingProvider:
    return GeminiEmbeddingProvider(api_key=settings.gemini_api_key)


@lru_cache
def get_llm_provider() -> GeminiLLMProvider:
    return GeminiLLMProvider(api_key=settings.gemini_api_key)


@lru_cache
def get_vector_store() -> QdrantVectorStore:
    return QdrantVectorStore(url=settings.qdrant_url, api_key=settings.qdrant_api_key)


@lru_cache
def get_weather_provider() -> OpenWeatherMapProvider:
    return OpenWeatherMapProvider(
        api_key=settings.openweather_api_key,
        timeout_seconds=settings.live_api_timeout_seconds,
    )


@lru_cache
def get_mandi_provider() -> AgmarknetProvider:
    return AgmarknetProvider(
        api_key=settings.agmarknet_api_key,
        timeout_seconds=settings.live_api_timeout_seconds,
    )


@lru_cache
def get_transcription_provider() -> SarvamSTTProvider:
    return SarvamSTTProvider(api_key=settings.sarvam_api_key)
