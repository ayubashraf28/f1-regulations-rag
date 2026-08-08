"""Verify ingested chunks exist in pgvector and run a sample vector search."""

from pgvector import Vector
from pgvector.psycopg import register_vector

from f1_regulations_rag.ingestion.embedder import get_embedding_provider
from f1_regulations_rag.ingestion.store import get_connection

conn = get_connection()
register_vector(conn)  # register BEFORE any query — pgvector requirement

with conn.cursor() as cur:
    # 1. Count rows per document
    cur.execute(
        "SELECT source_doc, COUNT(*) AS n FROM chunks GROUP BY source_doc ORDER BY source_doc"
    )
    print("rows per document:")
    for row in cur.fetchall():
        print(f"  {row['source_doc']}: {row['n']}")

    # 2. Vector similarity search (sneak peek of Phase C)
    question = "What is the minimum pit lane speed?"
    query = get_embedding_provider("local").embed([question])[0]
    cur.execute(
        "SELECT article_number, content, 1 - (embedding <=> %s) AS similarity "
        "FROM chunks ORDER BY embedding <=> %s LIMIT 3",
        (Vector(query), Vector(query)),
    )
    print(f"\ntop 3 chunks for: {question!r}")
    for row in cur.fetchall():
        print(f"  {row['similarity']:.3f}  [{row['article_number']}]  {row['content'][:80]}")

conn.close()