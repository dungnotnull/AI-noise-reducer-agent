from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class SourceType(str, Enum):
    WEBPAGE = "webpage"
    PAPER = "paper"
    USER_FEEDBACK = "user_feedback"


class ScoreBundle(BaseModel):
    ai_slop_score: float = Field(ge=0, le=100)
    information_density_score: float = Field(ge=0, le=100)
    trust_score: float = Field(ge=0, le=100)


class EvidenceItem(BaseModel):
    text: str
    kind: str
    value: str | None = None
    source_ref: str | None = None
    confidence: float = Field(default=0.5, ge=0, le=1)


class KnowledgeItem(BaseModel):
    id: str
    source_type: SourceType
    source: str
    url: HttpUrl | None = None
    authors: list[str] = Field(default_factory=list)
    date: datetime | None = None
    category: str
    summary: str
    key_findings: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0, le=1)
    relevance: float = Field(default=0.5, ge=0, le=1)
    benchmark_impact: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)


class ArticleAnalysisRequest(BaseModel):
    url: HttpUrl | None = None
    raw_text: str | None = None
    source_name: str = "web_input"


class ArticleAnalysisResponse(BaseModel):
    source_name: str
    extracted_text: str
    summary_60s: str
    hard_facts: list[str]
    evidence_table: list[EvidenceItem]
    contradictions: list[str]
    missing_information: list[str]
    scores: ScoreBundle
    entities: list[str]


class BenchmarkRecord(BaseModel):
    benchmark_id: str
    task_type: str
    expected: dict[str, Any]
    predicted: dict[str, Any]
    latency_ms: float
    created_at: datetime = Field(default_factory=datetime.utcnow)


class FeedbackRecord(BaseModel):
    feedback_id: str
    analysis_id: str
    user_comment: str
    corrected_facts: list[str] = Field(default_factory=list)
    severity: str = "medium"
    created_at: datetime = Field(default_factory=datetime.utcnow)
