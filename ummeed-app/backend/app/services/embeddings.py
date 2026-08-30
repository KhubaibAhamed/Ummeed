from typing import Protocol


class EmbeddingProvider(Protocol):
    """
    Anything that turns text into vectors. Defined as a Protocol so ingestion logic
    can be tested against a fake, without needing a live API key for every test run.
    """

    def embed(self, texts: list[str]) -> list[list[float]]: ...


class GeminiEmbeddingProvider:
    """
    Real implementation, wrapping Gemini's text-embedding-004 model. Only constructed
    and exercised once a real GEMINI_API_KEY is configured — not used in unit tests.
    """

    def __init__(self, api_key: str, model: str = "gemini-embedding-001"):
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required to construct GeminiEmbeddingProvider")
        self._api_key = api_key
        self._model = model
        self._client = None  # lazily constructed, see _get_client

    def _get_client(self):
        if self._client is None:
            from google import genai

            self._client = genai.Client(api_key=self._api_key)
        return self._client

    def embed(self, texts: list[str]) -> list[list[float]]:
        client = self._get_client()
        result = client.models.embed_content(model=self._model, contents=texts)
        return [embedding.values for embedding in result.embeddings]
