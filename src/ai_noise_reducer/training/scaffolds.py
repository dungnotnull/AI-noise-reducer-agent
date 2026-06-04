from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TrainingGate:
    min_relative_improvement: float = 0.10

    def should_train(self, baseline_metric: float, candidate_metric: float) -> bool:
        if baseline_metric <= 0:
            return candidate_metric > 0
        improvement = (candidate_metric - baseline_metric) / baseline_metric
        return improvement >= self.min_relative_improvement


class AISlopDetectorTrainingScaffold:
    task_name = "ai_slop_detector"

    def build_dataset_spec(self) -> dict:
        return {"inputs": ["text"], "labels": ["slop_score"], "format": "jsonl"}


class FactDensityPredictorTrainingScaffold:
    task_name = "fact_density_predictor"

    def build_dataset_spec(self) -> dict:
        return {"inputs": ["text"], "labels": ["density_score"], "format": "jsonl"}


class TrustScorePredictorTrainingScaffold:
    task_name = "trust_score_predictor"

    def build_dataset_spec(self) -> dict:
        return {"inputs": ["evidence", "source_metadata", "density"], "labels": ["trust_score"], "format": "jsonl"}
