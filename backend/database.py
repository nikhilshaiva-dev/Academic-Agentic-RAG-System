import sqlite3
import uuid
from datetime import datetime, timezone
import os
import sys

# Ensure parent directory is in sys.path to access config
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from config import DATABASE_PATH


def get_db_connection():
    """Get a SQLite database connection with row factory enabled."""
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables for conversations and messages."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
            )
        """)
        
        # Index on conversation_id for fast message queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_conversation_id 
            ON messages (conversation_id)
        """)
        
        conn.commit()


# Ensure tables exist on module import
init_db()


def get_now_iso() -> str:
    """Return current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


def create_conversation(conversation_id: str = None, title: str = "New Chat") -> dict:
    """Create a new conversation record."""
    cid = conversation_id or str(uuid.uuid4())
    now = get_now_iso()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO conversations (id, title, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            """,
            (cid, title, now, now)
        )
        conn.commit()
    return {
        "id": cid,
        "title": title,
        "created_at": now,
        "updated_at": now
    }


def get_conversation(conversation_id: str) -> dict | None:
    """Retrieve metadata for a specific conversation."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, created_at, updated_at FROM conversations WHERE id = ?",
            (conversation_id,)
        )
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None


def get_conversations() -> list[dict]:
    """Retrieve all conversations ordered by last updated descending."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, created_at, updated_at FROM conversations ORDER BY updated_at DESC"
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def update_conversation_title(conversation_id: str, title: str):
    """Update title and timestamp of a conversation."""
    now = get_now_iso()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE conversations SET title = ?, updated_at = ? WHERE id = ?",
            (title, now, conversation_id)
        )
        conn.commit()


def update_conversation_timestamp(conversation_id: str):
    """Update the updated_at timestamp of a conversation."""
    now = get_now_iso()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE conversations SET updated_at = ? WHERE id = ?",
            (now, conversation_id)
        )
        conn.commit()


def add_message(conversation_id: str, role: str, content: str, message_id: str = None) -> dict:
    """Add a message to the database."""
    mid = message_id or str(uuid.uuid4())
    now = get_now_iso()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO messages (id, conversation_id, role, content, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (mid, conversation_id, role, content, now)
        )
        conn.commit()
    return {
        "id": mid,
        "conversation_id": conversation_id,
        "role": role,
        "content": content,
        "created_at": now
    }


def get_messages(conversation_id: str) -> list[dict]:
    """Retrieve all messages for a given conversation ordered by created_at."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, conversation_id, role, content, created_at 
            FROM messages 
            WHERE conversation_id = ? 
            ORDER BY created_at ASC
            """,
            (conversation_id,)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def delete_conversation(conversation_id: str) -> bool:
    """
    Delete a conversation, all its messages, and any associated LangGraph checkpoints.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Check if conversation exists
        cursor.execute("SELECT id FROM conversations WHERE id = ?", (conversation_id,))
        if not cursor.fetchone():
            return False
            
        # Delete messages
        cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
        
        # Delete conversation
        cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
        
        # Clean up LangGraph checkpointer tables if they exist
        tables_to_clean = ["checkpoints", "checkpoint_blobs", "checkpoint_writes"]
        for table in tables_to_clean:
            try:
                cursor.execute(f"DELETE FROM {table} WHERE thread_id = ?", (conversation_id,))
            except sqlite3.OperationalError:
                # Table might not exist or have different column schema
                pass
                
        conn.commit()
        return True
