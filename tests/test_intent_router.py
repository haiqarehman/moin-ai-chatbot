from app.services.intent_router import IntentRouter


def test_routes_pricing_question():
    router = IntentRouter()

    assert router.route("How much does your software development cost?") == "quote_request"


def test_routes_service_question():
    router = IntentRouter()

    assert router.route("What services do you provide?") == "service_project"


def test_routes_buying_intent():
    router = IntentRouter()

    assert router.route("I want to hire your team") == "buying_intent"


def test_routes_unknown_question_to_fallback():
    router = IntentRouter()

    assert router.route("What is the weather in London?") == "fallback"


def test_routes_general_question():
    router = IntentRouter()

    assert router.route("Tell me about your company") == "general_query"
def test_pricing_intent_routes_to_quote_request():
    router = IntentRouter()

    result = router.route(
        "I need a quote for an AI chatbot project."
    )

    assert result == "quote_request"    