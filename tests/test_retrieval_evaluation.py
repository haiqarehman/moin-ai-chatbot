import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.retriever import retrieve_knowledge


tests = [
    {
        "name": "Company information",
        "query": "What is MoinSystems AI?",
        "should_have_results": True,
    },
    {
        "name": "Services",
        "query": "What services does MoinSystems AI offer?",
        "should_have_results": True,
    },
    {
        "name": "Pricing",
        "query": "How much does your software development service cost?",
        "should_have_results": True,
    },
    {
        "name": "Weather",
        "query": "What is the weather in London today?",
        "should_have_results": False,
    },
    {
        "name": "FIFA",
        "query": "Who won the FIFA World Cup in 2022?",
        "should_have_results": False,
    },
    {
        "name": "Chocolate cake",
        "query": "Give me a recipe for chocolate cake.",
        "should_have_results": False,
    },
]


def run_tests():
    print("\n========== RAG RETRIEVAL EVALUATION ==========\n")

    passed = 0

    for test in tests:
        print(f"Test: {test['name']}")
        print(f"Question: {test['query']}")

        results = retrieve_knowledge(test["query"])

        has_results = len(results) > 0

        if has_results == test["should_have_results"]:
            print("Result: PASS")
            passed += 1
        else:
            print("Result: FAIL")

        print(f"Retrieved results: {len(results)}")
        print("-" * 50)

    print("\n========== SUMMARY ==========")
    print(f"Passed: {passed}/{len(tests)}")

    if passed == len(tests):
        print("All retrieval tests passed!")
    else:
        print("Some retrieval tests need review.")


if __name__ == "__main__":
    run_tests()