from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class MetricsRegistry:
    counters: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    timings_ms: dict[str, list[float]] = field(default_factory=lambda: defaultdict(list))

    def inc(self, key: str, amount: int = 1) -> None:
        self.counters[key] += amount

    def observe(self, key: str, duration_ms: float) -> None:
        self.timings_ms[key].append(duration_ms)

    def snapshot(self) -> dict:
        return {
            "counters": dict(self.counters),
            "timings_ms_avg": {
                k: (sum(v) / len(v) if v else 0.0)
                for k, v in self.timings_ms.items()
            },
        }


class Timer:
    def __init__(self, registry: MetricsRegistry, key: str) -> None:
        self.registry = registry
        self.key = key
        self.start = 0.0

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        duration_ms = (time.perf_counter() - self.start) * 1000
        self.registry.observe(self.key, duration_ms)
