"""
Uses a pre-trained Natural Language Inference model (default:
``cross-encoder/nli-distilroberta-base``) to judge whether each evidence
passage SUPPORTS, REFUTES, or provides NOT_ENOUGH_INFO for a given claim.
The module then aggregates passage-level verdicts into a single claim-level
verdict with a confidence score.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Optional

import numpy as np


@dataclass
class PassageVerdict:
    """Verdict for a single (claim, evidence) pair."""

    evidence: str
    label: str  # SUPPORTS | REFUTES | NOT_ENOUGH_INFO
    confidence: float
    scores: dict[str, float]


@dataclass
class ClaimVerdict:
    """Aggregated verdict across all evidence passages."""

    claim: str
    verdict: str
    confidence: float
    passage_verdicts: list[PassageVerdict]
    explanation: str


# Map model output indices → our label names.
# cross-encoder/nli-distilroberta-base uses: 0=contradiction, 1=entailment, 2=neutral
_NLI_ID_TO_LABEL = {0: "REFUTES", 1: "SUPPORTS", 2: "NOT_ENOUGH_INFO"}


class NliVerifier:
    """Verify a claim against evidence passages using an NLI cross-encoder."""

    def __init__(
        self,
        model_name: str = "cross-encoder/nli-distilroberta-base",
    ) -> None:
        try:
            from transformers import AutoModelForSequenceClassification, AutoTokenizer
            import torch
        except ImportError as exc:
            raise ImportError(
                "Install transformers & torch: pip install transformers torch"
            ) from exc

        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self._model.eval()
        self._device = "cuda" if torch.cuda.is_available() else "cpu"
        self._model.to(self._device)


    def verify_single(self, claim: str, evidence: str) -> PassageVerdict:
        """Return the verdict for one (claim, evidence) pair."""
        import torch

        inputs = self._tokenizer(
            claim,
            evidence,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True,
        ).to(self._device)

        with torch.no_grad():
            logits = self._model(**inputs).logits

        probs = torch.softmax(logits, dim=-1).cpu().numpy().flatten()
        pred_idx = int(np.argmax(probs))
        label = _NLI_ID_TO_LABEL[pred_idx]
        scores = {_NLI_ID_TO_LABEL[i]: float(probs[i]) for i in range(len(probs))}

        return PassageVerdict(
            evidence=evidence,
            label=label,
            confidence=float(probs[pred_idx]),
            scores=scores,
        )


    def verify(self, claim: str, evidences: list[str]) -> ClaimVerdict:
        """
        Verify a claim against multiple evidence passages and aggregate into
        a single verdict.
        """
        if not evidences:
            return ClaimVerdict(
                claim=claim,
                verdict="NOT_ENOUGH_INFO",
                confidence=1.0,
                passage_verdicts=[],
                explanation="No evidence passages provided.",
            )

        passage_verdicts = [self.verify_single(claim, e) for e in evidences]

        # Aggregate: majority-vote weighted by confidence
        label_scores: dict[str, float] = {
            "SUPPORTS": 0.0,
            "REFUTES": 0.0,
            "NOT_ENOUGH_INFO": 0.0,
        }
        for pv in passage_verdicts:
            label_scores[pv.label] += pv.confidence

        best_label = max(label_scores, key=lambda k: label_scores[k])
        total = sum(label_scores.values()) or 1.0
        best_confidence = label_scores[best_label] / total

        # Build explanation
        n = len(passage_verdicts)
        counts = {lab: sum(1 for pv in passage_verdicts if pv.label == lab) for lab in label_scores}
        explanation = (
            f"Analysed {n} evidence passage(s). "
            f"{counts.get('SUPPORTS', 0)} support(s), "
            f"{counts.get('REFUTES', 0)} refute(s), "
            f"{counts.get('NOT_ENOUGH_INFO', 0)} inconclusive. "
            f"Aggregated verdict: {best_label} "
            f"(confidence {best_confidence:.2%})."
        )

        return ClaimVerdict(
            claim=claim,
            verdict=best_label,
            confidence=round(best_confidence, 4),
            passage_verdicts=passage_verdicts,
            explanation=explanation,
        )
