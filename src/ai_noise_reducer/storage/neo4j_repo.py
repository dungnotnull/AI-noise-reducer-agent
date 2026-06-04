from __future__ import annotations

from neo4j import GraphDatabase

from ai_noise_reducer.config import settings
from ai_noise_reducer.domain_models import KnowledgeItem


class Neo4jRepository:
    def __init__(self) -> None:
        self.driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        )

    def upsert_knowledge_item(self, item: KnowledgeItem) -> None:
        query = """
        MERGE (k:KnowledgeItem {id: $id})
        SET k.source = $source,
            k.category = $category,
            k.summary = $summary,
            k.confidence = $confidence,
            k.relevance = $relevance
        """
        with self.driver.session() as session:
            session.run(
                query,
                id=item.id,
                source=item.source,
                category=item.category,
                summary=item.summary,
                confidence=item.confidence,
                relevance=item.relevance,
            )

    def add_relation(self, from_id: str, to_id: str, relation: str = "RELATED_TO") -> None:
        query = f"""
        MATCH (a:KnowledgeItem {{id: $from_id}})
        MATCH (b:KnowledgeItem {{id: $to_id}})
        MERGE (a)-[:{relation}]->(b)
        """
        with self.driver.session() as session:
            session.run(query, from_id=from_id, to_id=to_id)

    def close(self) -> None:
        self.driver.close()
