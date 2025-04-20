@echo off
echo 🚀 Starting FastAPI server...
cd backend
call venv\Scripts\activate
uvicorn main:app --reload
pause
