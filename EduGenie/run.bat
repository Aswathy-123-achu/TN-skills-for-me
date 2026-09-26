@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Virtual environment not found.
  echo Please follow README.md setup steps first.
  pause
  exit /b 1
)
.venv\Scripts\python.exe -m uvicorn main:app --reload
pause
