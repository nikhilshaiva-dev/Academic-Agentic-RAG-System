import React from 'react';
import { 
  GraduationCap, 
  Plus, 
  MessageSquare, 
  Trash2, 
  Sun, 
  Moon, 
  ChevronLeft, 
  ChevronRight,
  Sparkles,
  BookOpen
} from 'lucide-react';

export default function Sidebar({
  conversations,
  currentConversationId,
  onSelectConversation,
  onNewChat,
  onDeleteConversation,
  isOpen,
  onToggleSidebar,
  theme,
  onToggleTheme,
  loading
}) {
  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={onToggleSidebar}
          aria-hidden="true"
        />
      )}

      <aside 
        className={`fixed md:static inset-y-0 left-0 z-50 flex flex-col w-64 md:w-72 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 transition-transform duration-300 ease-in-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full md:-translate-x-full'
        }`}
      >
        {/* Header: Logo and title */}
        <div className="flex items-center justify-between px-4 py-4 border-b border-gray-200 dark:border-gray-800">
          <div className="flex items-center space-x-2.5">
            <div className="flex items-center justify-center w-9 h-9 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-600 text-white shadow-sm">
              <GraduationCap className="w-5 h-5" />
            </div>
            <div>
              <h1 className="font-semibold text-sm leading-tight text-gray-900 dark:text-white">
                Student AI
              </h1>
              <span className="text-[11px] font-medium text-brand-600 dark:text-brand-400">
                Management Assistant
              </span>
            </div>
          </div>

          <button
            onClick={onToggleSidebar}
            className="md:hidden p-1.5 rounded-lg text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            title="Close sidebar"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
        </div>

        {/* New Chat Button */}
        <div className="p-3">
          <button
            onClick={onNewChat}
            disabled={loading}
            className="w-full flex items-center justify-center space-x-2 py-2.5 px-3.5 rounded-xl bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-700 hover:to-indigo-700 text-white text-sm font-medium shadow-sm hover:shadow transition-all duration-150 disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer"
          >
            <Plus className="w-4 h-4 stroke-[2.5]" />
            <span>New Chat</span>
          </button>
        </div>

        {/* Recent Conversations List */}
        <div className="flex-1 overflow-y-auto px-2 py-2 space-y-1">
          <div className="px-2 pb-1.5">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-gray-400 dark:text-gray-500">
              Recent Chats
            </span>
          </div>

          {conversations.length === 0 ? (
            <div className="px-3 py-6 text-center text-xs text-gray-400 dark:text-gray-500">
              No conversations yet.
            </div>
          ) : (
            conversations.map((conv) => {
              const isActive = conv.id === currentConversationId;
              return (
                <div
                  key={conv.id}
                  onClick={() => onSelectConversation(conv.id)}
                  className={`group relative flex items-center justify-between px-3 py-2.5 rounded-xl text-sm transition-all duration-150 cursor-pointer ${
                    isActive
                      ? 'bg-brand-50 dark:bg-brand-950/60 text-brand-700 dark:text-brand-300 font-medium'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800/60'
                  }`}
                >
                  <div className="flex items-center space-x-2.5 min-w-0 flex-1 mr-2">
                    <MessageSquare className={`w-4 h-4 shrink-0 ${
                      isActive ? 'text-brand-600 dark:text-brand-400' : 'text-gray-400 group-hover:text-gray-500'
                    }`} />
                    <span className="truncate" title={conv.title}>
                      {conv.title || 'Untitled Chat'}
                    </span>
                  </div>

                  <button
                    onClick={(e) => onDeleteConversation(conv.id, e)}
                    className="opacity-0 group-hover:opacity-100 focus:opacity-100 p-1 rounded-lg text-gray-400 hover:text-red-500 dark:text-gray-500 dark:hover:text-red-400 hover:bg-white dark:hover:bg-gray-800 transition-all duration-150"
                    title="Delete conversation"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              );
            })
          )}
        </div>

        {/* Footer: Knowledge summary & Theme toggle */}
        <div className="p-3 border-t border-gray-200 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-900/50 space-y-2">
          {/* Quick RAG stats badge */}
          <div className="flex items-center justify-between px-2.5 py-1.5 rounded-lg bg-gray-100 dark:bg-gray-800 text-[11px] text-gray-500 dark:text-gray-400">
            <span className="flex items-center space-x-1.5">
              <BookOpen className="w-3.5 h-3.5 text-brand-500" />
              <span>Policies & CSVs</span>
            </span>
            <span className="font-mono text-xs text-brand-600 dark:text-brand-400 font-medium">
              RAG Ready
            </span>
          </div>

          {/* Theme toggle */}
          <button
            onClick={onToggleTheme}
            className="w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            <span className="flex items-center space-x-2">
              {theme === 'dark' ? (
                <Moon className="w-4 h-4 text-brand-400" />
              ) : (
                <Sun className="w-4 h-4 text-amber-500" />
              )}
              <span>{theme === 'dark' ? 'Dark Mode' : 'Light Mode'}</span>
            </span>
            <span className="text-[10px] text-gray-400 uppercase tracking-wider">
              Toggle
            </span>
          </button>
        </div>
      </aside>
    </>
  );
}

