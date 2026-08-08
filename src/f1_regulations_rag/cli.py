"""Command-line interface: python -m f1_regulations_rag.cli ingest ..."""

import argparse
from pathlib import Path

from f1_regulations_rag.ingestion.chunkers import FixedSizeChunker, HierarchicalChunker
from f1_regulations_rag.ingestion.embedder import get_embedding_provider
from f1_regulations_rag.ingestion.loaders import extract_text
from f1_regulations_rag.ingestion.store import create_schema, get_connection, insert_chunks

STRATEGIES = {
    "fixed": FixedSizeChunker,
    "hierarchical": HierarchicalChunker,
}


def ingest(pdf_dir: str, strategy: str, provider_name: str) -> None:
    """Run the full pipeline: load -> chunk -> embed -> store."""
    chunker = STRATEGIES[strategy]()
    provider = get_embedding_provider(provider_name)
    conn = get_connection()

    for pdf_path in sorted(Path(pdf_dir).glob("*.pdf")):
        text = extract_text(pdf_path)
        chunks = chunker.chunk(text)
        if not chunks:
            print(f"skip  {pdf_path.name} (no chunks)")
            continue
        # First chunk tells us the embedding dimension; create schema once
        create_schema(conn, dimension=384)  # BGE default; OpenAI would be 1536
        embeddings = provider.embed([c.text for c in chunks])
        n = insert_chunks(
            conn,
            chunks,
            embeddings,
            source_doc=pdf_path.stem,
            strategy=strategy,
        )
        print(f"ingested {pdf_path.name}: {n} chunks")

    conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="F1 regulations ingestion")
    sub = parser.add_subparsers(dest="command", required=True)

    ingest_parser = sub.add_parser("ingest", help="Ingest PDFs into pgvector")
    ingest_parser.add_argument("--pdf-dir", default="data/raw", help="Folder with PDFs")
    ingest_parser.add_argument("--strategy", choices=STRATEGIES, default="hierarchical")
    ingest_parser.add_argument("--embedding-provider", default="local")

    args = parser.parse_args()
    if args.command == "ingest":
        ingest(args.pdf_dir, args.strategy, args.embedding_provider)


if __name__ == "__main__":
    main()
