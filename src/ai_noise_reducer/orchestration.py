from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from hashlib import sha256

from ai_noise_reducer.domain_models import (
    ArticleAnalysisRequest,
    ArticleAnalysisResponse,
    BenchmarkRecord,
    FeedbackRecord,
    ScoreBundle,
)
from ai_noise_reducer.feedback.learning import FeedbackLearningService
from ai_noise_reducer.pipeline.citation_analysis import CitationAnalyzer
from ai_noise_reducer.pipeline.entity_extraction import EntityExtractor
from ai_noise_reducer.pipeline.evidence_extraction import EvidenceExtractor
from ai_noise_reducer.pipeline.extraction import WebExtractor
from ai_noise_reducer.pipeline.hard_fact_engine import HardFactEngine
from ai_noise_reducer.pipeline.information_density import InformationDensityEngine
from ai_noise_reducer.pipeline.slop_detection import AISlopDetector
from ai_noise_reducer.pipeline.source_credibility import SourceCredibilityScorer
from ai_noise_reducer.pipeline.trust_engine import TrustScoreEngine
from ai_noise_reducer.scale.analytics import AnalyticsPipeline
from ai_noise_reducer.scale.i18n import LocalizationService
from ai_noise_reducer.scale.observability import MetricsRegistry, Timer
from ai_noise_reducer.storage.postgres_repo import PostgresRepository


class AnalysisOrchestrator:
    def __init__(self) -> None:
        self.extractor = WebExtractor()
        self.slop = AISlopDetector()
        self.density = InformationDensityEngine()
        self.evidence = EvidenceExtractor()
        self.entities = EntityExtractor()
        self.hard_facts = HardFactEngine()
        self.citation = CitationAnalyzer()
        self.source = SourceCredibilityScorer()
        self.trust = TrustScoreEngine()

        self.metrics = MetricsRegistry()
        self.analytics = AnalyticsPipeline()
        self.i18n = LocalizationService()

        self.pg = PostgresRepository()
        self.feedback = FeedbackLearningService()

    async def analyze(self, req: ArticleAnalysisRequest, language: str = "en") -> ArticleAnalysisResponse:
        with Timer(self.metrics, "analysis.total_ms"):
            if req.url:
                text = await self.extractor.extract_from_url(str(req.url))
            else:
                text = self.extractor.extract_from_raw(req.raw_text or "")

            ai_slop_score = self.slop.score(text)
            density_score, _density_meta = self.density.compute(text)
            evidence_table = self.evidence.extract(text)
            entity_list = self.entities.extract(text)
            hard_facts, summary_60s, contradictions, missing_information = self.hard_facts.build(text, evidence_table)

            _citation_meta = self.citation.analyze(text)
            source_authority = self.source.score(req.source_name, str(req.url) if req.url else None)
            freshness = 70.0
            trust_score = self.trust.score(evidence_table, density_score, source_authority, freshness)

            localized_summary = self.i18n.localize_brief(summary_60s, language=language)

            self.analytics.emit(
                "analysis_completed",
                {
                    "source": req.source_name,
                    "has_url": bool(req.url),
                    "entities": len(entity_list),
                    "facts": len(hard_facts),
                },
            )
            self.metrics.inc("analysis.count")

            return ArticleAnalysisResponse(
                source_name=req.source_name,
                extracted_text=text,
                summary_60s=localized_summary,
                hard_facts=hard_facts,
                evidence_table=evidence_table,
                contradictions=contradictions,
                missing_information=missing_information,
                scores=ScoreBundle(
                    ai_slop_score=ai_slop_score,
                    information_density_score=density_score,
                    trust_score=trust_score,
                ),
                entities=entity_list,
            )

    def save_benchmark_record(self, benchmark: BenchmarkRecord) -> None:
        self.pg.save_benchmark(benchmark.model_dump(mode="json"))

    def ingest_feedback(self, feedback: FeedbackRecord) -> dict:
        return self.feedback.ingest(feedback)

    def status(self) -> dict:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": self.metrics.snapshot(),
            "analytics": self.analytics.aggregate(),
            "fingerprint": sha256(str(self.metrics.snapshot()).encode()).hexdigest()[:12],
        }

    def training_gate(self, baseline: float, candidate: float) -> bool:
        improvement = (candidate - baseline) / baseline if baseline > 0 else 1.0
        return improvement >= 0.10
