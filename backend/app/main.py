from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import asyncio
from datetime import datetime
import logging

from app.agent import LangGraphAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="LangGraph CopilotKit Agent",
    description="A LangGraph-powered AI agent with CopilotKit UI integration",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent
agent = LangGraphAgent()

# Request/Response models
class Message(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    messages: List[Message]
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    context: Dict[str, Any]
    task_completed: bool
    timestamp: str

class StreamMessage(BaseModel):
    type: str
    content: str
    stage: Optional[str] = None

class HealthCheck(BaseModel):
    status: str
    timestamp: str
    version: str
    agent_ready: bool

@app.get("/", tags=["Root"])
async def root():
    return {
        "service": "LangGraph CopilotKit Agent",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "chat": "/chat",
            "stream": "/stream",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthCheck, tags=["Health"])
async def health_check():
    return HealthCheck(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        agent_ready=True
    )

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_endpoint(request: ChatRequest):
    try:
        # Convert messages to format expected by agent
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]
        
        # Run agent
        result = await agent.arun(messages)
        
        return ChatResponse(
            response=result.get("response", ""),
            context=result.get("context", {}),
            task_completed=result.get("task_completed", False),
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stream", tags=["Chat"])
async def stream_endpoint(request: ChatRequest):
    async def event_stream():
        try:
            # Convert messages
            messages = [
                {"role": msg.role, "content": msg.content}
                for msg in request.messages
            ]
            
            # Send initial message
            yield f"data: {json.dumps({'type': 'status', 'content': 'Starting agent...'})}\n\n"
            
            # Run agent
            result = await agent.arun(messages)
            
            # Stream response in chunks for better UX
            response = result.get("response", "")
            
            # Send analysis stage
            yield f"data: {json.dumps({'type': 'stage', 'content': 'Analysis complete', 'stage': 'analyze'})}\n\n"
            await asyncio.sleep(0.1)
            
            # Send planning stage
            yield f"data: {json.dumps({'type': 'stage', 'content': 'Plan formulated', 'stage': 'plan'})}\n\n"
            await asyncio.sleep(0.1)
            
            # Send execution stage
            yield f"data: {json.dumps({'type': 'stage', 'content': 'Executing plan', 'stage': 'execute'})}\n\n"
            await asyncio.sleep(0.1)
            
            # Stream response word by word
            words = response.split()
            for i, word in enumerate(words):
                yield f"data: {json.dumps({'type': 'chunk', 'content': word + ' ', 'stage': 'respond'})}\n\n"
                await asyncio.sleep(0.02)  # Small delay for streaming effect
            
            # Send completion
            yield f"data: {json.dumps({'type': 'complete', 'content': response, 'stage': 'completed'})}\n\n"
            
        except Exception as e:
            logger.error(f"Stream error: {str(e)}")
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
    
    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.get("/sessions/{session_id}", tags=["Sessions"])
async def get_session(session_id: str):
    # In a real app, you'd retrieve session history from a database
    return {
        "session_id": session_id,
        "messages": [],
        "created_at": datetime.utcnow().isoformat(),
        "message": "Session history not implemented in this demo"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
