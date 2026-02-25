# app/generation/guardrails.py

import re


# Input Moderation

def moderate_input(query):
    """
    Basic content safety moderation.
    Extendable for enterprise use.
    """

    banned_terms = [
        "hack",
        "exploit",
        "attack system",
        "bypass security",
        "illegal access"
    ]

    query_lower = query.lower()
    return not any(term in query_lower for term in banned_terms)


# Retrieval Confidence Check

def retrieval_confidence_check(results, min_top_score=0.30):

    if not results:
        return False

    top_score = results[0]["score"]

    # Minimum absolute confidence threshold
    return top_score >= min_top_score



# Citation Enforcement

def citation_check(answer):
    """
    Ensure answer includes source citation.
    """

    return "[Source" in answer


# Numeric Consistency Guardrail

def numeric_consistency_check(answer, context):
    """
    Prevents hallucinated numeric values.
    Ensures all numbers in answer exist in context.
    """

    context_numbers = set(re.findall(r'\d+\.?\d*', context))
    answer_numbers = set(re.findall(r'\d+\.?\d*', answer))

    return answer_numbers.issubset(context_numbers)