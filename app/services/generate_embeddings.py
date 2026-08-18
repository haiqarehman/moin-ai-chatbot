from sentence_transformers import SentenceTransformer
from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.knowledge_chunk import KnowledgeChunk


MODEL_NAME = "all-MiniLM-L6-v2"


def generate_embeddings() -> None:
    model = SentenceTransformer(MODEL_NAME)

    db = SessionLocal()

    try:
        chunks = db.scalars(
            select(KnowledgeChunk)
            .where(KnowledgeChunk.embedding.is_(None))
        ).all()

        print(f"Chunks without embeddings: {len(chunks)}")

        if not chunks:
            print("All chunks already have embeddings.")
            return

        texts = [chunk.content for chunk in chunks]

        embeddings = model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

        for chunk, embedding in zip(chunks, embeddings):
            chunk.embedding = embedding.tolist()

        db.commit()

        print(f"Successfully generated embeddings for {len(chunks)} chunks.")

    finally:
        db.close()


if __name__ == "__main__":
    generate_embeddings()