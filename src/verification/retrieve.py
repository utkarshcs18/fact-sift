"""
Provides two retrieval strategies:
  1. TF-IDF cosine similarity (lightweight, no GPU needed)
  2. Sentence-Transformers dense retrieval (higher quality, needs model DL)

Both accept a claim string and a corpus of passages and return the top-k
most relevant passages with similarity scores.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List, Optional

import numpy as np


@dataclass
class RetrievedPassage:
    text: str
    score: float
    source: str = ""


class TfidfRetriever:
    def __init__(self) -> None:
        from sklearn.feature_extraction.text import TfidfVectorizer

        self._vectorizer = TfidfVectorizer(
            max_features=30_000, ngram_range=(1, 2), sublinear_tf=True
        )
        self._corpus_matrix = None
        self._corpus: list[str] = []

    def index(self, passages: list[str]) -> None:
        """Build the TF-IDF index from a list of passages."""
        self._corpus = passages
        self._corpus_matrix = self._vectorizer.fit_transform(passages)

    def retrieve(
        self, claim: str, top_k: int = 5
    ) -> list[RetrievedPassage]:
        if self._corpus_matrix is None:
            raise RuntimeError("Index is empty – call .index() first.")

        from sklearn.metrics.pairwise import cosine_similarity

        claim_vec = self._vectorizer.transform([claim])
        scores = cosine_similarity(claim_vec, self._corpus_matrix).flatten()
        top_idxs = np.argsort(scores)[::-1][:top_k]
        return [
            RetrievedPassage(
                text=self._corpus[i], score=float(scores[i]), source="tfidf"
            )
            for i in top_idxs
        ]


class DenseRetriever:

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise ImportError(
                "Install sentence-transformers: pip install sentence-transformers"
            ) from exc
        self._model = SentenceTransformer(model_name)
        self._corpus_embeddings: Optional[np.ndarray] = None
        self._corpus: list[str] = []

    def index(self, passages: list[str]) -> None:
        """Encode and store corpus embeddings."""
        self._corpus = passages
        self._corpus_embeddings = self._model.encode(
            passages, show_progress_bar=True, convert_to_numpy=True
        )

    def retrieve(
        self, claim: str, top_k: int = 5
    ) -> list[RetrievedPassage]:
        """Return the *top_k* passages most similar to *claim*."""
        if self._corpus_embeddings is None:
            raise RuntimeError("Index is empty – call .index() first.")

        from sklearn.metrics.pairwise import cosine_similarity

        claim_emb = self._model.encode([claim], convert_to_numpy=True)
        scores = cosine_similarity(claim_emb, self._corpus_embeddings).flatten()
        top_idxs = np.argsort(scores)[::-1][:top_k]
        return [
            RetrievedPassage(
                text=self._corpus[i], score=float(scores[i]), source="dense"
            )
            for i in top_idxs
        ]


def get_retriever(kind: str = "tfidf") -> TfidfRetriever | DenseRetriever:
    """Return a retriever instance by name."""
    if kind == "tfidf":
        return TfidfRetriever()
    elif kind == "dense":
        return DenseRetriever()
    else:
        raise ValueError(f"Unknown retriever kind: {kind!r}")
