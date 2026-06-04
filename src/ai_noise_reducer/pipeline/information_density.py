from __future__ import annotations

import re


class InformationDensityEngine:
    def compute(self, text: str) -> tuple[float, dict[str, float]]:
        words = re.findall(r"\w+", text)
        if not words:
            return 0.0, {"unique_facts_per_word": 0.0, "entities_per_100_words": 0.0, "numerical_facts": 0.0}

        sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
        numerical = re.findall(r"\b\d+(?:\.\d+)?%?\b", text)
        entities = re.findall(r"\b[A-Z][a-zA-Z]{2,}\b", text)

        unique_claim_like = set(sentences)
        unique_facts_per_word = len(unique_claim_like) / max(len(words), 1)
        entities_per_100 = (len(entities) / max(len(words), 1)) * 100

        raw_density = (0.5 * unique_facts_per_word) + (0.3 * min(entities_per_100 / 10, 1.0)) + (
            0.2 * min(len(numerical) / max(len(sentences), 1), 1.0)
        )
        score = max(0.0, min(100.0, raw_density * 100))

        return score, {
            "unique_facts_per_word": unique_facts_per_word,
            "entities_per_100_words": entities_per_100,
            "numerical_facts": float(len(numerical)),
        }
