"""Pluggable embedding providers.

Contract: every provider implements embed(texts) -> list[list[float]].
Select the active one via config: EMBEDDING_PROVIDER=openai|local.
"""

from abc import ABC, abstractmethod
from hashlib import sha256
from pathlib import Path
from diskcache import Cache

from f1_regulations_rag.config import CACHE_ROOT, settings


class BaseEmbeddingProvider(ABC):
    """The contract every embedding provider must implement."""

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Return one vector per input text."""


class OpenAIEmbeddingProvider(BaseEmbeddingProvider):
    """Cloud embeddings via OpenAI's text-embedding-3-small."""

    def __init__(self, model: str = "text-embedding-3-small") -> None:
        from openai import OpenAI

        self._client = OpenAI(api_key=settings.openai_api_key)
        self._model = model

    def embed(self, texts: list[str]) -> list[list[float]]:
        response = self._client.embeddings.create(model=self._model, input=texts)
        return [item.embedding for item in response.data]


class LocalBGEProvider(BaseEmbeddingProvider):
    """Local open-source embeddings via BAAI/bge-small-en-v1.5."""

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5") -> None:
        self._model_name = model_name
        self._model = None  # lazy: don't load 130MB at import time

    def _load(self) -> None:
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self._model_name)

    def embed(self, texts: list[str]) -> list[list[float]]:
        self._load()
        vectors = self._model.encode(texts, normalize_embeddings=True)
        return [v.tolist() for v in vectors]


class CachedEmbeddingProvider(BaseEmbeddingProvider):
    """Wraps any provider with a disk cache keyed by text hash.

    Cache folder is per provider class, so OpenAI (1536-dim) and BGE
    (384-dim) vectors never collide.
    """

    def __init__(self, inner: BaseEmbeddingProvider, cache_dir: Path | None = None) -> None:
        self._inner = inner
        if cache_dir is None:
            cache_dir = CACHE_ROOT / "embeddings" / type(inner).__name__
        cache_dir.mkdir(parents=True, exist_ok=True)
        self._cache = Cache(str(cache_dir))

    @property
    def inner(self) -> BaseEmbeddingProvider:
        return self._inner

    @staticmethod
    def _hash(text: str) -> str:
        return sha256(text.encode("utf-8")).hexdigest()

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        results: list[list[float] | None] = [None] * len(texts)
        missing: list[tuple[int, str]] = []
        for index, text in enumerate(texts):
            key = self._hash(text)
            if key in self._cache:
                results[index] = self._cache[key]
            else:
                missing.append((index, text))
        if missing:
            fresh = self._inner.embed([text for _, text in missing])
            for (index, text), vector in zip(missing, fresh, strict=True):
                self._cache[self._hash(text)] = vector
                results[index] = vector
        assert all(v is not None for v in results)
        return [v for v in results if v is not None]




def get_embedding_provider(provider: str | None = None) -> BaseEmbeddingProvider:
    """Factory: return the configured provider, wrapped in the cache."""
    selected = provider or settings.embedding_provider
    if selected == "openai":
        return CachedEmbeddingProvider(OpenAIEmbeddingProvider())
    if selected == "local":
        return CachedEmbeddingProvider(LocalBGEProvider())
    raise ValueError(f"Unknown EMBEDDING_PROVIDER: {selected!r}")
