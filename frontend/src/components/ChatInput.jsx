import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2 } from 'lucide-react';

export default function ChatInput({ onSendMessage, loading, disabled }) {
  const [input, setInput] = useState('');
  const textareaRef = useRef(null);

  // Auto-resize textarea based on content
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      const scrollHeight = textareaRef.current.scrollHeight;
      // Max height ~160px
      textareaRef.current.style.height = `${Math.min(scrollHeight, 160)}px`;
    }
  }, [input]);

  const handleSubmit = (e) => {
    if (e) e.preventDefault();
    if (!input.trim() || loading || disabled) return;
    onSendMessage(input);
    setInput('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e) => {
    // Enter without Shift sends message
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto px-4 pb-4">
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative flex items-end rounded-2xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm focus-within:border-brand-500 focus-within:ring-2 focus-within:ring-brand-500/20 transition-all duration-150">
          <textarea
            ref={textareaRef}
            rows={1}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading || disabled}
            placeholder="Ask anything about students, attendance, performance, or policies..."
            className="w-full resize-none py-3 pl-4 pr-12 bg-transparent text-sm text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none disabled:opacity-50"
            style={{ minHeight: '44px' }}
          />

          {/* Send Button */}
          <button
            type="submit"
            disabled={!input.trim() || loading || disabled}
            className="absolute right-2 bottom-2 p-2 rounded-xl bg-brand-600 hover:bg-brand-700 text-white disabled:opacity-30 disabled:hover:bg-brand-600 disabled:cursor-not-allowed transition-all duration-150 shadow-sm cursor-pointer"
            title="Send message"
          >
            {loading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </button>
        </div>

        {/* Footnote */}
        <p className="mt-2 text-center text-[11px] text-gray-400 dark:text-gray-500">
          Student AI Assistant combines LangGraph agent reasoning with FAISS policy retrieval and student records.
        </p>
      </form>
    </div>
  );
}

