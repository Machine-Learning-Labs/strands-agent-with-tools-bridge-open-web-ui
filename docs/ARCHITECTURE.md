# Architecture Overview - Specialised Agents Edition

## System Components

This project demonstrates an advanced integration between Open Web UI and AWS Strands Agents SDK through an OpenAI-compatible API layer, featuring multiple specialised agents.

### Component Flow

```
┌─────────────────┐
│   Open Web UI   │  (Port 3000)
│   Web Interface │
└────────┬────────┘
         │ HTTP Requests
         │ (OpenAI API Format)
         ▼
┌─────────────────┐
│   Agent API     │  (Port 8000)
│  FastAPI Server │
│  /v1/models     │
│  /v1/chat/...   │
│  /v1/agents     │
└────────┬────────┘
         │ Agent Selection
         ▼
┌─────────────────┐
│ Agent Registry  │
│ 6 Specialised   │
│ Agents + Alfred │
└────────┬────────┘
         │ Tool Integration
         ▼
┌─────────────────┐
│ Strands Tools   │
│ calculator      │
│ python_repl     │
│ http_request    │
│ file_read/write │
│ tavily_search   │
└────────┬────────┘
         │ Model Calls
         ▼
┌─────────────────┐
│  AWS Bedrock    │
│   Nova Pro v1   │
└─────────────────┘
```

## Key Integration Points

### 1. OpenAI API Compatibility Layer (`src/api.py`)

The FastAPI application provides OpenAI-compatible endpoints plus agent discovery:

- **GET /v1/models**: Lists all available agents as "models" (7 total)
- **POST /v1/chat/completions**: Routes messages to appropriate specialised agents
- **GET /v1/agents**: Discovers available agents and their capabilities
- **GET /v1/agents/{agent_id}**: Gets detailed agent information
- **GET /v1/agents/category/{category}**: Browses agents by category

### 2. Agent Registry System (`src/registry/agent_registry.py`)

The registry manages all specialised agents:

- **Agent Discovery**: Lists available agents with metadata
- **Dynamic Instantiation**: Creates agents on-demand
- **Category Organisation**: Groups agents by functionality
- **Error Handling**: Gracefully handles configuration issues

### 3. Specialised Agents (`src/agents/`)

Each agent is optimised for specific tasks:

- **Calculator Agent**: Mathematical computations using `calculator` tool
- **Python REPL Agent**: Code execution using `python_repl` tool  
- **HTTP Request Agent**: Web APIs using `http_request` tool
- **File Read Agent**: File analysis using `file_read` tool
- **File Write Agent**: File creation using `file_write` tool
- **Tavily Search Agent**: Web search using `tavily_search` tool
- **Alfred Butler**: General conversation (original agent)

### 4. Request Flow

1. User selects agent/model in Open Web UI
2. Open Web UI makes POST request to `/v1/chat/completions` with model ID
3. API routes to appropriate specialised agent via registry
4. Agent processes message using its dedicated tools
5. Tools interact with Strands SDK and external services
6. Response formatted as OpenAI completion
7. Open Web UI displays the specialised response

## Configuration

### Environment Variables

- **AWS Credentials**: Required for Bedrock access
- **OPENAI_API_KEY**: Used for service-to-service authentication
- **Database**: PostgreSQL connection details for Open Web UI

### Docker Networking

All services communicate through the `strands-network` bridge network:

- Services reference each other by container name
- Open Web UI connects to `http://agent-api:8000/v1`
- Agent API and Open Web UI both connect to `postgres:5432`

## Security Considerations

This is a demonstration project. For production use:

1. Implement proper API key validation
2. Add rate limiting
3. Use secrets management for credentials
4. Enable HTTPS/TLS
5. Implement proper error handling and logging
6. Add authentication and authorisation
7. Use environment-specific configurations

## Extending the System

### Adding New Specialised Agents

1. Create new agent class in appropriate category folder (`src/agents/category/`)
2. Inherit from `BaseSpecialisedAgent` 
3. Implement required methods (`get_tools()`, `get_system_prompt()`, etc.)
4. Register in `src/registry/agent_registry.py`
5. Agent automatically appears in `/v1/models` and `/v1/agents`

### Adding Tools to Existing Agents

Strands SDK supports multiple tools per agent:

```python
from strands_tools import calculator, python_repl

class MathPythonAgent(BaseSpecialisedAgent):
    def get_tools(self):
        return [calculator, python_repl]  # Multiple related tools
```

### Environment Configuration

Each agent can require specific environment variables:

```python
class TavilySearchAgent(BaseSpecialisedAgent):
    def __init__(self):
        self._validate_tavily_api_key()  # Check TAVILY_API_KEY
        super().__init__()
```

### Streaming Support

To add streaming responses:

1. Enable streaming in Bedrock model
2. Implement Server-Sent Events (SSE) in API
3. Stream tokens as they arrive from Bedrock
