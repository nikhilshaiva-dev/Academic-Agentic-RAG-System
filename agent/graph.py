import os
import sys
import io
import sqlite3

from dotenv import load_dotenv

# Fix Windows terminal Unicode issues (special chars in AI responses)
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from agent.state import AgentState
from agent.prompt import SYSTEM_PROMPT
from agent.tools import tools
from config import DATABASE_PATH

# ----------------------------------
# Load API Key
# ----------------------------------

load_dotenv()

# Embeddings: local FastEmbed (BAAI/bge-small-en-v1.5) - no API key needed
# LLM: Groq openai/gpt-oss-120b - requires GROQ_API_KEY only

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)

# Bind tools to Groq
llm = llm.bind_tools(tools)


# ----------------------------------
# AI Node
# ----------------------------------

def chatbot(state: AgentState):

    messages = state["messages"]

    response = llm.invoke(
        [SystemMessage(content=SYSTEM_PROMPT)] + messages
    )

    return {
        "messages": [response]
    }


# ----------------------------------
# Should call tool?
# ----------------------------------

def should_continue(state: AgentState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END


# ----------------------------------
# Tool Node
# ----------------------------------

tool_node = ToolNode(tools)


# ----------------------------------
# Graph
# ----------------------------------

graph = StateGraph(AgentState)

graph.add_node("chatbot", chatbot)
graph.add_node("tools", tool_node)

graph.set_entry_point("chatbot")

graph.add_conditional_edges(
    "chatbot",
    should_continue,
)

graph.add_edge(
    "tools",
    "chatbot",
)

# Persistent SQLite checkpointer for conversation memory
try:
    from langgraph.checkpoint.sqlite import SqliteSaver
    checkpoint_conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    sqlite_checkpointer = SqliteSaver(checkpoint_conn)
    sqlite_checkpointer.setup()
    app = graph.compile(checkpointer=sqlite_checkpointer)
except Exception as e:
    print(f"Warning: SqliteSaver could not be initialized ({e}), compiling without checkpointer")
    sqlite_checkpointer = None
    app = graph.compile()


# ----------------------------------
# Test
# ----------------------------------

if __name__ == "__main__":

    cli_thread_id = "cli_default_session"

    while True:

        question = input("\nYou: ")

        if question.lower() == "exit":
            break

        config = {"configurable": {"thread_id": cli_thread_id}} if sqlite_checkpointer else None

        result = app.invoke(
            {"messages": [HumanMessage(content=question)]},
            config=config
        )

        ai_message = result["messages"][-1]

        print("\n========== AI RESPONSE ==========\n")
        if isinstance(ai_message.content, list):
            for block in ai_message.content:
                if isinstance(block, dict) and block.get("type") == "text":
                    print(block["text"])
        else:
            print(ai_message.content)
