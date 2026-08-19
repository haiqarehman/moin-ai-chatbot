import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.retriever import retrieve_knowledge


def test_relevant_company_question_returns_results():
    results = retrieve_knowledge("What is MoinSystems AI?")
    assert len(results) > 0


def test_relevant_service_question_returns_results():
    results = retrieve_knowledge(
        "What services does MoinSystems AI offer?"
    )
    assert len(results) > 0


def test_pricing_question_returns_results():
    results = retrieve_knowledge(
        "How much does your software development service cost?"
    )
    assert len(results) > 0


def test_unrelated_weather_question_returns_no_results():
    results = retrieve_knowledge(
        "What is the weather in London today?"
    )
    assert len(results) == 0


def test_category_filter_returns_only_requested_category():
    results = retrieve_knowledge(
        "What services does MoinSystems AI provide?",
        category="service",
    )

    assert len(results) > 0

    for result in results:
        assert result.category == "service"


def test_intent_filter_returns_matching_intent():
    results = retrieve_knowledge(
        "I want to know about your AI chatbot services",
        intent="service_discovery",
        threshold=0.40,
    )

    assert len(results) > 0

    for result in results:
        assert "service_discovery" in result.intents