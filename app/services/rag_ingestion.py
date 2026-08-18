import json
from pathlib import Path
from typing import Any


DATASET_PATH = Path(
    "data/raw/MoinSystems_AI_Public_Chatbot_RAG_Dataset_v2.jsonl"
)
DATASET_VERSION = "v2"

def normalize_text(value: Any) -> str:
    """Normalize text without changing its meaning."""
    if value is None:
        return ""

    return " ".join(str(value).split())


def normalize_record(record: dict) -> dict:
    """Normalize one RAG knowledge record."""
    return {
        "id": normalize_text(record.get("id")),
        "title": normalize_text(record.get("title")),
        "category": normalize_text(record.get("category")),
        "tags": normalize_text(record.get("tags")),
        "intents": normalize_text(record.get("intents")),
        "content": normalize_text(record.get("content")),
        "embedding_text": normalize_text(record.get("embedding_text")),
        "data_status": normalize_text(record.get("data_status")),
        "source_basis": normalize_text(record.get("source_basis")),
    }


def load_jsonl(path: Path = DATASET_PATH) -> list[dict]:
    """Load and normalize all records from the JSONL dataset."""
    records = []

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON on line {line_number}"
                ) from exc

            if not isinstance(record, dict):
                raise ValueError(
                    f"Line {line_number} is not a JSON object"
                )

            records.append(normalize_record(record))

    return records

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.knowledge_document import KnowledgeDocument
from app.models.knowledge_chunk import KnowledgeChunk


def ingest_knowledge_base(db: Session) -> int:
    """Load normalized JSONL records into the knowledge tables."""

    records = load_jsonl()

    source_name = DATASET_PATH.name

    # Find existing document/version
    document = db.scalar(
        select(KnowledgeDocument).where(
            KnowledgeDocument.source_name == source_name,
            KnowledgeDocument.version == DATASET_VERSION,
        )
    )

    if document is None:
        document = KnowledgeDocument(
            source_name=source_name,
            version=DATASET_VERSION,
            source_uri=str(DATASET_PATH),
            status="active",
        )
        db.add(document)
        db.flush()
    else:
        # Keep ingestion idempotent for the same dataset version.
        db.execute(
            delete(KnowledgeChunk).where(
                KnowledgeChunk.document_id == document.id
            )
        )

    for record in records:
        chunk = KnowledgeChunk(
            document_id=document.id,
            content=record["content"],
            category=record["category"] or None,
            tags=record["tags"] or None,
            intents=record["intents"] or None,
            embedding=None,
        )

        db.add(chunk)

    db.commit()

    return len(records)   