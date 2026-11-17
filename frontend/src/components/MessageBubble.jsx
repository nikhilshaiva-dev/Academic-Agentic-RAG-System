import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Copy, Check, Sparkles, User } from 'lucide-react';

export default function MessageBubble({ message }) {
  const [copied, setCopied] = useState(false);
  const isUser = message.role === 'user';

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(message.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy message:', err);
    }
  };

  if (isUser) {
    return (
      <div className="flex justify-end mb-4 px-2">
        <div className="flex items-start max-w-[85%] md:max-w-[75%] space-x-2 flex-row-reverse space-x-reverse">
          <div className="w-8 h-8 rounded-full bg-brand-600 text-white flex items-center justify-center shrink-0 shadow-sm mt-0.5">
            <User className="w-4 h-4" />
          </div>
          <div className="bg-brand-600 text-white px-4 py-2.5 rounded-2xl rounded-tr-sm text-sm leading-relaxed shadow-sm">
            <p className="whitespace-pre-wrap break-words">{message.content}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start mb-6 px-2 group">
      <div className="flex items-start max-w-[95%] md:max-w-[85%] space-x-3">
        {/* Assistant Avatar */}
        <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-brand-600 to-indigo-600 text-white flex items-center justify-center shrink-0 shadow-sm mt-0.5">
          <Sparkles className="w-4 h-4" />
        </div>

        {/* Message Container */}
        <div className="flex-1 min-w-0">
          <div className="relative bg-white dark:bg-gray-800/90 border border-gray-200/80 dark:border-gray-700/60 rounded-2xl rounded-tl-sm px-4 py-3.5 text-gray-800 dark:text-gray-100 shadow-sm">
            {/* Markdown rendered content */}
            <div className="prose-ai">
              <ReactMarkdown 
                remarkPlugins={[remarkGfm]}
                components={{
                  table: ({ node, ...props }) => (
                    <div className="overflow-x-auto my-3 rounded-lg border border-gray-200 dark:border-gray-700">
                      <table className="w-full text-sm" {...props} />
                    </div>
                  ),
                  th: ({ node, ...props }) => (
                    <th className="px-3 py-2 bg-gray-100 dark:bg-gray-900/60 font-semibold text-gray-900 dark:text-white border-b border-gray-200 dark:border-gray-700" {...props} />
                  ),
                  td: ({ node, ...props }) => (
                    <td className="px-3 py-2 border-b border-gray-100 dark:border-gray-800" {...props} />
                  ),
                  a: ({ node, ...props }) => (
                    <a className="text-brand-600 dark:text-brand-400 hover:underline" target="_blank" rel="noopener noreferrer" {...props} />
                  )
                }}
              >
                {message.content}
              </ReactMarkdown>
            </div>

            {/* Bottom Actions: Copy response */}
            <div className="mt-3 pt-2.5 border-t border-gray-100 dark:border-gray-700/40 flex items-center justify-between text-xs text-gray-400">
              <span className="text-[11px]">Student Management Assistant</span>
              <button
                onClick={handleCopy}
                className="flex items-center space-x-1.5 px-2 py-1 rounded-md text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700/60 transition-colors cursor-pointer"
                title="Copy response to clipboard"
              >
                {copied ? (
                  <>
                    <Check className="w-3.5 h-3.5 text-emerald-500" />
                    <span className="text-emerald-500 font-medium">Copied!</span>
                  </>
                ) : (
                  <>
                    <Copy className="w-3.5 h-3.5" />
                    <span>Copy</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

