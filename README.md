# Student Management AI Assistant – Agentic RAG Web Application

A full-stack, ChatGPT-inspired academic assistant application that transforms an Agentic RAG command-line agent into an interactive, multi-session web chat platform.

The system combines **LangGraph** agent orchestration, **FastAPI** REST services, and a modern **React + Tailwind CSS** frontend to provide intelligent answers regarding student details, attendance records, academic performance, assessment marks, courses, mentors, leaderboard analytics, at-risk alerts, and university policy retrieval.

---

## 1. System Architecture

```text
                  USER
                    │
                    ▼
           REACT FRONTEND (Vite)
                    │
          ┌─────────────────────┐
          │                     │
          ▼                     ▼
      Sidebar              Chat Window
          │                     │
          │                 Chat Input
          │                     │
          └─────────────────────┘
                    │ REST API
                    ▼
              FASTAPI SERVER (Uvicorn :8000)
                    │
              Chat & Conversation Routes
                    │
                    ▼
             LANGGRAPH AGENT
                    │
          ┌──────────────────────┐
          │          │           │
          ▼          ▼           ▼
      Grok LLM     Tools     Agent State
  (openai/gpt-oss)   │      (SQLite Checkpointer)
                     │
             ┌───────┴───────┐
             │               │
             ▼               ▼
      Student Analytics    Policy Retrieval
             │               │
             ▼               ▼
        CSV Datasets    FAISS Vector Store
       (Students, etc.) (FastEmbed / Policies)
             │               │
             └───────┬───────┘
                     │
                     ▼
                AI RESPONSE
                     │
                     ▼
               FASTAPI SERVER
                     │
                     ▼
             REACT CHAT WINDOW
```

---

## 2. Technology Stack

### Frontend
- **Framework:** React 18, Vite
- **Styling:** Tailwind CSS, PostCSS, Autoprefixer
- **Icons:** Lucide React
- **Markdown:** React Markdown, Remark GFM (tables, lists, bold text)
- **Theme:** Dark & Light modes with automatic persistence

### Backend
- **Framework:** FastAPI, Starlette
- **Server:** Uvicorn
- **Agent Orchestration:** LangGraph (StateGraph, ToolNode)
- **LLM Integration:** LangChain Groq (`openai/gpt-oss-120b`)
- **Embeddings:** FastEmbed (`BAAI/bge-small-en-v1.5`)
- **Vector Retrieval:** FAISS CPU
- **Data Analytics:** Pandas

### Storage & Persistence
- **Conversation Metadata & Messages:** SQLite (`chat_app.db`)
- **Agent State & Multi-Turn Memory:** LangGraph `SqliteSaver` checkpointer with isolated `thread_id` sessions
- **Policy Knowledge Base:** FAISS vector store index

---

## 3. Project Structure

```text
Agentic rag/
│
├── backend/
│   ├── __init__.py
│   ├── main.py                  # FastAPI initialization, CORS, static mounting
│   ├── database.py              # SQLite connection, CRUD for conversations/messages
│   ├── schemas.py               # Pydantic request/response validation
│   └── routes/
│       ├── __init__.py
│       ├── chat.py              # POST /api/chat with agent invocation
│       └── conversations.py     # Conversation management endpoints
│
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── components/
│       │   ├── Sidebar.jsx          # Conversations sidebar, New Chat, theme toggle
│       │   ├── ChatWindow.jsx       # Header, message scroll, input layout
│       │   ├── MessageBubble.jsx    # User & Markdown AI bubbles, copy action
│       │   ├── ChatInput.jsx        # Textarea with Enter/Shift+Enter, send button
│       │   ├── TypingIndicator.jsx  # "AI is thinking..." animated indicator
│       │   └── EmptyChat.jsx        # ChatGPT-style welcome & prompt suggestions
│       ├── services/
│       │   └── api.js               # Clean API service functions
│       ├── hooks/
│       │   └── useChat.js           # Chat state, theme, and API orchestration
│       ├── App.jsx
│       ├── main.jsx
│       └── index.css
│
├── agent/
│   ├── graph.py                 # LangGraph agent compilation & checkpointer
│   ├── prompt.py                # System instructions & formatting rules
│   ├── state.py                 # AgentState TypedDict with add_messages
│   └── tools.py                 # 9 registered agent tools
│
├── tools/
│   ├── analytics_tools.py       # Attendance & performance analytics
│   ├── policy_search.py         # FAISS vector store policy retrieval
│   ├── risk_detection.py        # At-risk student heuristics
│   └── student_tools.py         # Student record lookups
│
├── utils/
│   ├── data_loader.py           # Cached CSV dataset loaders
│   ├── embeddings.py            # Local FastEmbed embeddings
│   ├── policy_loader.py         # Policy markdown file loader
│   └── text_splitter.py         # Document chunking with metadata
│
├── data/                        # CSV datasets (students, attendance, assessments, etc.)
├── policies/                    # University policy documents (.md)
├── vectorstore/                 # FAISS index files
├── config.py                    # Project-relative paths & configuration
├── run.py                       # CLI runner (backward compatible)
├── test_verification_suite.py   # Full automated test suite
├── requirements.txt             # Python backend dependencies
├── .env                         # API keys (GROQ_API_KEY, GEMINI_API_KEY)
└── .gitignore                   # Ignores .env, databases, node_modules
```

---

## 4. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Backend status & agent readiness |
| `POST` | `/api/chat` | Send message to AI agent & receive markdown response |
| `GET` | `/api/conversations` | Retrieve all conversations sorted by latest activity |
| `POST` | `/api/conversations` | Create a new conversation session |
| `GET` | `/api/conversations/{id}/messages` | Retrieve message history for a conversation |
| `DELETE` | `/api/conversations/{id}` | Delete conversation, history, and checkpoints |

---

## 5. Setup & Running Instructions

### Prerequisites
- Python 3.10+ (tested with Python 3.11)
- Node.js 18+ (tested with Node.js 24)
- Valid `GROQ_API_KEY` configured in `.env`

### Backend Setup

Navigate to the project root:
```bash
cd "Agentic rag"
```

Activate or create a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install backend dependencies:
```bash
pip install -r requirements.txt
```

Start the FastAPI backend server:
```bash
uvicorn backend.main:app --reload --port 8000
```
Backend API will be live at `http://localhost:8000`. You can test health at `http://localhost:8000/api/health`.

### Frontend Setup

Open a second terminal:
```bash
cd "Agentic rag/frontend"
npm install
npm run dev
```
Open your browser at the Vite URL (typically `http://localhost:5173`).

---

## 6. Automated Verification Suite

Run the end-to-end automated verification script:
```bash
cd "Agentic rag"
python test_verification_suite.py
```

This validates all 7 core test requirements:
1. **Test 1: Backend Health** (`/api/health` status 200).
2. **Test 2: Student Attendance** (STU0050 attendance percentage calculation).
3. **Test 3: Conversation Memory** (follow-up question context retention without repeating student ID).
4. **Test 4: Separate Conversations Isolation** (verifies STU0050 and STU0020 sessions never mix context).
5. **Test 5: Policy Retrieval** (FAISS similarity search for attendance policy).
6. **Test 6: Leaderboard Analytics** (`top_students` execution).
7. **Test 7: Chat History Restoration** (SQLite persistence and retrieval).

