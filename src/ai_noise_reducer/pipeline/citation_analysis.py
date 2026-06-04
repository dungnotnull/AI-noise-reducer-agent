from __future__ import annotations

import re


class CitationAnalyzer:
    def analyze(self, text: str) -> dict[str, float]:
        bracket_citations = re.findall(r"\[\d+\]", text)
        author_year_citations = re.findall(r"\([A-Z][A-Za-z]+(?: et al\.)?,\s?\d{4}\)", text)

        total = len(bracket_citations) + len(author_year_citations)
        words = max(len(re.findall(r"\w+", text)), 1)

        citation_density = total / words * 1000
        citation_quality = min(100.0, 20.0 + citation_density * 8.0)

        return {
            "citation_count": float(total),
            "citation_density_per_1k_words": citation_density,
            "citation_quality_score": citation_quality,
        }
