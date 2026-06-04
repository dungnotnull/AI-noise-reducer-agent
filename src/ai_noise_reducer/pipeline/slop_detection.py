from __future__ import annotations

import math
import re
from collections import Counter


class AISlopDetector:
    GENERIC_PATTERNS = [
        "in today's fast-paced world",
        "it is important to note",
        "delve into",
        "ever-evolving landscape",
        "in conclusion",
    ]

    def score(self, text: str) -> float:
        tokens = self._tokenize(text)
        if not tokens:
            return 100.0

        repetition_ratio = self._repetition_ratio(tokens)
        lexical_diversity = self._lexical_diversity(tokens)
        entropy = self._entropy(tokens)
        generic_penalty = self._generic_pattern_ratio(text)

        # Higher score => more slop
        score = (
            40 * repetition_ratio
            + 30 * (1 - lexical_diversity)
            + 20 * (1 - min(entropy / 8, 1))
            + 10 * generic_penalty
        )
        return max(0.0, min(100.0, score * 100 / 40))

    def _tokenize(self, text: str) -> list[str]:
        return re.findall(r"[a-zA-Z0-9]+", text.lower())

    def _repetition_ratio(self, tokens: list[str]) -> float:
        counts = Counter(tokens)
        repeated = sum(c for c in counts.values() if c > 1)
        return repeated / max(len(tokens), 1)

    def _lexical_diversity(self, tokens: list[str]) -> float:
        return len(set(tokens)) / max(len(tokens), 1)

    def _entropy(self, tokens: list[str]) -> float:
        counts = Counter(tokens)
        total = len(tokens)
        return -sum((c / total) * math.log2(c / total) for c in counts.values())

    def _generic_pattern_ratio(self, text: str) -> float:
        lower = text.lower()
        hits = sum(1 for p in self.GENERIC_PATTERNS if p in lower)
        return hits / max(len(self.GENERIC_PATTERNS), 1)
