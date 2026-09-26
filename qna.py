from gemini_client import gemini_generate


def answer_question(question: str) -> str:
    prompt = f"""
You are EduGenie, a friendly educational assistant.
Answer the student's question accurately and clearly.

Rules:
- Use simple English.
- Give the direct answer first.
- Add a short explanation when useful.
- If the question is ambiguous, state the assumption.
- Do not invent facts.
- Keep the response concise.

Student question:
{question}
"""
    try:
        return gemini_generate(prompt)
    except RuntimeError as exc:
        return f"AI service is not ready: {exc}"
