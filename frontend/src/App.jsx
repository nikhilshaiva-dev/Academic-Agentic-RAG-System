import React from 'react';
import { useChat } from './hooks/useChat';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';

export default function App() {
  const {
    conversations,
    currentConversationId,
    messages,
    loading,
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
    clearError,
    retryConnection
  } = useChat();

  const currentConv = conversations.find(c => c.id === currentConversationId);

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-white dark:bg-gray-950">
      {/* Sidebar navigation */}
      <Sidebar
        conversations={conversations}
        currentConversationId={currentConversationId}
        onSelectConversation={selectConversation}
        onNewChat={startNewChat}
        onDeleteConversation={removeConversation}
        isOpen={sidebarOpen}
        onToggleSidebar={() => setSidebarOpen(prev => !prev)}
        theme={theme}
        onToggleTheme={toggleTheme}
        loading={loading}
      />

      {/* Main chat window */}
      <main className="flex-1 flex flex-col min-w-0 h-full relative">
        <ChatWindow
          conversation={currentConv}
          messages={messages}
          loading={loading}
          error={error}
          backendAvailable={backendAvailable}
          onSendMessage={sendUserMessage}
          onSelectPrompt={sendUserMessage}
          onToggleSidebar={() => setSidebarOpen(prev => !prev)}
          onNewChat={startNewChat}
          onRetryConnection={retryConnection}
          onDismissError={clearError}
        />
      </main>
    </div>
  );
}

