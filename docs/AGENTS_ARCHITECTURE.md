# Specialised Agents Architecture

This document explains the architecture and design principles behind the specialised agents system in this repository.

## Overview

The specialised agents architecture is designed to provide task-specific AI assistants, each optimised for particular tools and capabilities from the Strands Agents Tools library. This modular approach offers several advantages over a single general-purpose agent.

## Design Principles

### 1. Single Responsibility
Each agent focuses on a specific set of related tools and tasks. This makes agents more predictable and easier to understand.

**Example**: The Calculator Agent only handles mathematical computations, whilst the File Read Agent focuses solely on reading and analysing files.

### 2. Tool Specialisation
Agents are organised around the tools they use, not arbitrary categories. An agent typically uses one tool (or multiple tools of the same type).

**Example**: The Tavily Search Agent uses `tavily_search`, whilst the Tavily Crawl Agent uses `tavily_crawl` - both are web-related but serve different purposes.

### 3. Educational Clarity
The code is written to be easily understood by developers learning about AI agents and the Strands SDK.

**Features**:
- Clear, descriptive names
- Extensive documentation
- Simple, straightforward implementations
- British English throughout

### 4. Extensibility
Adding new agents is straightforward and doesn't require modifying existing code (except for registration).

## Architecture Components

### Base Agent Class

```python
class BaseSpecialisedAgent(ABC):
    """Abstract base class for all specialised agents."""
```

The base class provides:
- Common initialisation logic
- Model configuration
- Message processing
- Abstract methods for customisation

**Key Methods**:
- `get_tools()` - Returns the tools this agent uses
- `get_system_prompt()` - Defines the agent's personality and expertise
- `get_agent_name()` - Human-readable name
- `get_agent_description()` - Brief description of capabilities
- `invoke()` / `ainvoke()` - Process messages

### Agent Categories

Agents are organised into logical categories:

#### Utility Agents (`agents/utility/`)
General-purpose computational tools:
- **Calculator Agent** (`calculator`) - Mathematical operations ✅ Implemented
- **Python REPL Agent** (`python-repl`) - Code execution ✅ Implemented  
- **HTTP Request Agent** (`http-request`) - Web API interactions ✅ Implemented

#### File Management Agents (`agents/files/`)
File system operations:
- **File Read Agent** (`file-read`) - Reading file contents ✅ Implemented
- **File Write Agent** (`file-write`) - Creating and writing files ✅ Implemented

#### Web & Search Agents (`agents/web/`)
Internet and web-related operations:
- **Tavily Search Agent** (`tavily-search`) - Real-time web search ✅ Implemented

#### Future Categories (Architecture Ready)
The following categories are prepared but not yet implemented:

**AWS Service Agents** (`agents/aws/`)
- AWS Agent - General AWS operations
- Bedrock Memory Agent - Knowledge base operations  
- Agent Core Memory Agent - Advanced memory management

**Communication Agents** (`agents/communication/`)
- Slack Agent - Slack integration
- RSS Agent - RSS feed management

**Media & Content Agents** (`agents/media/`)
- Nova Reels Agent - Video generation
- Stability AI Agent - Image generation
- Diagram Agent - Technical diagrams

**System Agents** (`agents/system/`)
- Environment Agent - Environment variables
- MCP Client Agent - Model Context Protocol
- Load Tool Agent - Dynamic tool loading

**Orchestration Agents** (`agents/orchestration/`)
- Batch Agent - Parallel execution
- Workflow Agent - Multi-step workflows
- Agent Graph Agent - Multi-agent systems
- Handoff Agent - User interaction

**Memory Management Agents** (`agents/memory/`)
- Retrieve Agent - Information retrieval
- Elasticsearch Memory Agent - Elasticsearch integration

### Agent Registry

```python
class AgentRegistry:
    """Central registry for all available specialised agents."""
```

The registry provides:
- **Agent Discovery**: List all available agents
- **Agent Creation**: Instantiate agents by ID
- **Categorisation**: Organise agents by category
- **Metadata**: Access agent information

