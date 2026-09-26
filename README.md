# EduGenie – Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant based on the supplied project
documentation. It provides:

- Question & Answer
- Simple concept explanation
- 3-question MCQ quiz generation
- Text summarization
- Personalized learning paths

## Stack

- Python 3.10+
- FastAPI + Uvicorn
- Jinja2 HTML templates
- HTML/CSS/JavaScript frontend
- Google Gemini through the `google-genai` SDK
- Optional local `LaMini-Flan-T5-783M` explanation model

## Quick start

### Windows PowerShell

```powershell
cd EduGenie
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

Open `.env` and replace the placeholder with your Gemini API key.

Then:

```powershell
uvicorn main:app --reload
```

Open http://127.0.0.1:8000

### Windows CMD

```cmd
cd EduGenie
py -3.11 -m venv .venv
.venv\Scriptsctivate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload
```

## API endpoints

- `GET /health`
- `POST /qa`
- `POST /explain`
- `POST /quiz`
- `POST /summarize`
- `POST /learn/recommendations`

Interactive API documentation is available at `/docs`.

## Optional local explanation model

The supplied documentation mentions LaMini-Flan-T5-783M. This implementation
supports it without making it mandatory for basic setup.

Install the optional packages:

```powershell
pip install torch transformers sentencepiece
```

Then set:

```text
ENABLE_LOCAL_EXPLAINER=true
```

The first explanation may take longer because the model needs to be downloaded.
If it cannot load, EduGenie automatically falls back to Gemini.

## Troubleshooting

### "AI service is not ready"
Check that `.env` exists beside `main.py` and contains a valid
`GEMINI_API_KEY`. Restart Uvicorn after changing `.env`.

### PowerShell blocks activation

You can avoid activation and run:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn main:app --reload
```

### Port 8000 is busy

```powershell
uvicorn main:app --reload --port 8001
```

Then open http://127.0.0.1:8001
