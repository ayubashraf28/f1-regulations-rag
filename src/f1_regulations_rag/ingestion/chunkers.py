"""Chunking strategies for the F1 regulation corpus.

All chunkers implement the same contract: chunk(text: str) -> list[Chunk].
This lets the evaluation harness swap strategies without changing code.
"""

import re
from dataclasses import dataclass

import tiktoken


@dataclass(frozen=True)
class Chunk:
    """A single retrievable piece of text, with optional metadata."""

    text: str
    article_number: str | None = None


class FixedSizeChunker:
    """Cut text into chunks of ~chunk_size tokens, with token overlap."""

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 50,
        encoding_name: str = "cl100k_base",
    ) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap
        self._enc = tiktoken.get_encoding(encoding_name)

    def chunk(self, text: str) -> list[Chunk]:
        tokens = self._enc.encode(text)
        if not tokens:
            return []
        if len(tokens) <= self.chunk_size:
            return [Chunk(text=text)]

        stride = self.chunk_size - self.overlap
        chunks: list[Chunk] = []
        start = 0
        while start < len(tokens):
            end = min(start + self.chunk_size, len(tokens))
            chunks.append(Chunk(text=self._enc.decode(tokens[start:end])))
            if end == len(tokens):
                break
            start += stride
        return chunks


class HierarchicalChunker:
    """Split on the regulations' real structure.

    The 2026 FIA format uses 'ARTICLE B5: TITLE' for top-level articles
    and 'B5.13' for sub-clauses. The section letter prefix (B, C, ...)
    distinguishes real article numbers from table row labels like '1.1'.
    """

    _TOP_LEVEL = re.compile(r"^ARTICLE\s+([A-Z]\d+)\s*:")
    _SUB_CLAUSE = re.compile(r"^([A-Z]\d+\.\d+)\s+\S")

    def chunk(self, text: str) -> list[Chunk]:
        chunks: list[Chunk] = []
        current: list[str] = []
        current_number: str | None = None

        def flush() -> None:
            if current:
                chunks.append(Chunk(text="\n".join(current), article_number=current_number))

        for line in text.splitlines():
            top = self._TOP_LEVEL.match(line)
            sub = self._SUB_CLAUSE.match(line)
            if top:
                flush()
                current, current_number = [line], top.group(1)
            elif sub:
                flush()
                current, current_number = [line], sub.group(1)
            else:
                current.append(line)
        flush()
        return chunks
