#!/bin/bash

# kvizAI Project Setup Script
echo "🚀 Setting up kvizAI Project..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

echo "✅ Python and Node.js are installed"

# Backend Setup
echo "📦 Setting up Backend..."
cd backend

# Create virtual environment
python3 -m venv venv
echo "✅ Virtual environment created"

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
echo "✅ Python dependencies installed"

# Create .env file from example
if [ ! -f .env ]; then
    cp env.example .env
    echo "✅ Environment file created (update .env with your settings)"
fi

cd ..

# Frontend Setup
echo "📦 Setting up Frontend..."
cd frontend

# Install Node.js dependencies
npm install
echo "✅ Node.js dependencies installed"

# Create .env file from example
if [ ! -f .env ]; then
    cp env.example .env
    echo "✅ Environment file created (update .env with your settings)"
fi

cd ..

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update backend/.env with your configuration"
echo "2. Update frontend/.env with your configuration"
echo "3. Install Ollama: curl -fsSL https://ollama.ai/install.sh | sh"
echo "4. Pull Llama 2 model: ollama pull llama2:7b"
echo ""
echo "To start development:"
echo "Backend: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "Frontend: cd frontend && npm run dev"
echo ""
echo "Happy coding! 🚀" 