import sys
import os
import uuid
import logging
from fastapi import APIRouter, HTTPException, status
from langchain_core.messages import HumanMessage

# Ensure parent directory is in sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from backend.schemas import ChatRequest, ChatResponse
from backend.database import (
    get_conversation,
    create_conversation,
    update_conversation_title,
    update_conversation_timestamp,
    add_message,
    get_messages
)
from agent.graph import app, sqlite_checkpointer

logger = logging.getLogger("uvicorn.error")
router = APIRouter()


def clean_title_from_message(message: str) -> str:
    """Derive a friendly conversation title from the first message."""
    cleaned = " ".join(message.strip().split())
    if len(cleaned) > 40:
        return cleaned[:37] + "..."
    return cleaned if cleaned else "New Chat"


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Handle a user message:
    1. Ensure conversation exists in SQLite.
    2. Persist the user message.
    3. Invoke the LangGraph agent with the thread_id.
    4. Persist the assistant message.
    5. Return the response.
    """
    user_prompt = request.message.strip()
    if not user_prompt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty."
        )

    cid = request.conversation_id.strip()
    if not cid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="conversation_id cannot be empty."
        )

    try:
        # Check if conversation exists; create if not
        conv = get_conversation(cid)
        is_first_message = False
        if not conv:
            conv = create_conversation(conversation_id=cid, title="New Chat")
            is_first_message = True
        else:
            existing_messages = get_messages(cid)
            if len(existing_messages) == 0 or conv["title"] == "New Chat":
                is_first_message = True

        # Store user message
        user_msg_id = str(uuid.uuid4())
        add_message(
            conversation_id=cid,
            role="user",
            content=user_prompt,
            message_id=user_msg_id
        )

        # Update title if this is the first user query
        if is_first_message:
            new_title = clean_title_from_message(user_prompt)
            update_conversation_title(cid, new_title)

        # Invoke LangGraph app with thread_id for conversation memory isolation
        config = {"configurable": {"thread_id": cid}} if sqlite_checkpointer else None

        result = app.invoke(
            {"messages": [HumanMessage(content=user_prompt)]},
            config=config
        )

        # Extract assistant response text
        messages = result.get("messages", [])
        if not messages:
            raise RuntimeError("Agent produced no response messages.")

        ai_msg = messages[-1]
        if isinstance(ai_msg.content, list):
            text_blocks = []
            for block in ai_msg.content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_blocks.append(block.get("text", ""))
                elif isinstance(block, str):
                    text_blocks.append(block)
            response_text = "\n".join(text_blocks)
        else:
            response_text = str(ai_msg.content)

        if not response_text.strip():
            response_text = "I processed your request, but no text response was generated."

        # Store assistant message
        ai_msg_id = str(uuid.uuid4())
        add_message(
            conversation_id=cid,
            role="assistant",
            content=response_text,
            message_id=ai_msg_id
        )

        # Update conversation timestamp
        update_conversation_timestamp(cid)

        return ChatResponse(
            conversation_id=cid,
            response=response_text,
            message_id=ai_msg_id
        )

    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Error in chat_endpoint for conversation {cid}: {str(exc)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the request: {str(exc)}"
        )

