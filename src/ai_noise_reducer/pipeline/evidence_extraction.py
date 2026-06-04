from __future__ import annotations

import re

from ai_noise_reducer.domain_models import EvidenceItem


class EvidenceExtractor:
    def extract(self, text: str) -> list[EvidenceItem]:
        evidence: list[EvidenceItem] = []

        for number in re.findall(r"\b\d+(?:\.\d+)?%?\b", text):
            evidence.append(
                EvidenceItem(
                    text=f"Numerical claim: {number}",
                    kind="statistic",
                    value=number,
                    confidence=0.75,
                )
            )

        for quote in re.findall(r'"([^"]{10,300})"', text):
            evidence.append(
                EvidenceItem(
                    text=quote,
                    kind="quote",
                    value=quote[:120],
                    confidence=0.65,
                )
            )

        for citation in re.findall(r"\[(\d+)\]|\(([^)]+,\s?\d{4})\)", text):
            label = next((c for c in citation if c), "")
            evidence.append(
                EvidenceItem(
                    text=f"Citation detected: {label}",
                    kind="citation",
                    value=label,
                    confidence=0.8,
                )
            )

        return evidence
