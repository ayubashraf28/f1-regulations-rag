import psycopg
import pytest

from f1_regulations_rag.ingestion.chunkers import Chunk
from f1_regulations_rag.ingestion.store import create_schema, get_connection, insert_chunks

try:
    conn = get_connection()
    conn.close()
    DB_AVAILABLE = True
except Exception:
    DB_AVAILABLE = False

pytestmark = pytest.mark.skipif(not DB_AVAILABLE, reason="Postgres not running")


@pytest.fixture()
def db():
    conn = get_connection()
    yield conn
    conn.close()


def test_create_schema_and_insert_and_query(db) -> None:
    create_schema(db, dimension=384)
    chunks = [Chunk(text="The quick brown fox", article_number="B1.1")]
    embeddings = [[0.1] * 384]
    inserted = insert_chunks(
        db,
        chunks,
        embeddings,
        source_doc="test_doc",
        strategy="hierarchical",
    )
    assert inserted == 1


def test_dimension_mismatch_raises(db) -> None:
    """Inserting a vector of the wrong size must fail loudly, not silently."""
    create_schema(db, dimension=384)
    chunks = [Chunk(text="wrong dim")]
    with pytest.raises(psycopg.Error):
        insert_chunks(
            db,
            chunks,
            [[0.1, 0.2, 0.3]],  # only 3 numbers, but column expects 384
            source_doc="test_doc",
            strategy="hierarchical",
        )
