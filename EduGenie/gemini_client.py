"""Gemini API client for EduGenie."""

import os
import time
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv

try:
    from google import genai
    from google.genai import errors
except ImportError:
    genai = None
    errors = None


# Load values from .env
load_dotenv()


# Default model
DEFAULT_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
).strip()


@lru_cache(maxsize=1)
def get_client():
    """Create and cache the Gemini client."""

    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Please add your Gemini API key to the .env file."
        )

    if genai is None:
        raise RuntimeError(
            "The google-genai package is not installed. "
            "Run: pip install -r requirements.txt"
        )

    return genai.Client(api_key=api_key)


def gemini_generate(
    prompt: str,
    *,
    model: Optional[str] = None
) -> str:
    """Generate text using Gemini."""

    client = get_client()

    selected_model = (
        model or DEFAULT_MODEL
    ).strip()

    if not selected_model:
        selected_model = "gemini-3.8-flash"

    # Try up to 3 times for temporary server errors
    max_attempts = 3

    for attempt in range(max_attempts):
        try:
            response = client.models.generate_content(
                model=selected_model,
                contents=prompt,
            )

            text = getattr(response, "text", None)

            if not text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return text.strip()

        except Exception as exc:

            # Check whether this is a temporary Gemini server error
            error_text = str(exc)

            is_temporary_error = (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "high demand" in error_text.lower()
                or "temporarily unavailable" in error_text.lower()
            )

            if is_temporary_error and attempt < max_attempts - 1:
                # Wait before trying again
                wait_time = 2 ** attempt
                time.sleep(wait_time)
                continue

            # Convert the Gemini error into a clean RuntimeError
            raise RuntimeError(
                f"Gemini API error: {error_text}"
            ) from exc

    raise RuntimeError(
        "Gemini service is temporarily unavailable. "
        "Please try again later."
    )