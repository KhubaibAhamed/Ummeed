from fastapi.testclient import TestClient

from app.dependencies import (
    get_embedding_provider,
    get_llm_provider,
    get_mandi_provider,
    get_vector_store,
    get_weather_provider,
)
from app.main import app


class FakeEmbeddingProvider:
    def embed(self, texts):
        return [[0.1, 0.2, 0.3] for _ in texts]


class FakeVectorStoreWithResults:
    def search(self, vector, top_k):
        return [
            {
                "payload": {
                    "chunk_text": "Cercospora leaf spot appears during high humidity.",
                    "document_title": "ICAR Cotton Advisory 2025",
                    "document_id": "d1",
                    "char_start": 0,
                    "char_end": 50,
                },
                "score": 0.87,
            }
        ]

    def upsert(self, points):
        pass


class FakeVectorStoreNoResults:
    def search(self, vector, top_k):
        return []

    def upsert(self, points):
        pass


class FakeLLMProvider:
    def generate(self, prompt: str) -> str:
        return "Remove affected leaves and monitor humidity levels."


class FakeWeatherProvider:
    def get_weather(self, location):
        return {"humidity": 68, "temp_celsius": 28.5, "forecast_trend": "falling"}


class FakeMandiProvider:
    def get_price(self, crop, location):
        return {"price_per_quintal": 6850.0, "mandi_name": "Guntur", "date": "29/08/2026"}


def _override(vector_store):
    app.dependency_overrides[get_embedding_provider] = lambda: FakeEmbeddingProvider()
    app.dependency_overrides[get_vector_store] = lambda: vector_store
    app.dependency_overrides[get_llm_provider] = lambda: FakeLLMProvider()
    app.dependency_overrides[get_weather_provider] = lambda: FakeWeatherProvider()
    app.dependency_overrides[get_mandi_provider] = lambda: FakeMandiProvider()


def _clear_overrides():
    app.dependency_overrides.clear()


def test_query_endpoint_returns_grounded_answer_with_citations():
    _override(FakeVectorStoreWithResults())
    client = TestClient(app)

    response = client.post(
        "/query", json={"text": "Why are my cotton leaves yellow?", "language": "en"}
    )
    _clear_overrides()

    assert response.status_code == 200
    body = response.json()
    assert body["grounded"] is True
    assert body["answer"] == "Remove affected leaves and monitor humidity levels."
    assert len(body["citations"]) == 1
    assert body["citations"][0]["document_title"] == "ICAR Cotton Advisory 2025"
    assert isinstance(body["response_time_ms"], int)


def test_query_endpoint_returns_honest_fallback_when_nothing_retrieved():
    _override(FakeVectorStoreNoResults())
    client = TestClient(app)

    response = client.post(
        "/query", json={"text": "What is the meaning of life?", "language": "en"}
    )
    _clear_overrides()

    assert response.status_code == 200
    body = response.json()
    assert body["grounded"] is False
    assert body["citations"] == []
    assert "don't have" in body["answer"].lower()


def test_query_endpoint_rejects_missing_text_field():
    _override(FakeVectorStoreWithResults())
    client = TestClient(app)

    response = client.post("/query", json={"language": "en"})
    _clear_overrides()

    assert response.status_code == 422  # FastAPI's validation error for missing required field


def test_query_endpoint_includes_live_data_when_intent_and_location_present():
    _override(FakeVectorStoreWithResults())
    client = TestClient(app)

    response = client.post(
        "/query",
        json={
            "text": "Should I spray my cotton or wait for the rain?",
            "language": "en",
            "location": "Guntur",
        },
    )
    _clear_overrides()

    assert response.status_code == 200
    body = response.json()
    assert len(body["live_data"]) == 1
    assert body["live_data"][0]["label"] == "Weather"


def test_query_endpoint_omits_live_data_when_no_location_given():
    _override(FakeVectorStoreWithResults())
    client = TestClient(app)

    response = client.post(
        "/query",
        json={"text": "Should I spray my cotton or wait for the rain?", "language": "en"},
    )
    _clear_overrides()

    assert response.status_code == 200
    assert response.json()["live_data"] == []
