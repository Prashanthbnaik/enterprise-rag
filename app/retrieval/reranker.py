import torch
from sentence_transformers import CrossEncoder



# LOAD MODEL 

try:

    device = "cuda" if torch.cuda.is_available() else "cpu"

    reranker_model = CrossEncoder(
        "cross-encoder/ms-marco-MiniLM-L-6-v2",
        device=device
    )

    print(f"Reranker loaded on {device}")

except Exception as e:

    print(f"Reranker failed to load: {e}")

    reranker_model = None



# RERANK FUNCTION

def rerank(query, candidates, batch_size=16):

    if not candidates:
        return []

    if reranker_model is None:
        return candidates


    pairs = [

        (query, c["content"])

        for c in candidates

    ]


    scores = reranker_model.predict(

        pairs,

        batch_size=batch_size,

        show_progress_bar=False

    )


    ranked = sorted(

        zip(candidates, scores),

        key=lambda x: x[1],

        reverse=True

    )


    reranked_results = []

    for new_rank, (candidate, score) in enumerate(ranked):

        reranked_results.append({

            "rank": new_rank + 1,

            "score": float(score),

            "content": candidate["content"],

            "doc": candidate["doc"]

        })


    return reranked_results