**Key Methods**:
- `get_agent_class(agent_id)` - Get agent class by ID
- `create_agent(agent_id, **kwargs)` - Create agent instance
- `list_agents()` - List all agents with metadata
- `list_agents_by_category()` - Organised by category
- `get_agent_info(agent_id)` - Detailed agent information

### Service Layer

```python
class ChatService:
    """Service class handling chat completion logic."""
```

The service layer:
- Manages agent selection
- Converts message formats (OpenAI ↔ Strands)
- Handles multimodal content
- Estimates token usage
- Processes errors

**Agent Selection Logic**:
1. Check for explicit `agent_id` parameter
2. Fall back to `model` field in request
3. Default to Alfred Butler if neither specified

### API Layer

```python
app = FastAPI(title="Strands Agent OpenAI-Compatible API")
```

The API provides:
- **OpenAI-Compatible Endpoints**: `/v1/models`, `/v1/chat/completions`
- **Agent Discovery Endpoints**: `/v1/agents`, `/v1/agents/{agent_id}`
- **Category Browsing**: `/v1/agents/category/{category}`

## Message Flow

```
1. Client Request
   ↓
2. API Endpoint (/v1/chat/completions)
   ↓
3. Service Layer (ChatService)
   ↓
4. Agent Selection (Registry)
   ↓
5. Message Format Conversion
   ↓
6. Specialised Agent (invoke)
   ↓
7. Strands SDK (Agent with Tools)
   ↓
8. Bedrock Model (Nova Pro)
   ↓
9. Response Processing
   ↓
10. OpenAI-Compatible Response
```

## Creating a New Agent

### Step 1: Create Agent Class

```python
# src/agents/utility/my_agent.py
from strands_tools import my_tool
from ..base_agent import BaseSpecialisedAgent
from typing import List, Any

class MyAgent(BaseSpecialisedAgent):
    """My specialised agent description."""
    
    def get_tools(self) -> List[Any]:
        return [my_tool]
    
    def get_system_prompt(self) -> str:
        return """You are a specialist in...
        
Your expertise includes:
- Capability 1
- Capability 2
- Capability 3

You provide... [describe behaviour]"""
    
    def get_agent_name(self) -> str:
        return "My Agent"
    
    def get_agent_description(self) -> str:
        return "Brief description of what this agent does"
    
    def get_agent_category(self) -> str:
        return "utility"  # or files, web, aws, etc.
```

### Step 2: Register Agent

```python
# src/registry/agent_registry.py
from ..agents.utility.my_agent import MyAgent

class AgentRegistry:
    _agents: Dict[str, Type[BaseSpecialisedAgent]] = {
        # ... existing agents
        "my-agent": MyAgent,
    }
    
    _categories = {
        "utility": [..., "my-agent"],
        # ... other categories
    }
```

### Step 3: Test Agent

```bash
# List agents to verify registration
curl http://localhost:8000/v1/agents | jq '.agents[] | select(.id=="my-agent")'

# Get detailed information
curl http://localhost:8000/v1/agents/my-agent

# Test the agent
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "my-agent",
    "messages": [{"role": "user", "content": "Test message"}]
  }'
```

## Best Practices

### System Prompts

Good system prompts should:
1. **Define Expertise**: Clearly state what the agent specialises in
2. **List Capabilities**: Enumerate specific skills and functions
3. **Provide Guidance**: Explain how the agent should behave
4. **Be Educational**: Help users understand what the agent can do

**Example**:
```python
def get_system_prompt(self) -> str:
    return """You are a Calculator Agent, a mathematical computation specialist.

Your expertise includes:
- Arithmetic operations (addition, subtraction, multiplication, division)
- Advanced mathematical functions (trigonometry, logarithms, exponentials)
- Statistical calculations and data analysis

You provide accurate, step-by-step mathematical solutions.
Always show your working when solving complex problems."""
```

### Agent Names

- Use descriptive, clear names
- Follow the pattern: `[Function] Agent`
- Examples: "Calculator Agent", "File Read Agent", "HTTP Request Agent"

### Agent IDs

- Use lowercase with hyphens
- Match the tool name when possible
- Examples: `calculator`, `file-read`, `http-request`

### Tool Selection

