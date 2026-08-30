from app.services.embeddings import EmbeddingProvider
from app.services.vector_store import VectorStore


def retrieve_relevant_chunks(
    query: str,
    embedding_provider: EmbeddingProvider,
    vector_store: VectorStore,
    top_k: int = 4,
    min_score: float = 0.55,
) -> list[dict]:
    """
    Finds chunks relevant to a farmer's query, filtered to only confident matches.

    The min_score threshold is the core anti-hallucination mechanism from the Phase 6
    design: if nothing clears the bar, we return an empty list and the caller (the
    /query endpoint, built in a later module) is expected to say "I don't have
    reliable information on that" rather than let the LLM free-generate an answer.
    """
    query_vector = embedding_provider.embed([query])[0]
    raw_results = vector_store.search(query_vector, top_k)

    confident_results = [r for r in raw_results if r["score"] >= min_score]
    confident_results.sort(key=lambda r: r["score"], reverse=True)

    return [
        {
            "chunk_text": r["payload"]["chunk_text"],
            "document_title": r["payload"]["document_title"],
            "document_id": r["payload"]["document_id"],
            "char_start": r["payload"]["char_start"],
            "char_end": r["payload"]["char_end"],
            "score": r["score"],
        }
        for r in confident_results
    ]
