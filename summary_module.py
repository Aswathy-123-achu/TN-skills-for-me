from gemini_client import gemini_generate


def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following educational text for quick revision.

Requirements:
- Keep the important facts.
- Use simple English.
- Prefer 5-8 short bullet points.
- Do not add information that is not in the text.

Text:
{text}
"""
    try:
        return gemini_generate(prompt)
    except RuntimeError as exc:
        return f"AI service is not ready: {exc}"
