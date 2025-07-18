@echo off
REM kvizAI Project Setup Script for Windows
echo 🚀 Setting up kvizAI Project...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.11+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ first.
    pause
    exit /b 1
)

echo ✅ Python and Node.js are installed

REM Backend Setup
echo 📦 Setting up Backend...
cd backend

REM Create virtual environment
python -m venv venv
echo ✅ Virtual environment created

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install Python dependencies
pip install -r requirements.txt
echo ✅ Python dependencies installed

REM Create .env file from example
if not exist .env (
    copy env.example .env
    echo ✅ Environment file created (update .env with your settings)
)

cd ..

REM Frontend Setup
echo 📦 Setting up Frontend...
cd frontend

REM Install Node.js dependencies
npm install
echo ✅ Node.js dependencies installed

REM Create .env file from example
if not exist .env (
    copy env.example .env
    echo ✅ Environment file created (update .env with your settings)
)

cd ..

echo.
echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Update backend\.env with your configuration
echo 2. Update frontend\.env with your configuration
echo 3. Install Ollama from https://ollama.ai
echo 4. Pull Llama 2 model: ollama pull llama2:7b
echo.
echo To start development:
echo Backend: cd backend ^&^& venv\Scripts\activate ^&^& uvicorn main:app --reload
echo Frontend: cd frontend ^&^& npm run dev
echo.
echo Happy coding! 🚀
pause 