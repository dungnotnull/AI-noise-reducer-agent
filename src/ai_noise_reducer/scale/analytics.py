from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass
class AnalyticsEvent:
    name: str
    payload: dict


class AnalyticsPipeline:
    def __init__(self) -> None:
        self.events: list[AnalyticsEvent] = []

    def emit(self, name: str, payload: dict) -> None:
        self.events.append(AnalyticsEvent(name=name, payload=payload))

    def aggregate(self) -> dict:
        counts = Counter(e.name for e in self.events)
        return {
            "event_counts": dict(counts),
            "total_events": len(self.events),
        }
