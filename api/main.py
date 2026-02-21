from fastapi import FastAPI
from pydantic import BaseModel
from retrieval.hybrid_search import hybrid_search
from retrieval.reranker import rerank
from generation.generator import generate_answer

app = FastAPI(title="RAG Knowledge Assistant")

class QueryRequest(BaseModel):
    question: str
    collection: str = "company_kb"
    top_k: int = 5

@app.post("/query")
async def query(req: QueryRequest):
    # Hybrid retrieval
    candidates = await hybrid_search(req.question, req.collection, top_k=req.top_k * 3)
    # Re-rank
    ranked = rerank(req.question, candidates, top_k=req.top_k)
    # Generate with citations
    answer = await generate_answer(req.question, ranked)
    return {"answer": answer.text, "sources": answer.sources, "confidence": answer.confidence}

@app.get("/health")
async def health():
    return {"status": "ok"}
