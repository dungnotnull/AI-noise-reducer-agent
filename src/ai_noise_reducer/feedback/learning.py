from __future__ import annotations

from collections import Counter
from typing import Any

from ai_noise_reducer.domain_models import FeedbackRecord
from ai_noise_reducer.storage.postgres_repo import PostgresRepository


class FeedbackLearningService:
    def __init__(self) -> None:
        self.repo = PostgresRepository()

    def ingest(self, feedback: FeedbackRecord) -> dict[str, Any]:
        self.repo.save_feedback(feedback.model_dump(mode="json"))
        return {"status": "ingested", "feedback_id": feedback.feedback_id}

    def replay_as_benchmark(self, feedback_items: list[FeedbackRecord]) -> list[dict[str, Any]]:
        replay = []
        for f in feedback_items:
            replay.append(
                {
                    "benchmark_id": f"replay-{f.feedback_id}",
                    "task_type": "feedback_replay",
                    "expected": {"corrected_facts": f.corrected_facts},
                    "predicted": {"corrected_facts": []},
                    "latency_ms": 0.0,
                }
            )
        return replay

    def error_analysis(self, feedback_items: list[FeedbackRecord]) -> dict[str, Any]:
        severities = Counter(f.severity for f in feedback_items)
        correction_sizes = [len(f.corrected_facts) for f in feedback_items]
        return {
            "total_feedback": len(feedback_items),
            "severity_distribution": dict(severities),
            "avg_corrections_per_feedback": (sum(correction_sizes) / len(correction_sizes)) if correction_sizes else 0,
        }
