from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from fastapi.templating import Jinja2Templates

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie",
    description="Google Gemini powered learning assistant",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)


class QuizRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)


class QARequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=10000)


def clean_input(value: str) -> str:
    return value.strip()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa")
async def qa(payload: QARequest):
    return {"answer": answer_question(clean_input(payload.question))}


@app.post("/explain")
async def explain(payload: TextRequest):
    return {"explanation": explain_topic(clean_input(payload.text))}


@app.post("/quiz")
async def quiz(payload: QuizRequest):
    return {"quiz": generate_quiz(clean_input(payload.text))}


@app.post("/summarize")
async def summarize(payload: TextRequest):
    return {"summary": summarize_text(clean_input(payload.text))}


@app.post("/learn/recommendations")
async def recommendations(payload: TextRequest):
    return {"recommendations": get_learning_recommendations(clean_input(payload.text))}
