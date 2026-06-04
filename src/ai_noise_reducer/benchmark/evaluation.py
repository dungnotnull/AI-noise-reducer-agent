from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class EvaluationResult:
    precision: float
    recall: float
    hallucination_rate: float
    avg_latency_ms: float


class BenchmarkEvaluator:
    def evaluate(self, records: list[dict[str, Any]]) -> EvaluationResult:
        if not records:
            return EvaluationResult(0.0, 0.0, 1.0, 0.0)

        precisions = []
        recalls = []
        latencies = []

        for r in records:
            expected = set(r.get("expected", {}).get("facts", []))
            predicted = set(r.get("predicted", {}).get("facts", []))

            tp = len(expected.intersection(predicted))
            fp = len(predicted - expected)
            fn = len(expected - predicted)

            precision = tp / (tp + fp) if (tp + fp) else 0.0
            recall = tp / (tp + fn) if (tp + fn) else 0.0

            precisions.append(precision)
            recalls.append(recall)
            latencies.append(float(r.get("latency_ms", 0.0)))

        precision_avg = sum(precisions) / len(precisions)
        recall_avg = sum(recalls) / len(recalls)
        hallucination = max(0.0, 1 - precision_avg)
        avg_latency = sum(latencies) / len(latencies)

        return EvaluationResult(
            precision=precision_avg,
            recall=recall_avg,
            hallucination_rate=hallucination,
            avg_latency_ms=avg_latency,
        )
