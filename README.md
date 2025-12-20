# Strands Agents SDK with Open Web UI - Specialised Agents Edition

This is an advanced version of the Strands Agents integration with Open Web UI, featuring **specialised agents** for different tasks and tools. Each agent is designed to excel at specific capabilities using dedicated tools from the Strands Agents Tools library.

## 🎯 What's New in Version 2.0

- **6 Specialised Agents**: Each agent focuses on specific tools and tasks
- **Organised by Category**: Agents are grouped into logical categories (utility, files, web)
- **Educational Design**: Simple, clear code structure perfect for learning
- **OpenAI Compatible**: Works seamlessly with Open Web UI and other OpenAI-compatible clients
- **Agent Discovery**: REST API endpoints to explore available agents and their capabilities
- **Extensible Architecture**: Ready for additional agent categories

## 🤖 Currently Implemented Agents

### Utility Agents (3 agents)
- **Calculator Agent** (`calculator`) - Mathematical computations and calculations
- **Python REPL Agent** (`python-repl`) - Python code execution and data analysis  
- **HTTP Request Agent** (`http-request`) - Web API interactions and HTTP operations

### File Management Agents (2 agents)
- **File Read Agent** (`file-read`) - Reading and analysing file contents
- **File Write Agent** (`file-write`) - Creating and writing file contents

### Web & Search Agents (1 agent)
- **Tavily Search Agent** (`tavily-search`) - Real-time web search and information retrieval

### Plus Alfred Butler
- **Alfred Butler** (`alfred-butler`) - Default conversational agent with British personality

**Total: 6 specialised agents + Alfred Butler = 7 available models**

## 🔮 Future Agent Categories (Architecture Ready)

The system is designed to easily add agents in these categories:
- **AWS Service Agents** - Bedrock Memory, AWS operations
- **Communication Agents** - Slack, RSS, notifications  
- **Media & Content Agents** - Image/video generation, diagrams
- **System Agents** - Environment management, MCP integration
- **Orchestration Agents** - Batch processing, workflows

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd strands-agents-sdk-with-open-web-ui/repo2

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Set up your credentials for the required services:

#### AWS Bedrock (Required)
```bash
# Option 1: Bedrock API Key (for development)
export AWS_BEDROCK_API_KEY=your_bedrock_api_key

# Option 2: AWS Credentials (for production)
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=us-west-2
```

#### Tavily API (Required for Tavily Search Agent)
```bash
# Get your API key from https://tavily.com/
export TAVILY_API_KEY=your_tavily_api_key
```

**Note**: The Tavily Search Agent requires a valid Tavily API key. You can get one for free at [https://tavily.com/](https://tavily.com/). Without this key, the Tavily Search Agent will not be available, but all other agents will work normally.

### 3. Run the API Server

```bash
# Start the server
python -m uvicorn src.api:app --host 0.0.0.0 --port 8000

# Or use the development server with auto-reload
python -m uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Test with Open Web UI

1. Open your Open Web UI instance
2. Add a new connection: `http://localhost:8000`
3. Select from available models/agents:
   - `alfred-butler` (default conversational agent)
   - `calculator` (mathematical computations)
   - `python-repl` (Python code execution)
   - `http-request` (web API interactions)
   - And many more!

## 📚 API Endpoints

### OpenAI-Compatible Endpoints
- `GET /v1/models` - List all available agents as models
- `POST /v1/chat/completions` - Chat with any agent
- `GET /v1/models/{model_id}` - Get specific agent/model info

### Agent Discovery Endpoints
- `GET /v1/agents` - List all agents with categories
- `GET /v1/agents/{agent_id}` - Get detailed agent information
- `GET /v1/agents/category/{category}` - Get agents by category

### Example: Using a Specific Agent

```bash
# Chat with the Calculator Agent
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "calculator",
    "messages": [
      {"role": "user", "content": "What is the square root of 144?"}
    ]
  }'

# Chat with the Python REPL Agent
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "python-repl",
    "messages": [
      {"role": "user", "content": "Create a simple plot of y = x^2 for x from -5 to 5"}
    ]
  }'
```

## 🏗️ Architecture

```
src/
├── agents/                    # Specialised agent implementations
│   ├── base_agent.py         # Abstract base class for all agents
│   ├── utility/              # General-purpose agents
│   ├── files/                # File management agents
│   ├── web/                  # Web and search agents
│   ├── aws/                  # AWS service agents
│   ├── communication/        # Messaging agents
│   ├── media/                # Content creation agents
│   ├── system/               # System operation agents
│   ├── orchestration/        # Workflow coordination agents
│   └── memory/               # Memory management agents
├── registry/                 # Agent discovery and management
│   └── agent_registry.py     # Central agent registry
├── api.py                    # FastAPI REST endpoints
├── service.py                # Business logic
├── models.py                 # Pydantic data models
└── agent.py                  # Original Alfred agent (still available)
```

## 🎓 Educational Features

This repository is designed for learning and understanding:

- **Simple Code Structure**: Each agent is self-contained and easy to understand
- **Clear Documentation**: Extensive comments and docstrings in British English
- **Modular Design**: Easy to add new agents or modify existing ones
- **Best Practices**: Follows Python and open-source conventions
- **Tool Integration**: Demonstrates how to use Strands Agents Tools effectively

## 🔧 Adding New Agents

To add a new specialised agent:

1. **Create the agent class** in the appropriate category directory:

```python
# src/agents/utility/my_new_agent.py
from strands_tools import my_tool
from ..base_agent import BaseSpecialisedAgent

class MyNewAgent(BaseSpecialisedAgent):
    def get_tools(self):
        return [my_tool]
    
    def get_system_prompt(self):
        return "You are a specialist in..."
    
    def get_agent_name(self):
        return "My New Agent"
    
    def get_agent_description(self):
        return "Specialised agent for..."
```

2. **Register the agent** in `src/registry/agent_registry.py`:

```python
from ..agents.utility.my_new_agent import MyNewAgent

class AgentRegistry:
    _agents = {
        # ... existing agents
        "my-new-agent": MyNewAgent,
    }
```

3. **Test your agent**:

```bash
# List all agents to verify registration
curl http://localhost:8000/v1/agents

# Test your new agent
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{"model": "my-new-agent", "messages": [{"role": "user", "content": "Hello!"}]}'
```

## 🆚 Comparison with Simple Version

| Feature | Simple Version (repo/) | Specialised Version (repo2/) |
|---------|----------------------|----------------------------|
| **Agents** | 1 (Alfred Butler) | 6 Specialised + Alfred |
| **Tools** | None | Calculator, Python, HTTP, Files, Search |
| **Organisation** | Single file | Categorised by function |
| **Discovery** | Fixed model | Dynamic agent registry |
| **Use Case** | General conversation | Task-specific expertise |
| **Learning** | Basic integration | Advanced architecture |

## 🛠️ Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements.dev.txt

# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests for any improvements.

## 🔗 Related Projects

- [Strands Agents SDK](https://github.com/strands-agents/sdk-python) - The core SDK
- [Strands Agents Tools](https://github.com/strands-agents/tools) - Community tools library
- [Open Web UI](https://github.com/open-webui/open-webui) - The web interface

---

**Note**: This is the advanced version with specialised agents. For a simpler implementation, see the `repo/` directory which contains the basic Alfred Butler agent.