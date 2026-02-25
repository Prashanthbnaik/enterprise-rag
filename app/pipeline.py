import time
import os

from dotenv import load_dotenv

from app.core.vector_store import (
    get_index,
    get_documents,
    get_bm25,
    get_embedding_model
)

from app.retrieval.hybrid import hybrid_search
from app.retrieval.reranker import rerank

from app.generation.llm_client import GroqLLMClient
from app.generation.prompt import build_prompt, build_context


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = GroqLLMClient(GROQ_API_KEY)


def rag_pipeline(query: str):

    start = time.time()

    # Load indexed documents
    docs = get_documents()

    if not docs:
        return {
            "answer": "No documents indexed.",
            "contexts": [],
            "latency": 0
        }


    # Hybrid retrieval
    results = hybrid_search(
        query=query,
        embedding_model=get_embedding_model(),
        faiss_index=get_index(),
        documents=docs,
        bm25_index=get_bm25()
    )


    if not results:
        return {
            "answer": "No relevant context found.",
            "contexts": [],
            "latency": round(time.time() - start, 3)
        }


    # Rerank
    reranked = rerank(query, results)


    if not reranked:
        return {
            "answer": "No relevant context after reranking.",
            "contexts": [],
            "latency": round(time.time() - start, 3)
        }


    # Top-K chunks
    top_chunks = reranked[:5]


    # Safe context extraction
    contexts = []
    for chunk in top_chunks:
        content = chunk.get("content")
        if content:
            contexts.append(content)


    if not contexts:
        return {
            "answer": "No usable context found.",
            "contexts": [],
            "latency": round(time.time() - start, 3)
        }


    # Build prompt
    context_text = build_context(top_chunks)

    prompt = build_prompt(query, context_text)


    # Generate answer
    try:

        response = llm.generate(prompt)

        answer = response.get("text", "").strip()

        if not answer:
            answer = "No answer generated."

    except Exception as e:

        answer = f"LLM failed: {str(e)}"


    latency = round(time.time() - start, 3)


    return {
        "answer": answer,
        "contexts": contexts,
        "latency": latency
    }