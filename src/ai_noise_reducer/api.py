from __future__ import annotations

from fastapi import FastAPI

from ai_noise_reducer.benchmark.competitor_analysis import CompetitorAnalysisTemplate
from ai_noise_reducer.benchmark.evaluation import BenchmarkEvaluator
from ai_noise_reducer.domain_models import ArticleAnalysisRequest, BenchmarkRecord, FeedbackRecord
from ai_noise_reducer.logging import setup_logging
from ai_noise_reducer.orchestration import AnalysisOrchestrator
from ai_noise_reducer.research.learning_engine import ResearchLearningEngine
from ai_noise_reducer.training.scaffolds import (
    AISlopDetectorTrainingScaffold,
    FactDensityPredictorTrainingScaffold,
    TrainingGate,
    TrustScorePredictorTrainingScaffold,
)


setup_logging()
app = FastAPI(title="AI Noise Reducer Agent API", version="0.1.0")
orchestrator = AnalysisOrchestrator()
research_engine = ResearchLearningEngine()

benchmark_evaluator = BenchmarkEvaluator()
competitor_template = CompetitorAnalysisTemplate()
training_gate = TrainingGate()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(req: ArticleAnalysisRequest, language: str = "en"):
    return await orchestrator.analyze(req, language=language)


@app.post("/benchmark/record")
def save_benchmark(record: BenchmarkRecord):
    orchestrator.save_benchmark_record(record)
    return {"status": "saved", "benchmark_id": record.benchmark_id}


@app.post("/feedback")
def ingest_feedback(record: FeedbackRecord):
    return orchestrator.ingest_feedback(record)


@app.post("/benchmark/evaluate")
def evaluate(records: list[dict]):
    result = benchmark_evaluator.evaluate(records)
    return {
        "precision": result.precision,
        "recall": result.recall,
        "hallucination_rate": result.hallucination_rate,
        "avg_latency_ms": result.avg_latency_ms,
    }


@app.get("/competitor/template")
def competitor_analysis_template():
    return competitor_template.template()


@app.post("/research/update")
async def research_update(topic: str, limit: int = 5):
    return await research_engine.update(topic, limit=limit)


@app.get("/training/scaffolds")
def get_training_scaffolds():
    return {
        "ai_slop_detector": AISlopDetectorTrainingScaffold().build_dataset_spec(),
        "fact_density_predictor": FactDensityPredictorTrainingScaffold().build_dataset_spec(),
        "trust_score_predictor": TrustScorePredictorTrainingScaffold().build_dataset_spec(),
    }


@app.get("/training/gate")
def get_training_gate(baseline: float, candidate: float):
    return {
        "should_train": training_gate.should_train(baseline, candidate),
        "baseline": baseline,
        "candidate": candidate,
        "required_relative_improvement": training_gate.min_relative_improvement,
    }


@app.get("/status")
def status():
    return orchestrator.status()
