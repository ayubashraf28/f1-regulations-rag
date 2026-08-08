import tiktoken

from f1_regulations_rag.ingestion.chunkers import FixedSizeChunker


def test_empty_text_yields_no_chunks() -> None:
    assert FixedSizeChunker().chunk("") == []


def test_short_text_yields_single_chunk() -> None:
    chunks = FixedSizeChunker().chunk("A short piece of text.")
    assert len(chunks) == 1
    assert chunks[0].text == "A short piece of text."


def test_every_chunk_respects_max_token_size() -> None:
    long_text = "the quick brown fox jumps over the lazy dog. " * 60
    enc = tiktoken.get_encoding("cl100k_base")
    chunks = FixedSizeChunker(chunk_size=100, overlap=10).chunk(long_text)
    assert len(chunks) > 1  # we did get multiple chunks
    for chunk in chunks:
        assert len(enc.encode(chunk.text)) <= 100


def test_consecutive_chunks_overlap() -> None:
    long_text = "the quick brown fox jumps over the lazy dog. " * 60
    chunks = FixedSizeChunker(chunk_size=100, overlap=20).chunk(long_text)
    first_tail = chunks[0].text.split()[-5:]
    second_head = chunks[1].text.split()[:5]
    assert set(first_tail) & set(second_head)  # they share some words
