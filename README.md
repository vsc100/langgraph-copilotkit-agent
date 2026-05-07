# LangGraph CopilotKit Agent

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2.0-purple.svg)](https://langchain-ai.github.io/langgraph/)
[![React](https://img.shields.io/badge/React-18.2+-blue.svg)](https://react.dev)
[![CopilotKit](https://img.shields.io/badge/CopilotKit-UI-orange.svg)](https://github.com/CopilotKit)

A sophisticated AI agent built with LangGraph for multi-step reasoning, featuring a modern React-based UI with CopilotKit integration. This project demonstrates how to build production-ready AI agents with proper state management, streaming responses, and a polished user interface.

## Features

- **Multi-Step Reasoning**: LangGraph orchestrates complex workflows through planning, analysis, and execution stages
- **Real-time Streaming**: SSE (Server-Sent Events) for smooth, word-by-word response streaming
- **Modern UI**: Dark-themed React interface with smooth animations and responsive design
- **CopilotKit Integration**: Ready-to-use components for enhanced agent interactions
- **FastAPI Backend**: High-performance async API with automatic docs
- **Type Safety**: Full TypeScript support on frontend, Python type hints on backend
- **Modular Architecture**: Clean separation of concerns for easy extension

## Architecture

```

   Frontend    (React + TypeScript + CopilotKit UI)
   Port 3000

         ↑ HTTP/WebSocket
         ↓

   Backend     (FastAPI + LangGraph + OpenAI)
   Port 8000  
          
           LangGraph Agent
            
             Analyze → Plan → Execute → Respond
```

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- OpenAI API key (or Anthropic API key)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
```

5. Edit `.env` and add your OpenAI API key:
```env
OPENAI_API_KEY=your-openai-api-key-here
```

6. Run the server:
```bash
uvicorn app.main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The UI will be available at `http://localhost:3000`

## Usage

1. Open the UI in your browser
2. Type your message in the input box
3. Choose between:
   - **Send**: Get a standard response
   - **Stream**: Watch the agent think in real-time
   - **Clear**: Start a new conversation

### Example Queries

- "Explain LangGraph and its benefits"
- "Help me plan a multi-step project"
- "What are the best practices for AI agent development?"

## Agent Workflow

The LangGraph agent follows a structured 4-step process:

### 1. Analysis
- Parses user input
- Identifies intent and key entities
- Assesses complexity

### 2. Planning
- Formulates a step-by-step plan
- Considers context and constraints
- Optimizes for clarity and completeness

### 3. Execution
- Implements the plan
- Generates comprehensive responses
- Maintains consistency with context

### 4. Response
- Formats the final output
- Ensures quality and coherence
- Delivers to the user

## API Endpoints

### Health Check
```
GET /health
```
Returns the health status of the service.

### Chat
```
POST /chat
```
Send a message and receive a complete response.

**Request:**
```json
{
  "messages": [
    {"role": "user", "content": "Hello"}
  ],
  "session_id": "default"
}
```

**Response:**
```json
{
  "response": "Hello! How can I help you?",
  "context": {"stage": "completed"},
  "task_completed": true,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Stream
```
POST /stream
```
Stream the agent's response in real-time using Server-Sent Events.

### Documentation
```
GET /docs
```
Interactive API documentation (Swagger UI).

```
GET /redoc
```
Alternative API documentation (ReDoc).

## Project Structure

```
langgraph-copilotkit-agent/
 backend/
    app/
       agent.py          # LangGraph agent implementation
       main.py           # FastAPI application
       tests/            # Test suite
    .streamlit/           # Streamlit config (optional)
    requirements.txt      # Python dependencies
 frontend/
    src/
       components/       # React components
       hooks/           # Custom hooks
       pages/           # Page components
       types/           # TypeScript types
       styles/          # Global styles
       App.tsx          # Main App component
    package.json         # Node dependencies
    vite.config.ts       # Vite configuration
 .github/workflows/         # CI/CD pipelines
    ci-cd.yml             # GitHub Actions workflow
 .gitignore
 .env.example
 README.md
```

## Environment Variables

### Backend (.env)
```env
OPENAI_API_KEY=your-openai-api-key
```

### Frontend (.env.local)
```env
VITE_API_URL=http://localhost:8000
VITE_COPILOTKIT_PUBLIC_API_KEY=your-copilotkit-key
```

## Testing

Run the backend tests:
```bash
cd backend
python -m pytest app/tests/ -v
```

## Deployment

### Option 1: Docker

```dockerfile
# Backend Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Option 2: Cloud Platforms

- **Frontend**: Deploy to Vercel, Netlify, or GitHub Pages
- **Backend**: Deploy to Railway, Render, or Google Cloud Run

### Option 3: Kubernetes

See `k8s/` directory for deployment manifests (to be added).

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details

## Acknowledgments

- [LangGraph](https://github.com/langchain-ai/langgraph) for the agent orchestration framework
- [CopilotKit](https://github.com/CopilotKit) for the UI components
- [FastAPI](https://fastapi.tiangolo.com) for the backend framework
- [React](https://react.dev) for the frontend library

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Changelog

### v1.0.0 (2024-01-01)
- Initial release
- Multi-step agent with LangGraph
- React UI with CopilotKit integration
- Real-time streaming support
- Full documentation
