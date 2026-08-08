import pytest

from f1_regulations_rag.ingestion.embedder import (
    BaseEmbeddingProvider,
    CachedEmbeddingProvider,
    LocalBGEProvider,
    get_embedding_provider,
)


class _FakeProvider(BaseEmbeddingProvider):
    """A provider that never touches the network or a model."""

    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.calls.append(texts)
        return [[float(len(t))] for t in texts]


def test_cached_provider_returns_vectors_in_order(tmp_path) -> None:
    provider = CachedEmbeddingProvider(_FakeProvider(), cache_dir=tmp_path)
    assert provider.embed(["aa", "bbbb"]) == [[2.0], [4.0]]


def test_cached_provider_does_not_recompute_on_second_call(tmp_path) -> None:
    inner = _FakeProvider()
    provider = CachedEmbeddingProvider(inner, cache_dir=tmp_path)
    provider.embed(["hello world"])
    provider.embed(["hello world"])
    assert len(inner.calls) == 1


def test_cached_provider_empty_input(tmp_path) -> None:
    assert CachedEmbeddingProvider(_FakeProvider(), cache_dir=tmp_path).embed([]) == []


def test_factory_unknown_provider_raises() -> None:
    with pytest.raises(ValueError):
        get_embedding_provider("bogus")


def test_factory_local_returns_cached_bge() -> None:
    provider = get_embedding_provider("local")
    assert isinstance(provider, CachedEmbeddingProvider)
    assert isinstance(provider.inner, LocalBGEProvider)
