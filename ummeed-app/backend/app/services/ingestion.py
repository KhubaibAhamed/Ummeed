from app.services.chunking import chunk_text
from app.services.embeddings import EmbeddingProvider
from app.services.vector_store import VectorStore


def ingest_document(
    document_id: str,
    title: str,
    raw_text: str,
    embedding_provider: EmbeddingProvider,
    vector_store: VectorStore,
    chunk_size: int = 800,
    overlap: int = 150,
) -> dict:
    """
    Turns one document's raw text into embedded, searchable chunks.

    Embeds all chunks in a single batched call rather than one call per chunk —
    fewer round trips, and keeps us well within free-tier rate limits when
    ingesting a whole document corpus.
    """
    chunks = chunk_text(raw_text, chunk_size=chunk_size, overlap=overlap)

    if not chunks:
        return {"document_id": document_id, "chunks_ingested": 0}

    chunk_texts = [c["text"] for c in chunks]
    vectors = embedding_provider.embed(chunk_texts)

    points = [
        {
            "vector": vectors[i],
            "payload": {
                "document_id": document_id,
                "document_title": title,
                "chunk_text": chunk["text"],
                "chunk_index": chunk["chunk_index"],
                "char_start": chunk["char_start"],
                "char_end": chunk["char_end"],
            },
        }
        for i, chunk in enumerate(chunks)
    ]

    vector_store.upsert(points)

    return {"document_id": document_id, "chunks_ingested": len(points)}
