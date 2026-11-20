import React, { useRef, useEffect } from 'react';
import { Menu, Plus, AlertCircle, RefreshCw } from 'lucide-react';
import MessageBubble from './MessageBubble';
import TypingIndicator from './TypingIndicator';
import EmptyChat from './EmptyChat';
import ChatInput from './ChatInput';
import { API_BASE_URL } from '../services/api';

export default function ChatWindow({
  conversation,
  messages,
  loading,
  error,
  backendAvailable,
  onSendMessage,
  onSelectPrompt,
  onToggleSidebar,
  onNewChat,
  onRetryConnection,
  onDismissError
}) {
  const messagesEndRef = useRef(null);

  // Auto-scroll on new message or typing state change
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  return (
    <div className="flex-1 flex flex-col h-full bg-gray-50 dark:bg-gray-950 overflow-hidden relative">
      {/* Top Header */}
      <header className="h-14 border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md px-4 flex items-center justify-between z-10">
        <div className="flex items-center space-x-3 min-w-0">
          <button
            onClick={onToggleSidebar}
            className="p-1.5 rounded-lg text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors cursor-pointer"
            title="Toggle sidebar"
          >
            <Menu className="w-5 h-5" />
          </button>
          
          <h2 className="text-sm font-semibold text-gray-800 dark:text-gray-200 truncate">
            {conversation ? conversation.title : 'New Chat'}
          </h2>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={onNewChat}
            disabled={loading}
            className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-medium rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors disabled:opacity-50 cursor-pointer"
            title="Start new conversation"
          >
            <Plus className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">New Chat</span>
          </button>
        </div>
      </header>

      {/* Backend connection warning banner */}
      {!backendAvailable && (
        <div className="bg-red-500 text-white px-4 py-2 text-xs flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>Backend server is offline or waking up on Render. Please wait a moment and click Retry.</span>
          </div>
          <button
            onClick={onRetryConnection}
            className="flex items-center space-x-1 underline hover:text-red-100 font-medium cursor-pointer"
          >
            <RefreshCw className="w-3 h-3" />
            <span>Retry</span>
          </button>
        </div>
      )}

      {/* Error banner */}
      {error && backendAvailable && (
        <div className="bg-amber-50 dark:bg-amber-950/60 border-b border-amber-200 dark:border-amber-800/60 px-4 py-2.5 text-xs text-amber-800 dark:text-amber-300 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 shrink-0 text-amber-600 dark:text-amber-400" />
            <span>{error}</span>
          </div>
          <button
            onClick={onDismissError}
            className="text-amber-700 dark:text-amber-300 hover:underline font-medium ml-4 cursor-pointer"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-3xl mx-auto">
          {messages.length === 0 ? (
            <EmptyChat onSelectPrompt={onSelectPrompt} />
          ) : (
            <>
              {messages.map((msg) => (
                <MessageBubble key={msg.id} message={msg} />
              ))}
              {loading && <TypingIndicator />}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>
      </div>

      {/* Pinned Chat Input */}
      <div className="border-t border-transparent bg-gradient-to-t from-gray-50 via-gray-50 to-transparent dark:from-gray-950 dark:via-gray-950 pt-2">
        <ChatInput
          onSendMessage={onSendMessage}
          loading={loading}
          disabled={!backendAvailable}
        />
      </div>
    </div>
  );
}

