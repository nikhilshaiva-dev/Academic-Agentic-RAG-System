import sys
import os
from contextlib import asynccontextmanager

# Ensure the project root ("Agentic rag") is on the Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.database import init_db
from backend.schemas import HealthResponse
from backend.routes.chat import router as chat_router
from backend.routes.conversations import router as conversations_router
from agent.graph import app as agent_app


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database tables
    init_db()
    # The LangGraph agent (`agent_app`) and CSVs are loaded once at module import
    yield
    # Shutdown logic if any
    pass


app = FastAPI(
    title="Student Management AI Assistant API",
    description="Agentic RAG backend powering student analytics and policy retrieval",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"  # Allow all origins for seamless development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint to verify backend status and agent readiness."""
    return HealthResponse(
        status="healthy",
        service="Student AI Assistant API",
        version="1.0.0",
        agent_loaded=agent_app is not None
    )


# Register API routes
app.include_router(chat_router, prefix="/api", tags=["Chat"])
app.include_router(conversations_router, prefix="/api", tags=["Conversations"])


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
            "path": request.url.path
        }
    )


# Mount built frontend static files if available
dist_dir = os.path.join(PROJECT_ROOT, "frontend", "dist")
if os.path.exists(dist_dir):
    app.mount("/", StaticFiles(directory=dist_dir, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
