from gemini_client import gemini_generate


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
Create a personalized learning path for: {topic}

Use simple English and this structure:
- Goal
- Beginner: 3-5 topics
- Intermediate: 3-5 topics
- Advanced: 3-5 topics
- Suggested 4-week timeline
- Practice ideas
- Useful resource types (official docs, tutorials, books, videos)

Do not invent exact URLs. Explain what the learner should search for.
"""
    try:
        return gemini_generate(prompt)
    except RuntimeError as exc:
        return f"AI service is not ready: {exc}"
