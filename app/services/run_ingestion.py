from app.db.database import SessionLocal
from app.services.rag_ingestion import ingest_knowledge_base


def main() -> None:
    db = SessionLocal()

    try:
        count = ingest_knowledge_base(db)
        print(f"Successfully ingested {count} knowledge records.")
    finally:
        db.close()


if __name__ == "__main__":
    main()