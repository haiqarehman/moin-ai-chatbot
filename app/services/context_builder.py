from typing import Iterable


def build_context(results: Iterable) -> str:
    """
    Convert retrieved knowledge results into a clean context
    and remove duplicate content.
    """

    context_parts = []
    seen_contents = set()

    for index, result in enumerate(results, start=1):
        content = result.content.strip()

        # Skip duplicate content
        if content in seen_contents:
            continue

        seen_contents.add(content)

        context_parts.append(
            f"""Source {len(context_parts) + 1}
Category: {result.category}
Intent: {result.intents}
Content: {content}
"""
        )

    return "\n".join(context_parts)