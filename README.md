# Stateful AI Assistant

A Python-based AI assistant demonstrating tool calling, multi-step execution, and conversation continuity using the OpenAI Responses API and LangGraph.

## Problem Statement

An assistant often needs to retrieve information from application data and use earlier conversation context to understand follow-up questions. This project demonstrates how an LLM can select predefined tools, execute them through Python, and use their results to answer users.

## Architecture

1. **User input:** Receives a natural-language request.
2. **Analyze request:** Sends the request to the OpenAI Responses API with available tool definitions.
3. **Execute tool:** Validates tool arguments using Pydantic and invokes the corresponding Python function through a tool registry.
4. **Return tool results:** Sends results to OpenAI using function-call outputs and their matching call IDs.
5. **Continue or finish:** The model can request another tool or generate a final answer.
6. **Conversation continuity:** OpenAI `previous_response_id` continues the model conversation; LangGraph checkpointing retains graph state per thread.

## Technology Stack

- Python
- OpenAI Responses API
- LangGraph
- Pydantic
- python-dotenv

## Project Structure

```text
stateful-ai-assistant/
├── main.py
├── functions/
│   ├── functions.py
│   └── registry.py
├── models/
│   └── models.py
├── tests/
├── docs/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

Adjust this tree to match the actual files in the repository.

## Setup

Create and activate a virtual environment, then install the dependencies.

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your own API key to the local `.env` file:

```text
OPENAI_API_KEY=your_api_key_here
```

Run the application:

```powershell
python main.py
```

Enter a query when prompted. Type `exit` or `quit` to end the session.

## Example Interaction

User: Find customer C101 and show their orders.

Assistant: Returns the customer's details and orders from the sample data.

User: Show their latest order.

Assistant: Uses the continuing conversation to interpret the follow-up.

These are illustrative examples; actual output depends on the tool implementation and sample data.

## Engineering Decisions

- **Tool registry:** Separates tool definitions from execution logic.
- **Pydantic validation:** Validates model-generated arguments before invoking Python functions.
- **LangGraph:** Separates request analysis, tool execution, and post-tool processing into graph nodes.
- **previous_response_id:** Continues the OpenAI Responses API conversation without manually resending the entire preceding message history.
- **Checkpointing:** Uses LangGraph's InMemorySaver to preserve graph state for a thread while the process remains running.

## Current Limitations

- InMemorySaver does not provide durable persistence across process restarts.
- The project uses demonstration customer and order data.
- Authentication, authorization, and production-grade deployment are not included in the current demo.
- Automated test coverage and additional reliability improvements are planned.

## Roadmap

- Improve handling of tool failures and invalid arguments.
- Add automated tests for successful execution and failure scenarios.
- Verify isolation between conversation threads.
- Document the graph architecture and test results.
- Evaluate durable checkpoint storage for a production-oriented implementation.

## Security

Never commit API keys, local environment files, real customer records, or confidential employer code. Use synthetic data and a local `.env` file excluded by `.gitignore`.