from __future__ import annotations

import re

import httpx
import trafilatura

from ai_noise_reducer.config import settings


class WebExtractor:
    def __init__(self) -> None:
        self.timeout = settings.request_timeout_seconds

    async def extract_from_url(self, url: str) -> str:
        async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
            html = response.text
        extracted = trafilatura.extract(html, include_links=False, include_images=False)
        if not extracted:
            extracted = self._fallback_strip_html(html)
        return self._normalize(extracted)

    def extract_from_raw(self, raw_text: str) -> str:
        return self._normalize(raw_text)

    def _fallback_strip_html(self, html: str) -> str:
        text = re.sub(r"<[^>]+>", " ", html)
        return re.sub(r"\s+", " ", text).strip()

    def _normalize(self, text: str) -> str:
        compact = re.sub(r"\s+", " ", text).strip()
        words = compact.split()
        if len(words) > settings.max_article_words:
            words = words[: settings.max_article_words]
        return " ".join(words)
