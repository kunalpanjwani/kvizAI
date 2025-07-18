# kvizAI - AI-Powered Quiz Platform

A completely free, open-source quiz platform that uses local AI models (Llama and Gemini) to generate personalized quizzes based on user questionnaires.

## 🚀 Features

- **100% Free**: No API costs, no hosting fees, no hidden charges
- **Open Source**: Community-driven development and contributions
- **Local AI Processing**: Llama and Gemini models running locally
- **Privacy-First**: No data sent to external AI services
- **Self-Hostable**: Users can run their own instances

## 🛠️ Tech Stack

- **Frontend**: React.js with TypeScript + Tailwind CSS
- **Backend**: Python FastAPI
- **Database**: SQLite (development) / PostgreSQL (Oracle Cloud Free Tier)
- **AI/ML**: Llama 2 (Ollama) + Gemini API
- **Authentication**: JWT tokens
- **Deployment**: Oracle Cloud Free Tier

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- Git
- Oracle Cloud account (free)
- Google Cloud account (for Gemini API - free tier)

## 🚀 Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Install Ollama and Llama 2
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama2:7b

# Start backend
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## 📁 Project Structure

```
kvizai/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   └── package.json
└── docs/
```

## 🔧 Environment Variables

Create `.env` files in both backend and frontend directories:

### Backend (.env)
```env
DATABASE_URL=sqlite:///./kvizai.db
SECRET_KEY=your-secret-key
GOOGLE_API_KEY=your-gemini-api-key
CORS_ORIGINS=http://localhost:3000
OLLAMA_BASE_URL=http://localhost:11434
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
```

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📊 Project Status

- [x] Project setup and environment configuration
- [ ] Database schema and models
- [ ] User authentication system
- [ ] Basic API endpoints
- [ ] Local AI setup (Ollama + Llama 2)
- [ ] Gemini API integration
- [ ] Frontend development
- [ ] Integration and deployment 