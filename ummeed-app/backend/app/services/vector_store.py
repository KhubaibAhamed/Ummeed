import uuid
from typing import Protocol


class VectorStore(Protocol):
    """
    Anything that can store and search embedded chunks. A Protocol so ingestion and
    retrieval logic can be tested against an in-memory fake, without a live Qdrant
    Cloud connection for every test run.
    """

    def upsert(self, points: list[dict]) -> None: ...
    def search(self, vector: list[float], top_k: int) -> list[dict]: ...


class QdrantVectorStore:
    """
    Real implementation, wrapping Qdrant Cloud. Only constructed and exercised once
    QDRANT_URL and QDRANT_API_KEY are configured — not used in unit tests.
    """

    def __init__(self, url: str, api_key: str, collection_name: str = "ummeed_chunks"):
        if not url or not api_key:
            raise ValueError("QDRANT_URL and QDRANT_API_KEY are required")
        self._collection_name = collection_name
        self._client = None
        self._url = url
        self._api_key = api_key

    def _get_client(self):
        if self._client is None:
            from qdrant_client import QdrantClient

            self._client = QdrantClient(url=self._url, api_key=self._api_key)
        return self._client

    def upsert(self, points: list[dict]) -> None:
        from qdrant_client.models import PointStruct

        client = self._get_client()
        qdrant_points = [
            PointStruct(
                id=p.get("id", str(uuid.uuid4())),
                vector=p["vector"],
                payload=p["payload"],
            )
            for p in points
        ]
        client.upsert(collection_name=self._collection_name, points=qdrant_points)

    def search(self, vector: list[float], top_k: int) -> list[dict]:
        client = self._get_client()
        results = client.search(
            collection_name=self._collection_name, query_vector=vector, limit=top_k
        )
        return [{"payload": r.payload, "score": r.score} for r in results]
