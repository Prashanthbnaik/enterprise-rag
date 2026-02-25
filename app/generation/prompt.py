# BUILD CONTEXT

def build_context(
    reranked_results,
    max_chunks=5,
    max_chars_per_chunk=1200
):

    if not reranked_results:
        return ""

    context_blocks = []

    for i, r in enumerate(
        reranked_results[:max_chunks]
    ):

        content = r.get("content", "")

        cleaned = (
            content
            .replace("\n", " ")
            .replace("  ", " ")
            .strip()
        )

        cleaned = cleaned[:max_chars_per_chunk]

        context_blocks.append(
            f"[Source {i+1}] {cleaned}"
        )

    return "\n\n".join(context_blocks)



# BUILD PROMPT

def build_prompt(query, context):

    if not context:

        return f"""
No supporting context available.

User question:
{query}

Respond EXACTLY:
Insufficient evidence found in documents.
"""


    return f"""
You are an enterprise Retrieval-Augmented Generation (RAG) assistant.

You MUST follow these rules strictly:

RULES:

1. Answer ONLY using the provided context.

2. Do NOT use prior knowledge.

3. Every factual claim MUST include citation like:
   [Source 1]

4. If answer not clearly present, respond EXACTLY:

Insufficient evidence found in documents.



CONTEXT


{context}



QUESTION


{query}


ANSWER

"""