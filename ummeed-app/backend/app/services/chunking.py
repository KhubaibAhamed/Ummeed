def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> list[dict]:
    """
    Splits raw document text into overlapping chunks, tracking each chunk's exact
    character span in the original text so citations can point back to the source
    passage precisely, not just a document title.

    Overlap exists so a fact split across a chunk boundary (e.g. a sentence cut in
    half) still appears whole in at least one chunk.
    """
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size, or chunking never progresses")

    if not text:
        return []

    chunks = []
    start = 0
    index = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(
            {
                "text": text[start:end],
                "char_start": start,
                "char_end": end,
                "chunk_index": index,
            }
        )

        if end == text_length:
            break

        start = end - overlap
        index += 1

    return chunks
