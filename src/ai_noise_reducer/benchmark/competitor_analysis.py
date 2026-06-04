from __future__ import annotations

from typing import Any


class CompetitorAnalysisTemplate:
    def template(self) -> dict[str, Any]:
        return {
            "competitors": [
                {
                    "name": "Generic summarizer",
                    "strengths": ["Fluent summaries", "Fast output"],
                    "weaknesses": ["Low evidence grounding", "No trust score"],
                    "positioning_gap": "Evidence-first fact extraction and trust scoring",
                },
                {
                    "name": "SEO content detector",
                    "strengths": ["Spam pattern identification"],
                    "weaknesses": ["Weak hard-fact extraction", "No knowledge memory"],
                    "positioning_gap": "Integrated density + evidence + memory graph",
                },
            ],
            "moat": [
                "Knowledge accumulation",
                "Benchmark-driven continuous learning",
                "Traceable evidence graph",
                "Trust scoring pipeline",
            ],
        }
