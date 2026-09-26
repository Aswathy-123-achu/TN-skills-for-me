import json
import re
from typing import Any

from gemini_client import gemini_generate


def clean_json_block(text: str) -> str:
    """Remove markdown fences and return the JSON-looking portion."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    match = re.search(r"(\{.*\}|\[.*\])", cleaned, flags=re.DOTALL)
    return match.group(1) if match else cleaned


def _fallback_quiz(message: str) -> list[dict[str, Any]]:
    return [{
        "question": "Quiz could not be generated yet.",
        "options": ["Configure Gemini API", "Try again", "Check .env", "All of these"],
        "answer": "All of these",
        "explanation": message,
    }]


def generate_quiz(passage: str) -> list[dict[str, Any]]:
    prompt = f"""
Create exactly 3 multiple-choice questions from the passage below.

Return ONLY valid JSON in this exact shape:
[
  {{
    "question": "question text",
    "options": ["A", "B", "C", "D"],
    "answer": "the exact correct option text",
    "explanation": "one short explanation"
  }}
]

Rules:
- Exactly 3 questions.
- Exactly 4 options per question.
- Questions must be answerable from the passage.
- Make distractors plausible.
- No markdown or extra text.

Passage:
{passage}
"""
    try:
        raw = gemini_generate(prompt)
        data = json.loads(clean_json_block(raw))
        if not isinstance(data, list) or len(data) != 3:
            raise ValueError("Gemini did not return exactly 3 questions.")
        for item in data:
            if not all(k in item for k in ("question", "options", "answer", "explanation")):
                raise ValueError("Quiz item has missing fields.")
            if not isinstance(item["options"], list) or len(item["options"]) != 4:
                raise ValueError("Each quiz question must have 4 options.")
        return data
    except (RuntimeError, ValueError, json.JSONDecodeError) as exc:
        return _fallback_quiz(str(exc))
