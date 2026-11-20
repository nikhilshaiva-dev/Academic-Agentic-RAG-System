import { useState, useEffect, useCallback, useRef } from 'react';
import {
  getConversations,
  createConversation,
  getConversationMessages,
  sendMessage,
  deleteConversation,
  checkHealth
} from '../services/api';

export function useChat() {
  const [conversations, setConversations] = useState([]);
  const [currentConversationId, setCurrentConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [error, setError] = useState(null);
  const [backendAvailable, setBackendAvailable] = useState(true);
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('theme') || 'dark';
  });
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // Sync theme with HTML class and localStorage
  useEffect(() => {
    const root = document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
  };

  // Check health and load conversations on mount
  const refreshConversations = useCallback(async (selectFirstIfNoneSelected = false) => {
    try {
      setError(null);
      await checkHealth();
      setBackendAvailable(true);
      const convList = await getConversations();
      setConversations(convList);

      if (convList.length > 0) {
        if (selectFirstIfNoneSelected || !currentConversationId) {
          const targetId = convList[0].id;
          setCurrentConversationId(targetId);
          const msgs = await getConversationMessages(targetId);
          setMessages(msgs);
        }
      } else {
        // No conversations exist yet, create one
        const newConv = await createConversation("New Chat");
        setConversations([newConv]);
        setCurrentConversationId(newConv.id);
        setMessages([]);
      }
    } catch (err) {
  console.error("Failed to load conversations:", err);
  setBackendAvailable(false);
  setError(`Failed to load chat data: ${err.message}`);
} finally {
      setInitialLoading(false);
    }
  }, [currentConversationId]);

  useEffect(() => {
    refreshConversations(true);
  }, []);

  // Switch to a conversation
  const selectConversation = async (id) => {
    if (id === currentConversationId || loading) return;
    try {
      setLoading(false);
      setError(null);
      setCurrentConversationId(id);
      const msgs = await getConversationMessages(id);
      setMessages(msgs);
    } catch (err) {
      console.error("Failed to load messages:", err);
      setError(`Failed to load messages for conversation: ${err.message}`);
    }
  };

  // Start a fresh conversation
  const startNewChat = async () => {
    if (loading) return;
    try {
      setError(null);
      const newConv = await createConversation("New Chat");
      setConversations(prev => [newConv, ...prev]);
      setCurrentConversationId(newConv.id);
      setMessages([]);
    } catch (err) {
      console.error("Failed to create new conversation:", err);
      setError(`Failed to create new chat: ${err.message}`);
    }
  };

  // Send a message
  const sendUserMessage = async (text) => {
    const trimmed = text.trim();
    if (!trimmed || loading) return;

    let targetConvId = currentConversationId;
    if (!targetConvId) {
      try {
        const newConv = await createConversation("New Chat");
        setConversations(prev => [newConv, ...prev]);
        targetConvId = newConv.id;
        setCurrentConversationId(targetConvId);
      } catch (err) {
        setError("Failed to create conversation session.");
        return;
      }
    }

    const optimisticUserMsg = {
      id: `temp-${Date.now()}`,
      conversation_id: targetConvId,
      role: 'user',
      content: trimmed,
      created_at: new Date().toISOString()
    };

    // Optimistically update UI
    setMessages(prev => [...prev, optimisticUserMsg]);
    setLoading(true);
    setError(null);

    try {
      const result = await sendMessage(targetConvId, trimmed);
      
      const assistantMsg = {
        id: result.message_id,
        conversation_id: targetConvId,
        role: 'assistant',
        content: result.response,
        created_at: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMsg]);

      // Refresh conversations list to update title and updated_at order
      const updatedList = await getConversations();
      setConversations(updatedList);
    } catch (err) {
      console.error("Failed to send message:", err);
      setError(err.message || "Failed to get response from AI agent.");
    } finally {
      setLoading(false);
    }
  };

  // Delete conversation
  const removeConversation = async (id, e) => {
    if (e) {
      e.stopPropagation();
    }
    if (loading) return;

    try {
      await deleteConversation(id);
      const remaining = conversations.filter(c => c.id !== id);
      setConversations(remaining);

      if (currentConversationId === id) {
        if (remaining.length > 0) {
          const nextConv = remaining[0];
          setCurrentConversationId(nextConv.id);
          const msgs = await getConversationMessages(nextConv.id);
          setMessages(msgs);
        } else {
          // No conversations left, create a fresh one
          const fresh = await createConversation("New Chat");
          setConversations([fresh]);
          setCurrentConversationId(fresh.id);
          setMessages([]);
        }
      }
    } catch (err) {
      console.error("Failed to delete conversation:", err);
      setError(`Failed to delete conversation: ${err.message}`);
    }
  };

  return {
    conversations,
    currentConversationId,
    messages,
    loading,
    initialLoading,
    error,
    backendAvailable,
    theme,
    sidebarOpen,
    setSidebarOpen,
    toggleTheme,
    selectConversation,
    startNewChat,
    sendUserMessage,
    removeConversation,
    clearError: () => setError(null),
    retryConnection: () => refreshConversations(true)
  };
}

