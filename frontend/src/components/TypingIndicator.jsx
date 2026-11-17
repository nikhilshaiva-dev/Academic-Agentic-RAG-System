import React from 'react';
import { Sparkles } from 'lucide-react';

export default function TypingIndicator() {
  return (
    <div className="flex justify-start mb-6 px-2">
      <div className="flex items-center space-x-3">
        {/* Assistant Avatar */}
        <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-brand-600 to-indigo-600 text-white flex items-center justify-center shrink-0 shadow-sm animate-pulse">
          <Sparkles className="w-4 h-4" />
        </div>

        {/* Bubble with bouncing dots */}
        <div className="flex items-center space-x-2.5 bg-white dark:bg-gray-800/90 border border-gray-200/80 dark:border-gray-700/60 rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm">
          <span className="text-xs font-medium text-gray-500 dark:text-gray-400">
            AI is thinking...
          </span>
          <div className="flex space-x-1 items-center">
            <div className="w-1.5 h-1.5 rounded-full bg-brand-500 animate-bounce" style={{ animationDelay: '0ms' }} />
            <div className="w-1.5 h-1.5 rounded-full bg-brand-500 animate-bounce" style={{ animationDelay: '150ms' }} />
            <div className="w-1.5 h-1.5 rounded-full bg-brand-500 animate-bounce" style={{ animationDelay: '300ms' }} />
          </div>
        </div>
      </div>
    </div>
  );
}

