# RAG Knowledge Assistant — Enterprise Doc Q&A

Production RAG system enabling enterprise teams to query 10,000+ internal documents via natural language — returning accurate, cited answers instead of digging through folders.

## Architecture

```
Ingestion Pipeline                    Query Path
──────────────────                    ──────────
PDF/DOCX/HTML/CSV                     User Query (Next.js UI)
      ↓                                      ↓
LangChain text splitters              Query Rewriter (HyDE + expansion)
      ↓                                      ↓
OpenAI text-embedding-3-large    →   pgvector on Supabase
  (10,000+ docs indexed)              Semantic + BM25 hybrid retrieval
                                             ↓
                                       Re-ranker (cross-encoder)
                                             ↓
                                       LLM Generator (Claude API)
                                             ↓
                                       Answer + Source Citations
```

## Tech Stack
```
Python 3.11 · LangChain · FastAPI · OpenAI Embeddings
Claude API (generation) · Supabase pgvector · Next.js (UI)
BM25 (keyword index) · Docker · Redis (query cache)
```

## Key Features
- ✅ **Hybrid retrieval**: semantic + BM25 keyword search combined
- ✅ **Re-ranking**: cross-encoder confidence scoring filters weak matches
- ✅ **HyDE query expansion**: hypothetical document embeddings improve recall
- ✅ **Source citations**: every answer includes doc name + page reference
- ✅ **Confidence flagging**: low-certainty answers are marked for human review
- ✅ **Multi-format ingestion**: PDF, DOCX, HTML, CSV, plain text

## Results
- 10,000+ docs indexed across 3 enterprise clients
- Sub-2s average query response time
- 60% reduction in internal support tickets
- 94% answer accuracy on held-out eval set

## Quick Start
```bash
git clone https://github.com/b24repo/rag-knowledge-assistant
cd rag-knowledge-assistant
pip install -r requirements.txt
cp .env.example .env
# Run ingestion pipeline
python ingest.py --source ./docs --collection company_kb
# Start API server
uvicorn api.main:app --reload
```

## Project Structure
```
├── ingestion/
│   ├── loaders.py          # PDF, DOCX, HTML, CSV loaders
│   ├── chunker.py          # LangChain text splitters
│   └── embedder.py         # OpenAI embedding + pgvector upsert
├── retrieval/
│   ├── hybrid_search.py    # Semantic + BM25 fusion
│   ├── reranker.py         # Cross-encoder re-ranking
│   └── query_rewriter.py   # HyDE + query expansion
├── generation/
│   └── generator.py        # Claude API with citation grounding
├── api/
│   └── main.py             # FastAPI Q&A endpoint
├── ui/                     # Next.js chat interface
├── ingest.py               # CLI ingestion entrypoint
├── requirements.txt
└── .env.example
```

---
*Built for enterprise teams that need reliable answers from their internal knowledge base.*