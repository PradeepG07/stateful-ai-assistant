from langgraph.checkpoint.memory import InMemorySaver
from typing import Annotated, List, Literal, TypedDict
import operator


from langgraph.graph import StateGraph, START, END
import json

from functions.registry import tools
from functions.functions import (
    get_customer_by_name,
    get_orders,
    get_customer
)

from models.models import (
    GetCustomerByNameArgs,
    GetOrdersArgs,
    GetCustomerArgs
)

from models.graph_state import AssistantState
from nodes.nodes import analyze_request, execute_tool, continue_after_tools

memory = InMemorySaver()


def route_after_model(state: AssistantState) -> str:
    if state.get("function_calls"):
        return "execute_tool"

    return "finish"

# Build the graph.
builder = StateGraph(AssistantState)

builder.add_node("analyze_request", analyze_request)
builder.add_node("execute_tool", execute_tool)
builder.add_node("continue_after_tools", continue_after_tools)

builder.add_edge(START, "analyze_request")

builder.add_conditional_edges(
    "analyze_request",
    route_after_model,
    {
        "execute_tool": "execute_tool",
        "finish": END
    }
)

builder.add_edge("execute_tool", "continue_after_tools")

builder.add_conditional_edges(
    "continue_after_tools",
    route_after_model,
    {
        "execute_tool": "execute_tool",
        "finish": END
    }
)

assistant = builder.compile(checkpointer=memory)

png_data = assistant.get_graph().draw_mermaid_png()

with open("assistant.png", "wb") as f:
    f.write(png_data)

print("Graph image saved as graph.png")

if __name__ == "__main__":

    config = {
        "configurable": {
            "thread_id": "customer-demo-1"
        },
        "recursion_limit": 10
    }

    while True:
        user_query = input("\nYou: ").strip()

        if user_query.lower() in {"exit", "quit"}:
            print("Chat ended.")
            break

        if not user_query:
            continue

        initial_state: AssistantState = {
            "user_query": user_query
        }

        result = assistant.invoke(
            initial_state,
            config=config
        )

        print("\nAssistant:")
        print(result.get("result", "No final response generated."))