from __future__ import annotations

from typing import Any

import httpx


class BaseConnector:
    async def discover(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        raise NotImplementedError


class ArxivConnector(BaseConnector):
    API_URL = "http://export.arxiv.org/api/query"

    async def discover(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        params = {"search_query": query, "start": 0, "max_results": limit}
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(self.API_URL, params=params)
            response.raise_for_status()
        return [{"source": "arXiv", "raw": response.text[:5000], "query": query}]


class ACLConnector(BaseConnector):
    async def discover(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        return [{"source": "ACL", "query": query, "title": f"ACL discovery placeholder for {query}", "limit": limit}]


class SemanticScholarConnector(BaseConnector):
    API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

    async def discover(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        params = {"query": query, "limit": limit, "fields": "title,authors,year,abstract,url,citationCount"}
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(self.API_URL, params=params)
            response.raise_for_status()
            data = response.json()
        papers = data.get("data", [])
        return [{"source": "Semantic Scholar", **p} for p in papers]
