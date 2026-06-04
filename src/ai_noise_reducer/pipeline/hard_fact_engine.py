from __future__ import annotations

import re

from ai_noise_reducer.domain_models import EvidenceItem


class HardFactEngine:
    def build(
        self,
        text: str,
        evidence: list[EvidenceItem],
    ) -> tuple[list[str], str, list[str], list[str]]:
        sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
        strong = [s for s in sentences if self._is_fact_like(s)]

        hard_facts = strong[:20]

        summary_60s = " ".join(hard_facts[:5]) if hard_facts else (sentences[0] if sentences else "")
        contradictions = self._simple_contradictions(sentences)
        missing = self._missing_information_heuristics(text, evidence)

        return hard_facts, summary_60s, contradictions, missing

    def _is_fact_like(self, sentence: str) -> bool:
        has_number = bool(re.search(r"\b\d+(?:\.\d+)?%?\b", sentence))
        has_claim_verb = any(v in sentence.lower() for v in ["is", "are", "was", "were", "reported", "shows"])
        return has_number or has_claim_verb

    def _simple_contradictions(self, sentences: list[str]) -> list[str]:
        contradictions: list[str] = []
        for s in sentences[:200]:
            low = s.lower()
            if "no evidence" in low and "evidence" in low:
                contradictions.append(s)
            if "increased" in low and "decreased" in low:
                contradictions.append(s)
        return contradictions[:20]

    def _missing_information_heuristics(self, text: str, evidence: list[EvidenceItem]) -> list[str]:
        missing: list[str] = []
        lower = text.lower()
        if "methodology" not in lower:
            missing.append("Methodology details are missing.")
        if not any(e.kind == "citation" for e in evidence):
            missing.append("Supporting citations are missing.")
        if not any(e.kind == "statistic" for e in evidence):
            missing.append("Quantitative evidence is limited.")
        return missing
