from pydantic import BaseModel, Field
from typing import Optional, List


class ChatRequest(BaseModel):
    conversation_id: str = Field(..., description="Unique ID for the conversation session")
    message: str = Field(..., min_length=1, description="User's question or message")


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    message_id: str


class ConversationCreate(BaseModel):
    title: Optional[str] = "New Chat"


class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    created_at: str


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    agent_loaded: bool

