from app.services.retrieval import retrieve_relevant_chunks


class FakeEmbeddingProvider:
    def __init__(self, fixed_vector=None):
        self.calls: list[list[str]] = []
        self._fixed_vector = fixed_vector or [0.1, 0.2, 0.3]

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.calls.append(texts)
        return [self._fixed_vector for _ in texts]


class FakeVectorStore:
    """Returns a pre-canned set of search results, shaped like QdrantVectorStore.search()."""

    def __init__(self, canned_results: list[dict]):
        self._canned_results = canned_results
        self.search_calls: list[dict] = []

    def upsert(self, points):  # not used in these tests, present to satisfy the interface
        pass

    def search(self, vector: list[float], top_k: int) -> list[dict]:
        self.search_calls.append({"vector": vector, "top_k": top_k})
        return self._canned_results[:top_k]


def test_retrieve_embeds_the_query_text():
    embedder = FakeEmbeddingProvider()
    store = FakeVectorStore(canned_results=[])

    retrieve_relevant_chunks("my cotton has yellow spots", embedder, store)

    assert embedder.calls == [["my cotton has yellow spots"]]


def test_retrieve_searches_with_query_vector_and_top_k():
    embedder = FakeEmbeddingProvider(fixed_vector=[0.5, 0.5])
    store = FakeVectorStore(canned_results=[])

    retrieve_relevant_chunks("test query", embedder, store, top_k=6)

    assert store.search_calls[0]["vector"] == [0.5, 0.5]
    assert store.search_calls[0]["top_k"] == 6


def test_retrieve_filters_out_results_below_min_score():
    embedder = FakeEmbeddingProvider()
    store = FakeVectorStore(
        canned_results=[
            {"payload": {"chunk_text": "confident match", "document_title": "Doc A",
                          "document_id": "d1", "char_start": 0, "char_end": 10}, "score": 0.9},
            {"payload": {"chunk_text": "weak match", "document_title": "Doc B",
                          "document_id": "d2", "char_start": 0, "char_end": 10}, "score": 0.3},
        ]
    )

    results = retrieve_relevant_chunks("test", embedder, store, min_score=0.55)

    assert len(results) == 1
    assert results[0]["chunk_text"] == "confident match"


def test_retrieve_returns_correctly_shaped_chunk_data():
    embedder = FakeEmbeddingProvider()
    store = FakeVectorStore(
        canned_results=[
            {"payload": {"chunk_text": "leaf spot advice", "document_title": "ICAR Cotton Advisory",
                          "document_id": "d1", "char_start": 20, "char_end": 80}, "score": 0.81},
        ]
    )

    results = retrieve_relevant_chunks("test", embedder, store, min_score=0.55)

    assert results[0] == {
        "chunk_text": "leaf spot advice",
        "document_title": "ICAR Cotton Advisory",
        "document_id": "d1",
        "char_start": 20,
        "char_end": 80,
        "score": 0.81,
    }


def test_retrieve_returns_empty_list_when_nothing_meets_threshold():
    embedder = FakeEmbeddingProvider()
    store = FakeVectorStore(
        canned_results=[
            {"payload": {"chunk_text": "irrelevant", "document_title": "Doc X",
                          "document_id": "d9", "char_start": 0, "char_end": 5}, "score": 0.2},
        ]
    )

    results = retrieve_relevant_chunks("unrelated question", embedder, store, min_score=0.55)

    assert results == []


def test_retrieve_results_are_sorted_highest_score_first():
    embedder = FakeEmbeddingProvider()
    store = FakeVectorStore(
        canned_results=[
            {"payload": {"chunk_text": "medium", "document_title": "Doc A",
                          "document_id": "d1", "char_start": 0, "char_end": 5}, "score": 0.6},
            {"payload": {"chunk_text": "highest", "document_title": "Doc B",
                          "document_id": "d2", "char_start": 0, "char_end": 5}, "score": 0.95},
        ]
    )

    results = retrieve_relevant_chunks("test", embedder, store, min_score=0.5)

    assert results[0]["chunk_text"] == "highest"
    assert results[1]["chunk_text"] == "medium"
