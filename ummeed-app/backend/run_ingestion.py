"""
One-off ingestion script for Ummeed.

Usage (from the backend/ folder, with the venv active):
    .venv\\Scripts\\python run_ingestion.py

What it does:
1. Reads GEMINI_API_KEY / QDRANT_URL / QDRANT_API_KEY from backend/.env
2. Creates the "ummeed_chunks" collection in Qdrant if it doesn't exist yet,
   sized correctly for gemini-embedding-001 (3072 dimensions).
3. Reads every .txt file in ../ingestion/documents/, chunks it, embeds it,
   and upserts it into Qdrant.

Put your source .txt files in ummeed-app/ingestion/documents/ before running this.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from app.config import settings
from app.services.embeddings import GeminiEmbeddingProvider
from app.services.ingestion import ingest_document
from app.services.vector_store import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

COLLECTION_NAME = "ummeed_chunks"
EMBEDDING_DIM = 3072  # gemini-embedding-001 default output size
DOCUMENTS_DIR = pathlib.Path(__file__).parent.parent / "ingestion" / "documents"


def ensure_collection(client: QdrantClient):
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME in existing:
        print(f"Collection '{COLLECTION_NAME}' already exists — skipping creation.")
        return
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
    )
    print(f"Created collection '{COLLECTION_NAME}' with dim={EMBEDDING_DIM}.")


def main():
    if not settings.gemini_api_key or not settings.qdrant_url or not settings.qdrant_api_key:
        print("Missing GEMINI_API_KEY / QDRANT_URL / QDRANT_API_KEY in .env — aborting.")
        return

    raw_client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
    ensure_collection(raw_client)

    embedding_provider = GeminiEmbeddingProvider(api_key=settings.gemini_api_key)
    vector_store = QdrantVectorStore(url=settings.qdrant_url, api_key=settings.qdrant_api_key)

    if not DOCUMENTS_DIR.exists():
        print(f"No documents folder found at {DOCUMENTS_DIR} — nothing to ingest.")
        return

    txt_files = sorted(DOCUMENTS_DIR.glob("*.txt"))
    if not txt_files:
        print(f"No .txt files found in {DOCUMENTS_DIR} — add some documents and rerun.")
        return

    for path in txt_files:
        text = path.read_text(encoding="utf-8")
        result = ingest_document(
            document_id=path.stem,
            title=path.stem.replace("_", " ").title(),
            raw_text=text,
            embedding_provider=embedding_provider,
            vector_store=vector_store,
        )
        print(f"Ingested {path.name}: {result['chunks_ingested']} chunks")

    print("Done.")


if __name__ == "__main__":
    main()