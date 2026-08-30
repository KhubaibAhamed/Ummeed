from app.services.ingestion import ingest_document


class FakeEmbeddingProvider:
    """Test double — returns a predictable fake vector per text, no network call."""

    def __init__(self):
        self.calls: list[list[str]] = []

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.calls.append(texts)
        # deterministic fake vector: length-of-text repeated 3 times
        return [[float(len(t))] * 3 for t in texts]


class FakeVectorStore:
    """Test double — in-memory list instead of a real Qdrant collection."""

    def __init__(self):
        self.upserted_points: list[dict] = []

    def upsert(self, points: list[dict]) -> None:
        self.upserted_points.extend(points)


def test_ingest_document_embeds_every_chunk():
    embedder = FakeEmbeddingProvider()
    store = FakeVectorStore()
    text = "Cercospora leaf spot appears as small yellow-brown lesions. " * 30

    ingest_document(
        document_id="doc-1",
        title="ICAR Cotton Advisory 2025",
        raw_text=text,
        embedding_provider=embedder,
        vector_store=store,
        chunk_size=500,
        overlap=100,
    )

    # embed() should have been called once with all chunk texts batched together
    assert len(embedder.calls) == 1
    assert len(embedder.calls[0]) > 1  # text is long enough to produce multiple chunks


def test_ingest_document_upserts_one_point_per_chunk_with_correct_payload():
    embedder = FakeEmbeddingProvider()
    store = FakeVectorStore()
    text = "Short advisory text."

    ingest_document(
        document_id="doc-42",
        title="Test Scheme Document",
        raw_text=text,
        embedding_provider=embedder,
        vector_store=store,
        chunk_size=800,
        overlap=150,
    )

    assert len(store.upserted_points) == 1
    point = store.upserted_points[0]
    assert point["payload"]["document_id"] == "doc-42"
    assert point["payload"]["document_title"] == "Test Scheme Document"
    assert point["payload"]["chunk_text"] == text
    assert point["payload"]["char_start"] == 0
    assert point["payload"]["char_end"] == len(text)
    assert point["vector"] == [float(len(text))] * 3


def test_ingest_document_returns_summary_with_chunk_count():
    embedder = FakeEmbeddingProvider()
    store = FakeVectorStore()
    text = "A" * 2000

    result = ingest_document(
        document_id="doc-9",
        title="Long Document",
        raw_text=text,
        embedding_provider=embedder,
        vector_store=store,
        chunk_size=800,
        overlap=150,
    )

    assert result["document_id"] == "doc-9"
    assert result["chunks_ingested"] == len(store.upserted_points)
    assert result["chunks_ingested"] > 1


def test_ingest_document_handles_empty_text_gracefully():
    embedder = FakeEmbeddingProvider()
    store = FakeVectorStore()

    result = ingest_document(
        document_id="doc-empty",
        title="Empty Doc",
        raw_text="",
        embedding_provider=embedder,
        vector_store=store,
    )

    assert result["chunks_ingested"] == 0
    assert store.upserted_points == []
    assert embedder.calls == []  # never call the embedding API with nothing to embed
