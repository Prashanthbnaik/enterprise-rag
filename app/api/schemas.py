from pydantic import BaseModel
from typing import List


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    contexts: List[str]
    latency: float