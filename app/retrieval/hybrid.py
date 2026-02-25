from rank_bm25 import BM25Okapi
import numpy as np


def get_text(doc):
    """
    Supports both LangChain Document and dict formats.
    """
    if hasattr(doc, "page_content"):
        return doc.page_content
    return doc["content"]


# BUILD BM25
def build_bm25_index(documents):

    if not documents:
        return None

    corpus = [
        get_text(doc).lower().split()
        for doc in documents
    ]

    return BM25Okapi(corpus)


# NORMALIZE FAISS
def normalize_vector_scores(distances):

    distances = list(distances)

    if len(distances) == 0:
        return []

    max_dist = max(distances)

    if max_dist == 0:
        return [1.0] * len(distances)

    return [1 - (d / max_dist) for d in distances]


# NORMALIZE BM25
def normalize_bm25_scores(scores):

    scores = list(scores)

    if len(scores) == 0:
        return []

    max_score = max(scores)

    if max_score == 0:
        return [0.0] * len(scores)

    return [s / max_score for s in scores]


# HYBRID SEARCH
def hybrid_search(
    query,
    embedding_model,
    faiss_index,
    documents,
    bm25_index,
    top_k=5,
    alpha=0.6
):

    if not documents:
        return []

    query_embedding = embedding_model.encode([query]).astype("float32")

    distances, indices = faiss_index.search(
        query_embedding,
        min(top_k * 3, len(documents))
    )

    semantic_scores = normalize_vector_scores(distances[0])

    semantic_dict = {
        int(indices[0][i]): semantic_scores[i]
        for i in range(len(indices[0]))
    }


    # BM25
    if bm25_index is not None:

        bm25_scores = bm25_index.get_scores(
            query.lower().split()
        )

        bm25_norm = normalize_bm25_scores(bm25_scores)

    else:

        bm25_norm = [0.0] * len(documents)


    combined = {}

    for i in range(len(documents)):

        sem = semantic_dict.get(i, 0.0)
        bm = bm25_norm[i] if i < len(bm25_norm) else 0.0

        combined[i] = alpha * sem + (1 - alpha) * bm


    ranked = sorted(
        combined.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_k]


    results = []

    for rank, (idx, score) in enumerate(ranked):

        results.append({

            "rank": rank + 1,
            "score": float(score),
            "content": get_text(documents[idx]),
            "doc": documents[idx]

        })

    return results