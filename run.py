import sys
import os

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_core.messages import HumanMessage
from agent.graph import app, sqlite_checkpointer

cli_thread_id = "cli_runner_session"

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
