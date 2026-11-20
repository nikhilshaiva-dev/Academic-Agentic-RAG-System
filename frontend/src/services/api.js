const rawUrl =
  import.meta.env.VITE_API_URL ||
  (import.meta.env.PROD
    ? "https://academic-agentic-rag-system-1.onrender.com/api"
    : "http://localhost:8000/api");

// Normalize to guarantee it ends with /api regardless of how VITE_API_URL was set in Vercel
const cleanUrl = rawUrl.trim().replace(/\/+$/, "");
export const API_BASE_URL = cleanUrl.endsWith("/api") ? cleanUrl : `${cleanUrl}/api`;

/**
 * Handle API responses and throw informative errors
 */
async function handleResponse(response) {
  if (!response.ok) {
    let errorDetail = `HTTP ${response.status}: ${response.statusText}`;
    try {
      const data = await response.json();
      if (data && data.detail) {
        errorDetail = typeof data.detail === "string" ? data.detail : JSON.stringify(data.detail);
      } else if (data && data.error) {
        errorDetail = data.error;
      }
    } catch (_) {
      // response wasn't JSON
    }
    throw new Error(errorDetail);
  }
  return response.json();
}

/**
 * Check backend health status
 */
export async function checkHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);
  return handleResponse(response);
}

/**
 * Retrieve list of all conversations
 */
export async function getConversations() {
  const response = await fetch(`${API_BASE_URL}/conversations`);
  return handleResponse(response);
}

/**
 * Create a new conversation session
 */
export async function createConversation(title = "New Chat") {
  const response = await fetch(`${API_BASE_URL}/conversations`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ title }),
  });
  return handleResponse(response);
}

/**
 * Retrieve chat history for a specific conversation
 */
export async function getConversationMessages(id) {
  const response = await fetch(`${API_BASE_URL}/conversations/${id}/messages`);
  return handleResponse(response);
}

/**
 * Send a user message to the AI agent
 */
export async function sendMessage(conversationId, message) {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      conversation_id: conversationId,
      message: message,
    }),
  });
  return handleResponse(response);
}

/**
 * Delete a conversation, messages, and associated agent state
 */
export async function deleteConversation(id) {
  const response = await fetch(`${API_BASE_URL}/conversations/${id}`, {
    method: "DELETE",
  });
  return handleResponse(response);
}

