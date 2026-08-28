import requests

from app.core.config import settings
from app.services.llm.base import LLMProvider


class GeminiProvider(LLMProvider):
    """
    Gemini API provider using Google's REST API.
    """

    def __init__(self):
        api_key = settings.gemini_api_key

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")

        self.api_key = api_key

        self.url = (
            "https://generativelanguage.googleapis.com/"
            "v1beta/models/gemini-3.1-flash-lite:generateContent"
        )

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key,
        }

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": prompt,
                        }
                    ],
                }
            ]
        }

        if system_prompt:
            payload["system_instruction"] = {
                "parts": [
                    {
                        "text": system_prompt,
                    }
                ]
            }

        try:
            response = requests.post(
                self.url,
                headers=headers,
                json=payload,
                timeout=60,
            )

            response.raise_for_status()

            data = response.json()

            candidates = data.get("candidates", [])

            if not candidates:
                raise RuntimeError(
                    "Gemini returned no candidates."
                )

            content = candidates[0].get("content", {})
            parts = content.get("parts", [])

            for part in parts:
                text = part.get("text")

                if text:
                    return text

            raise RuntimeError(
                "Gemini returned no text response."
            )

        except Exception as exc:
            print("\n========== GEMINI ERROR ==========")
            print("ERROR TYPE:", type(exc).__name__)
            print("ERROR:", str(exc))

            if "response" in locals():
                print("STATUS:", response.status_code)
                print("BODY:", response.text)

            print("==================================\n")

            raise