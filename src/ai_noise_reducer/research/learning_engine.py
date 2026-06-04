from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Any

from ai_noise_reducer.domain_models import KnowledgeItem, SourceType
from ai_noise_reducer.knowledge.versioning import KnowledgeVersioningService
from ai_noise_reducer.logging import get_logger
from ai_noise_reducer.research.connectors import ACLConnector, ArxivConnector, SemanticScholarConnector
from ai_noise_reducer.storage.neo4j_repo import Neo4jRepository
from ai_noise_reducer.storage.qdrant_repo import QdrantRepository


logger = get_logger(__name__)


class ResearchLearningEngine:
    def __init__(self) -> None:
        self.arxiv = ArxivConnector()
        self.acl = ACLConnector()
        self.semantic = SemanticScholarConnector()
        self.versioning = KnowledgeVersioningService()
        self.qdrant = QdrantRepository()
        self.neo4j = Neo4jRepository()

    async def update(self, topic: str, limit: int = 5) -> dict[str, Any]:
        discovered = []
        discovered.extend(await self.arxiv.discover(topic, limit))
        discovered.extend(await self.acl.discover(topic, limit))
        discovered.extend(await self.semantic.discover(topic, limit))

        ingested = 0
        for item in discovered:
            knowledge = self._to_knowledge_item(item)
            embedding = self._fake_embedding(knowledge.summary, size=384)
            self.qdrant.upsert_knowledge_item(knowledge, embedding)
            self.neo4j.upsert_knowledge_item(knowledge)
            ingested += 1

        version = self.versioning.create_version(
            descriptor=f"research-update:{topic}",
            content_fingerprint=hashlib.sha256(str(discovered).encode()).hexdigest(),
        )

        logger.info("research_update_complete", topic=topic, ingested=ingested, version=version.version_id)

        return {
            "topic": topic,
            "ingested_items": ingested,
            "version_id": version.version_id,
            "updated_at": datetime.utcnow().isoformat(),
        }

    def _to_knowledge_item(self, raw: dict[str, Any]) -> KnowledgeItem:
        title = raw.get("title") or raw.get("query") or "Untitled Research Item"
        summary = raw.get("abstract") or raw.get("raw") or f"Discovered item from {raw.get('source', 'unknown')}"
        key_findings = [summary[:200]]
        item_id = hashlib.sha256(f"{title}:{raw.get('source')}:{summary[:64]}".encode()).hexdigest()[:24]
        return KnowledgeItem(
            id=item_id,
            source_type=SourceType.PAPER,
            source=raw.get("source", "unknown"),
            url=raw.get("url"),
            authors=[a.get("name", "") for a in raw.get("authors", []) if isinstance(a, dict)],
            date=datetime.utcnow(),
            category="research-learning",
            summary=summary[:1200],
            key_findings=key_findings,
            confidence=0.7,
            relevance=0.8,
            benchmark_impact=float(raw.get("citationCount", 0)) / 1000.0,
            metadata={"raw": raw},
        )

    def _fake_embedding(self, text: str, size: int = 384) -> list[float]:
        digest = hashlib.sha256(text.encode()).digest()
        out = []
        for i in range(size):
            out.append(((digest[i % len(digest)] / 255.0) * 2) - 1)
        return out
