from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256


@dataclass
class KnowledgeVersion:
    version_id: str
    created_at: datetime
    description: str


class KnowledgeVersioningService:
    def create_version(self, descriptor: str, content_fingerprint: str) -> KnowledgeVersion:
        token = sha256(f"{descriptor}:{content_fingerprint}:{datetime.utcnow().isoformat()}".encode()).hexdigest()[:16]
        return KnowledgeVersion(
            version_id=f"kv-{token}",
            created_at=datetime.utcnow(),
            description=descriptor,
        )
