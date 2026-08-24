from app.services.llm.base import LLMProvider
from app.services.llm.prompts import SYSTEM_PROMPT
from app.services.retriever import retrieve_knowledge
from app.services.context_builder import build_context


class ChatService:
    """
    Connects retrieval, context building, and the LLM provider.
    """

    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    def answer(self, question: str) -> str:
        """
        Retrieve relevant knowledge and generate a grounded answer.
        """

        results = retrieve_knowledge(question)

        if not results:
            return (
                "I don't have enough information to answer "
                "that question."
            )

        context = build_context(results)

        prompt = f"""
Company Information:
{context}

User Question:
{question}
"""

        return self.llm_provider.generate(
            prompt,
            system_prompt=SYSTEM_PROMPT,
        )