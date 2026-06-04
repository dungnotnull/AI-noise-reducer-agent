from __future__ import annotations

from urllib.parse import urlparse


class SourceCredibilityScorer:
    HIGH_TRUST_DOMAINS = {
        "nature.com": 95,
        "science.org": 95,
        "arxiv.org": 85,
        "aclweb.org": 88,
        "semanticscholar.org": 82,
        "openai.com": 85,
        "deepmind.google": 88,
        "anthropic.com": 85,
    }

    def score(self, source_name: str, url: str | None = None) -> float:
        if url:
            domain = urlparse(url).netloc.lower().replace("www.", "")
            for trusted_domain, val in self.HIGH_TRUST_DOMAINS.items():
                if trusted_domain in domain:
                    return float(val)
            if domain.endswith(".gov") or domain.endswith(".edu"):
                return 80.0
            if domain.endswith(".org"):
                return 70.0
            return 50.0
        if source_name.lower() in {"arxiv", "acl", "semantic scholar"}:
            return 85.0
        return 55.0
