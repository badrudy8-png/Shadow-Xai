"""Lightweight evaluation helpers for quality and regression checks."""

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class EvaluationCase:
    prompt: str
    expected_terms: tuple[str, ...]


@dataclass(frozen=True)
class EvaluationResult:
    prompt: str
    passed: bool
    score: float
    response: str


def evaluate(cases: list[EvaluationCase], respond: Callable[[str], str]) -> list[EvaluationResult]:
    results = []
    for case in cases:
        response = respond(case.prompt).lower()
        score = sum(term.lower() in response for term in case.expected_terms) / max(1, len(case.expected_terms))
        results.append(EvaluationResult(case.prompt, score == 1.0, score, response))
    return results
