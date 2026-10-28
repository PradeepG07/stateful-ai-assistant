from openai import OpenAI
import os
import json
from dotenv import load_dotenv

from models.graph_state import AssistantState
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


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

tool_registry = {

    "get_customer_by_name": {
        "function": get_customer_by_name,
        "schema": GetCustomerByNameArgs
    },

    "get_orders": {
        "function": get_orders,
        "schema": GetOrdersArgs
    },
    "get_customer": {
    "function": get_customer,
    "schema": GetCustomerArgs
}

}

def analyze_request(state: AssistantState) -> dict:
    user_input = state["user_query"]

    request_args = {
        "model": "gpt-5.6",
        "input": user_input,
        "tools": tools
    }

    # Get the previous OpenAI response ID from LangGraph state
    previous_response_id = state.get("response_id")

    print("Previous response ID:", previous_response_id)

    # Continue the existing OpenAI conversation
    if previous_response_id:
        request_args["previous_response_id"] = previous_response_id

    response = client.responses.create(**request_args)

    function_calls = [
        {
            "call_id": item.call_id,
            "name": item.name,
            "arguments": item.arguments
        }
        for item in response.output
        if item.type == "function_call"
    ]

    return {
        "function_calls": function_calls,
        "response_id": response.id,
        "tool_results": [],
        "result": response.output_text if not function_calls else ""
    }


def execute_tool(state: AssistantState) -> dict:
    tool_results = []
    customer_id = None

    for item in state.get("function_calls", []):
        tool_name = item["name"]

        try:
            # 1. Check whether the requested tool is registered
            if tool_name not in tool_registry:
                raise ValueError(f"Unknown tool: {tool_name}")

            # 2. Parse the arguments
            arguments = json.loads(item["arguments"])

            # 3. Get the function and Pydantic schema
            tool = tool_registry[tool_name]

            # 4. Validate arguments
            validated_args = tool["schema"].model_validate(
                arguments
            )

            # 5. Execute the Python function
            output = tool["function"](
                **validated_args.model_dump()
            )

            if (
                tool_name in {"get_customer", "get_customer_by_name"}
                and isinstance(output, dict)
                and output.get("customer_id") is not None
            ):
                customer_id = int(output["customer_id"])

            tool_results.append({
                "call_id": item["call_id"],
                "name": tool_name,
                "output": output
            })

        except Exception as exc:
            tool_results.append({
                "call_id": item["call_id"],
                "name": tool_name,
                "output": {"error": str(exc)}
            })

    result_update = {
    "tool_results": tool_results
    }

    if customer_id is not None:
        result_update["customer_id"] = customer_id

    return result_update


def continue_after_tools(state: AssistantState) -> dict:
    tool_results = state.get("tool_results", [])

    function_outputs = [
        {
            "type": "function_call_output",
            "call_id": item["call_id"],
            "output": json.dumps(
                item["output"],
                default=str
            )
        }
        for item in tool_results
    ]

    response = client.responses.create(
        model="gpt-5.6",
        previous_response_id=state["response_id"],
        input=function_outputs,
        tools=tools
    )
    print("\nMODEL OUTPUT:")

    for item in response.output:
        if item.type == "function_call":
            print("Tool name:", item.name)
            print("Raw arguments:", item.arguments)
        elif item.type == "message":
            print("Model message:", response.output_text)

    function_calls = [
        {
            "call_id": item.call_id,
            "name": item.name,
            "arguments": item.arguments
        }
        for item in response.output
        if item.type == "function_call"
    ]

    return {
        "response_id": response.id,
        "function_calls": function_calls,
        "tool_results": [],
        "result": response.output_text if not function_calls else ""
    }