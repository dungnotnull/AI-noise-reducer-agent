from __future__ import annotations

import re


class EntityExtractor:
    def extract(self, text: str) -> list[str]:
        candidates = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", text)
        seen: set[str] = set()
        entities: list[str] = []
        for c in candidates:
            if len(c) < 3:
                continue
            if c not in seen:
                seen.add(c)
                entities.append(c)
        return entities[:200]
