"""pgvector storage for chunks.

Saves text chunks with their embeddings and metadata into PostgreSQL
using the pgvector extension.
"""

from pgvector.psycopg import register_vector
from psycopg import Connection, connect
from psycopg.rows import dict_row

from f1_regulations_rag.config import settings


def get_connection() -> Connection:
    """Open a connection to the configured Postgres database."""
    return connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        user=settings.postgres_user,
        password=settings.postgres_password,
        dbname=settings.postgres_db,
        row_factory=dict_row,
    )


def create_schema(conn: Connection, dimension: int, table: str = "chunks") -> None:
    """Create the pgvector extension and the chunks table (idempotent)."""
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
        cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id BIGSERIAL PRIMARY KEY,
                source_doc TEXT NOT NULL,
                article_number TEXT,
                chunking_strategy TEXT NOT NULL,
                content TEXT NOT NULL,
                embedding vector({dimension})
            )
            """
        )
    conn.commit()


def insert_chunks(
    conn: Connection,
    chunks: list,
    embeddings: list[list[float]],
    source_doc: str,
    strategy: str,
    table: str = "chunks",
) -> int:
    """Insert chunks with embeddings. Returns the number of rows inserted."""
    register_vector(conn)
    with conn.cursor() as cur:
        cur.executemany(
            f"""
            INSERT INTO {table}
                (source_doc, article_number, chunking_strategy, content, embedding)
            VALUES (%s, %s, %s, %s, %s)
            """,
            [
                (source_doc, c.article_number, strategy, c.text, emb)
                for c, emb in zip(chunks, embeddings, strict=True)
            ],
        )
    conn.commit()
    return len(chunks)
