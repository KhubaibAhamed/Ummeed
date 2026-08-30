from app.services.chunking import chunk_text


def test_short_text_returns_single_chunk():
    text = "This is a short crop advisory."
    chunks = chunk_text(text, chunk_size=800, overlap=150)

    assert len(chunks) == 1
    assert chunks[0]["text"] == text
    assert chunks[0]["char_start"] == 0
    assert chunks[0]["char_end"] == len(text)


def test_long_text_splits_into_multiple_chunks():
    # 2000 chars of content, well beyond a single 800-char chunk
    text = "A" * 2000
    chunks = chunk_text(text, chunk_size=800, overlap=150)

    assert len(chunks) > 1
    # every chunk should be at most chunk_size long
    assert all(len(c["text"]) <= 800 for c in chunks)


def test_consecutive_chunks_overlap_by_requested_amount():
    text = "A" * 2000
    chunks = chunk_text(text, chunk_size=800, overlap=150)

    first_end = chunks[0]["char_end"]
    second_start = chunks[1]["char_start"]
    # overlap means the second chunk starts before the first one ends
    assert first_end - second_start == 150


def test_char_positions_map_back_to_original_text():
    text = "Cercospora leaf spot appears as small yellow-brown lesions. " * 30
    chunks = chunk_text(text, chunk_size=500, overlap=100)

    for c in chunks:
        assert text[c["char_start"] : c["char_end"]] == c["text"]


def test_chunk_index_increments_in_order():
    text = "A" * 2000
    chunks = chunk_text(text, chunk_size=800, overlap=150)

    indices = [c["chunk_index"] for c in chunks]
    assert indices == list(range(len(chunks)))


def test_empty_text_returns_no_chunks():
    assert chunk_text("", chunk_size=800, overlap=150) == []


def test_invalid_overlap_raises_value_error():
    # overlap must be smaller than chunk_size or chunking would never progress
    import pytest

    with pytest.raises(ValueError):
        chunk_text("some text", chunk_size=100, overlap=100)
