from sentence_transformers import SentenceTransformer
from sqlalchemy import text

from app.db.database import SessionLocal


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def retrieve_knowledge(
    query: str,
    top_k: int = 3,
    threshold: float = 0.40,
    category: str | None = None,
    intent: str | None = None,
):
    """
    Search the knowledge base and return relevant
    knowledge chunks for the user's question.

    Also prints retrieval information for debugging.
    """

    query_embedding = model.encode(
        query,
        normalize_embeddings=True,
    ).tolist()

    db = SessionLocal()

    try:
        conditions = ["embedding IS NOT NULL"]

        params = {
            "query_embedding": str(query_embedding),
            "top_k": top_k,
        }

        if category:
            conditions.append("category = :category")
            params["category"] = category

        if intent:
            conditions.append("intents ILIKE :intent")
            params["intent"] = f"%{intent}%"

        where_clause = " AND ".join(conditions)

        sql = text(
            f"""
            SELECT
                id,
                content,
                category,
                tags,
                intents,
                1 - (embedding <=> CAST(:query_embedding AS vector))
                    AS similarity
            FROM knowledge_chunk
            WHERE {where_clause}
            ORDER BY embedding <=> CAST(:query_embedding AS vector)
            LIMIT :top_k
            """
        )

        results = db.execute(sql, params).fetchall()

        filtered_results = [
            result
            for result in results
            if result.similarity >= threshold
        ]

        # Retrieval tracing for debugging
        print("\n--- Retrieval Trace ---")
        print(f"Query: {query}")
        print(f"Top-K: {top_k}")
        print(f"Threshold: {threshold}")
        print(f"Retrieved: {len(filtered_results)}")

        for result in filtered_results:
            print(
                f"ID: {result.id} | "
                f"Score: {result.similarity:.4f} | "
                f"Category: {result.category}"
            )

        print("--- End Retrieval Trace ---\n")

        return filtered_results

    finally:
        db.close()