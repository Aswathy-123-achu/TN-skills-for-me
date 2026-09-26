"""Concept explanation module.

The original documentation specifies LaMini-Flan-T5-783M. The local model is
loaded only when ENABLE_LOCAL_EXPLAINER=true so first-time startup remains fast.
If the local model is unavailable, EduGenie safely uses Gemini instead.
"""

import os
from functools import lru_cache

from gemini_client import gemini_generate


@lru_cache(maxsize=1)
def _load_local_model():
    if os.getenv("ENABLE_LOCAL_EXPLAINER", "false").lower() != "true":
        return None

    try:
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        import torch
    except ImportError:
        return None

    model_name = os.getenv(
        "LOCAL_EXPLAINER_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M",
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model, torch


def _local_explain(topic: str):
    loaded = _load_local_model()
    if loaded is None:
        return None

    tokenizer, model, torch = loaded
    prompt = (
        "Explain this topic to a beginner in simple English. "
        "Use a short definition, 3 key points, and one example. Topic: "
        + topic
    )
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=220)
    return tokenizer.decode(output[0], skip_special_tokens=True).strip()


def explain_topic(topic: str) -> str:
    try:
        local = _local_explain(topic)
        if local:
            return local
    except Exception:
        # A local model can fail because of RAM, model download, or torch setup.
        # Falling back to Gemini keeps the application usable.
        pass

    prompt = f"""
Explain the following educational topic for a beginner.

Topic: {topic}

Use this structure:
1. Simple definition
2. How it works
3. 3 important points
4. One easy real-life/example
5. One-line recap

Use simple English and avoid unnecessary technical words.
"""
    try:
        return gemini_generate(prompt)
    except RuntimeError as exc:
        return f"AI service is not ready: {exc}"