An agent should use:
- **One tool** for most cases (single responsibility)
- **Multiple tools of the same type** when they're closely related
- **Never mix unrelated tools** (create separate agents instead)

### Error Handling

Agents should:
- Provide helpful error messages
- Explain what went wrong
- Suggest how to fix issues
- Maintain a polite, professional tone

## Configuration

### Model Configuration

All agents use the same base model configuration:
- **Model**: `us.amazon.nova-pro-v1:0` (default)
- **Temperature**: 0.7 (balanced)
- **Max Tokens**: 4096 (sufficient for most tasks)
- **Region**: us-west-2 (default)

These can be customised per agent if needed:

```python
class MyAgent(BaseSpecialisedAgent):
    def __init__(self):
        super().__init__(
            model_id="anthropic.claude-sonnet-4-20250514-v1:0",
            temperature=0.3,  # Lower for more deterministic responses
            max_tokens=8192   # Higher for longer responses
        )
```

### Environment Variables

Agents respect standard environment variables:
- `AWS_BEDROCK_API_KEY` - Bedrock API key
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `AWS_REGION` - AWS region

Tool-specific variables (see Strands Agents Tools documentation):
- `TAVILY_API_KEY` - For Tavily tools
- `STABILITY_API_KEY` - For Stability AI
- `SLACK_BOT_TOKEN` - For Slack integration
- And many more...

## Performance Considerations

### Agent Instantiation

Agents are instantiated on-demand:
- **Lazy Loading**: Agents are created only when needed
- **No Caching**: Each request creates a fresh agent instance
- **Stateless**: Agents don't maintain state between requests

For production, consider:
- Implementing agent pooling
- Caching agent instances
- Using connection pooling for external services

### Token Usage

Different agents have different token requirements:
- **Simple agents** (calculator): Low token usage
- **Code execution** (python-repl): Medium token usage
- **Web search** (tavily-search): High token usage (includes search results)

Monitor and optimise based on your use case.

## Security Considerations

### Tool Safety

Some tools require special consideration:
- **Python REPL**: Can execute arbitrary code
- **File Write**: Can modify the file system
- **MCP Client**: Can connect to external services
- **AWS Agent**: Can access AWS resources

**Recommendations**:
1. Run in isolated environments (containers)
2. Implement proper authentication
3. Use least-privilege IAM roles
4. Monitor and log all operations
5. Implement rate limiting

### API Security

The API includes basic security features:
- Header-based authentication (optional)
- Input validation (Pydantic models)
- Error message sanitisation
- CORS configuration

For production:
- Implement proper API key management
- Add rate limiting
- Use HTTPS
- Implement request signing
- Add audit logging

## Testing

### Unit Tests

Test individual agents:

```python
def test_calculator_agent():
    agent = CalculatorAgent()
    response = agent.invoke("What is 2 + 2?")
    assert "4" in response
```

### Integration Tests

Test the full flow:

```python
def test_agent_via_api():
    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "calculator",
            "messages": [{"role": "user", "content": "What is 5 * 6?"}]
        }
    )
    assert response.status_code == 200
    assert "30" in response.json()["choices"][0]["message"]["content"]
```

### Agent Registry Tests

Test agent discovery:

```python
def test_agent_registry():
    agents = AgentRegistry.list_agents()
    assert len(agents) > 0
    assert any(a["id"] == "calculator" for a in agents)
```

## Future Enhancements

The architecture is ready for these enhancements:

1. **Additional Agent Categories**: AWS, Communication, Media, System, Orchestration, Memory
2. **Agent Composition**: Combine multiple agents for complex tasks
3. **Agent Handoff**: Transfer between agents mid-conversation
4. **Streaming Responses**: Real-time response streaming
5. **Agent Memory**: Persistent memory across conversations
6. **Custom Models**: Per-agent model selection
7. **Performance Metrics**: Track agent performance and usage

**Current Status**: 6 specialised agents implemented, architecture ready for 25+ more agents across 6 additional categories.

## Conclusion

The specialised agents architecture provides a flexible, extensible, and educational framework for building task-specific AI assistants. By following the principles and patterns outlined in this document, you can create powerful, focused agents that excel at their designated tasks whilst maintaining code clarity and maintainability.