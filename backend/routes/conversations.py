import sys
import os
from typing import List
from fastapi import APIRouter, HTTPException, status

# Ensure parent directory is in sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from backend.schemas import (
    ConversationResponse,
    ConversationCreate,
    MessageResponse
)
from backend.database import (
    get_conversations,
    create_conversation,
    get_conversation,
    get_messages,
    delete_conversation
)

router = APIRouter()


@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations():
    """Retrieve all conversations, ordered by last activity."""
    conversations = get_conversations()
    return conversations


@router.post("/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def new_conversation(payload: ConversationCreate = None):
    """Create a new conversation session."""
    title = payload.title if payload and payload.title else "New Chat"
    conv = create_conversation(title=title)
    return conv


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_history(conversation_id: str):
    """Retrieve all chat messages for a specific conversation."""
    conv = get_conversation(conversation_id)
    if not conv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation with ID '{conversation_id}' not found."
        )
    messages = get_messages(conversation_id)
    return messages


@router.delete("/conversations/{conversation_id}")
async def remove_conversation(conversation_id: str):
    """Delete a conversation, its messages, and agent checkpoints."""
    deleted = delete_conversation(conversation_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation with ID '{conversation_id}' not found."
        )
    return {
        "status": "success",
        "message": f"Conversation '{conversation_id}' deleted successfully.",
        "conversation_id": conversation_id
    }

