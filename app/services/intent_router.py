class IntentRouter:
    def route(self, question: str) -> str:
        text = question.lower().strip()

        if any(
            word in text
            for word in ["price", "pricing", "cost", "quote", "quotation"]
        ):
            return "quote_request"

        if any(
            phrase in text
            for phrase in [
                "buy",
                "purchase",
                "hire",
                "order",
                "i want to get started",
            ]
        ):
            return "buying_intent"

        if any(
            word in text
            for word in [
                "service",
                "services",
                "software development",
                "web development",
                "app development",
                "chatbot",
            ]
        ):
            return "service_project"

        if any(
            word in text
            for word in ["weather", "joke", "recipe", "football", "fifa"]
        ):
            return "fallback"

        return "general_query"