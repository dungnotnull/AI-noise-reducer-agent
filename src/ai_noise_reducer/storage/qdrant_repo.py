from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from ai_noise_reducer.config import settings
from ai_noise_reducer.domain_models import KnowledgeItem


class QdrantRepository:
    def __init__(self, url: str | None = None, collection: str | None = None) -> None:
        self.client = QdrantClient(url=url or settings.qdrant_url)
        self.collection = collection or settings.qdrant_collection

    def ensure_collection(self, vector_size: int = 384) -> None:
        self.client.recreate_collection(
            collection_name=self.collection,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

    def upsert_knowledge_item(self, item: KnowledgeItem, embedding: list[float]) -> None:
        payload = item.model_dump(mode="json")
        self.client.upsert(
            collection_name=self.collection,
            points=[
                PointStruct(
                    id=item.id,
                    vector=embedding,
                    payload=payload,
                )
            ],
        )
