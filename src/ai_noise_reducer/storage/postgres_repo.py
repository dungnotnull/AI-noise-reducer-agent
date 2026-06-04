from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, Column, Float, MetaData, String, Table, create_engine, insert

from ai_noise_reducer.config import settings


metadata = MetaData()

benchmark_table = Table(
    "benchmark_records",
    metadata,
    Column("benchmark_id", String, primary_key=True),
    Column("task_type", String, nullable=False),
    Column("expected", JSON, nullable=False),
    Column("predicted", JSON, nullable=False),
    Column("latency_ms", Float, nullable=False),
)

feedback_table = Table(
    "feedback_records",
    metadata,
    Column("feedback_id", String, primary_key=True),
    Column("analysis_id", String, nullable=False),
    Column("user_comment", String, nullable=False),
    Column("corrected_facts", JSON, nullable=False),
    Column("severity", String, nullable=False),
)


class PostgresRepository:
    def __init__(self, dsn: str | None = None) -> None:
        self.engine = create_engine(dsn or settings.postgres_dsn, future=True)

    def ensure_schema(self) -> None:
        metadata.create_all(self.engine)

    def save_benchmark(self, payload: dict[str, Any]) -> None:
        with self.engine.begin() as conn:
            conn.execute(insert(benchmark_table).values(**payload))

    def save_feedback(self, payload: dict[str, Any]) -> None:
        with self.engine.begin() as conn:
            conn.execute(insert(feedback_table).values(**payload))
