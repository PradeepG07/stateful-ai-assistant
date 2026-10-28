from typing import TypedDict

class AssistantState(TypedDict, total=False):
    user_query: str
    function_calls: list[dict]
    response_id: str
    tool_results: list[dict]
    result: str
    error: str
    customer_id: int
