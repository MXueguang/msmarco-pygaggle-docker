import sys

sys.path.insert(0, '../pygaggle/')

from fastapi import FastAPI
from pygaggle.rerank.base import Query, Text
from pygaggle.rerank.transformer import MonoBERT
from pydantic import BaseModel
from typing import List


reranker = MonoBERT()
app = FastAPI()


class Passage(BaseModel):
    docid: str
    text: str


class RerankRequest(BaseModel):
    query: str
    passages: List[Passage]


@app.post("/rerank/")
def rerank(rerank_request: RerankRequest):
    query = rerank_request.query
    passages = rerank_request.passages
    texts = [Text(p.text, "", {'docid': p.docid}, 0) for p in passages]
    reranked = reranker.rerank(query, texts)
    reranked.sort(key=lambda x: x.score, reverse=True)
    results = [{'docid': t.metadata["docid"], 'score': t.score} for t in reranked]
    return {'results': results}

