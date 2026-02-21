"""
CLI ingestion pipeline — loads documents, chunks, embeds, and upserts to Supabase pgvector.

Usage:
  python ingest.py --source ./docs --collection company_kb
"""
import argparse
from ingestion.loaders import load_documents
from ingestion.chunker import chunk_documents
from ingestion.embedder import embed_and_upsert

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Path to documents folder")
    parser.add_argument("--collection", default="default", help="Vector collection name")
    args = parser.parse_args()

    print(f"Loading documents from {args.source}...")
    docs = load_documents(args.source)
    print(f"Loaded {len(docs)} documents")

    chunks = chunk_documents(docs)
    print(f"Created {len(chunks)} chunks")

    embed_and_upsert(chunks, collection=args.collection)
    print(f"Ingestion complete. Collection: {args.collection}")

if __name__ == "__main__":
    main()
