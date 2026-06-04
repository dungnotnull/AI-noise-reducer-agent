from __future__ import annotations

from ai_noise_reducer.domain_models import EvidenceItem


class TrustScoreEngine:
    def score(
        self,
        evidence: list[EvidenceItem],
        information_density_score: float,
        source_authority: float,
        freshness: float,
    ) -> float:
        evidence_quality = self._evidence_quality(evidence)
        citation_quality = self._citation_quality(evidence)

        trust = (
            0.35 * evidence_quality
            + 0.25 * citation_quality
            + 0.20 * information_density_score
            + 0.10 * source_authority
            + 0.10 * freshness
        )
        return max(0.0, min(100.0, trust))

    def _evidence_quality(self, evidence: list[EvidenceItem]) -> float:
        if not evidence:
            return 0.0
        return min(100.0, 100 * (sum(e.confidence for e in evidence) / len(evidence)))

    def _citation_quality(self, evidence: list[EvidenceItem]) -> float:
        if not evidence:
            return 0.0
        cites = [e for e in evidence if e.kind == "citation"]
        if not cites:
            return 10.0
        return min(100.0, 40 + 60 * (sum(e.confidence for e in cites) / len(cites)))
