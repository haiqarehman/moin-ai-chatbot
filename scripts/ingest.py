import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import json
from uuid import uuid4

from sqlalchemy import text

from app.db.database import SessionLocal
from app.models.knowledge_chunk import KnowledgeChunk


DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "MoinSystems_AI_Public_Chatbot_RAG_Dataset_v2.jsonl"
)

SOURCE_NAME = "MoinSystems_AI_Public_Chatbot_RAG_Dataset_v2.jsonl"
DATASET_VERSION = "v2"


def load_dataset():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {DATASET_PATH}"
        )

    records = []

    with DATASET_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:

        for line_number, line in enumerate(file, start=1):

            line = line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)

            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc

            required_fields = [
                "id",
                "title",
                "category",
                "tags",
                "intents",
                "content",
            ]

            missing_fields = [
                field
                for field in required_fields
                if field not in record
            ]

            if missing_fields:
                raise ValueError(
                    f"Line {line_number} is missing fields: "
                    f"{missing_fields}"
                )

            records.append(record)

    return records


def ingest():
    print()
    print("=" * 50)
    print("RAG INGESTION")
    print("=" * 50)
    print()

    print(f"Dataset path: {DATASET_PATH}")

    records = load_dataset()

    print(f"Dataset records: {len(records)}")

    db = SessionLocal()

    try:
        existing_document = db.execute(
            text(
                """
                SELECT id
                FROM knowledge_document
                WHERE source_name = :source_name
                  AND version = :version
                LIMIT 1
                """
            ),
            {
                "source_name": SOURCE_NAME,
                "version": DATASET_VERSION,
            },
        ).fetchone()

        if existing_document:

            document_id = existing_document.id

            print(
                f"Existing document found: {document_id}"
            )

            db.execute(
                text(
                    """
                    DELETE FROM knowledge_chunk
                    WHERE document_id = :document_id
                    """
                ),
                {
                    "document_id": document_id,
                },
            )

            print(
                "Existing chunks removed for re-indexing."
            )

        else:

            document_id = uuid4()

            db.execute(
                text(
                    """
                    INSERT INTO knowledge_document
                    (
                        id,
                        source_name,
                        version,
                        source_uri,
                        status,
                        created_at
                    )
                    VALUES
                    (
                        :id,
                        :source_name,
                        :version,
                        :source_uri,
                        :status,
                        CURRENT_TIMESTAMP
                    )
                    """
                ),
                {
                    "id": document_id,
                    "source_name": SOURCE_NAME,
                    "version": DATASET_VERSION,
                    "source_uri": str(DATASET_PATH),
                    "status": "active",
                },
            )

            print(
                f"Created knowledge document: {document_id}"
            )

        inserted = 0

        for record in records:

            chunk = KnowledgeChunk(
                id=uuid4(),
                document_id=document_id,
                content=record["content"],
                embedding=None,
                category=record.get("category"),
                tags=record.get("tags"),
                intents=record.get("intents"),
            )

            db.add(chunk)

            inserted += 1

        db.commit()

        print()
        print(f"Inserted chunks: {inserted}")
        print()
        print("RAG ingestion completed successfully! ✅")
        print()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    ingest()