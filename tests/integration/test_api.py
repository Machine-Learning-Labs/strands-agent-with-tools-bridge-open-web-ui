"""
Integration tests for FastAPI endpoints.
"""

import pytest
from unittest.mock import patch, Mock, AsyncMock

from src.models import ChatCompletionResponse, ChatCompletionChoice, Message, Usage


class TestRootEndpoint:
    """Test root endpoint."""

    def test_root_endpoint(self, client):
        """Test GET / endpoint."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Strands Agents - Specialised AI Assistant Collection"
        assert data["version"] == "2.0.0"
        assert data["default_model"] == "alfred-butler"
        assert "specialised-agents" in data["features"]
        assert data["specialised_agents"] >= 6  # At least 6 specialised agents


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check(self, client):
        """Test GET /health endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["agent"] == "alfred"


class TestModelsEndpoints:
    """Test model-related endpoints."""

    def test_list_models(self, client):
        """Test GET /v1/models endpoint."""
        response = client.get("/v1/models")

        assert response.status_code == 200
        data = response.json()
        assert data["object"] == "list"
        assert len(data["data"]) >= 7  # Alfred + 6 specialised agents

        # Check that alfred-butler is in the list
        model_ids = [model["id"] for model in data["data"]]
        assert "alfred-butler" in model_ids
        assert "calculator" in model_ids
        assert "python-repl" in model_ids

    def test_get_model_exists(self, client):
        """Test GET /v1/models/{model_id} for existing model."""
        response = client.get("/v1/models/alfred-butler")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "alfred-butler"
        assert data["object"] == "model"
        assert data["owned_by"] == "strands-agents"
        assert "created" in data

    def test_get_model_not_found(self, client):
        """Test GET /v1/models/{model_id} for non-existing model."""
        response = client.get("/v1/models/non-existent-model")

        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Model not found"


class TestAgentsEndpoints:
    """Test agent discovery endpoints."""

    def test_list_agents(self, client):
        """Test GET /v1/agents endpoint."""
        response = client.get("/v1/agents")

        assert response.status_code == 200
        data = response.json()
        assert "agents" in data
        assert "agents_by_category" in data
        assert "categories" in data
        assert "total_agents" in data

        # Check we have the expected agents
        agent_ids = [agent["id"] for agent in data["agents"]]
        expected_agents = [
            "calculator",
            "python-repl",
            "http-request",
            "file-read",
            "file-write",
            "tavily-search",
        ]
        for agent_id in expected_agents:
            assert agent_id in agent_ids

    def test_get_agent_info_exists(self, client):
        """Test GET /v1/agents/{agent_id} for existing agent."""
        response = client.get("/v1/agents/calculator")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "calculator"
        assert data["name"] == "Calculator Agent"
        assert data["category"] == "utility"
        assert "tools" in data

    def test_get_agent_info_not_found(self, client):
        """Test GET /v1/agents/{agent_id} for non-existing agent."""
        response = client.get("/v1/agents/non-existent-agent")

        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]

    def test_get_agents_by_category(self, client):
        """Test GET /v1/agents/category/{category} endpoint."""
        response = client.get("/v1/agents/category/utility")

        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "utility"
        assert "agents" in data
        assert "count" in data

        # Check utility agents are present
        agent_ids = [agent["id"] for agent in data["agents"]]
        assert "calculator" in agent_ids
        assert "python-repl" in agent_ids
        assert "http-request" in agent_ids

    def test_get_agents_by_invalid_category(self, client):
        """Test GET /v1/agents/category/{category} for invalid category."""
        response = client.get("/v1/agents/category/invalid-category")

        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]


class TestChatCompletionsEndpoint:
    """Test chat completions endpoint."""

    @patch("src.api.chat_service.process_chat_completion", new_callable=AsyncMock)
    def test_chat_completion_success(self, mock_process_chat_completion, client):
        """Test successful chat completion."""
        # Mock the service response
        mock_response = ChatCompletionResponse(
            id="chatcmpl-test123",
            created=1234567890,
            model="alfred-butler",
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=Message(role="assistant", content="Good day, sir!"),
                    finish_reason="stop",
                )
            ],
            usage=Usage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
        )

        # Configure the AsyncMock to return the response
        mock_process_chat_completion.return_value = mock_response

        # Make request
        request_data = {
            "model": "alfred-butler",
            "messages": [{"role": "user", "content": "Hello Alfred"}],
        }

        response = client.post("/v1/chat/completions", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "chatcmpl-test123"
        assert data["object"] == "chat.completion"
        assert data["model"] == "alfred-butler"
        assert len(data["choices"]) == 1
        assert data["choices"][0]["message"]["content"] == "Good day, sir!"
        assert data["usage"]["total_tokens"] == 15

    def test_chat_completion_invalid_request(self, client):
        """Test chat completion with invalid request data."""
        # Missing required fields
        request_data = {
            "model": "alfred-butler"
            # Missing messages
        }

        response = client.post("/v1/chat/completions", json=request_data)

        assert response.status_code == 422  # Validation error


class TestOpenAICompatibility:
    """Test OpenAI API compatibility."""

    @patch("src.api.chat_service.process_chat_completion", new_callable=AsyncMock)
    def test_openai_request_format(self, mock_process_chat_completion, client):
        """Test that the API accepts standard OpenAI request format."""
        mock_response = ChatCompletionResponse(
            id="chatcmpl-test123",
            created=1234567890,
            model="gpt-3.5-turbo",  # Different model name
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=Message(role="assistant", content="Hello!"),
                    finish_reason="stop",
                )
            ],
            usage=Usage(prompt_tokens=5, completion_tokens=2, total_tokens=7),
        )

        # Configure the AsyncMock to return the response
        mock_process_chat_completion.return_value = mock_response

        # Standard OpenAI format request
        request_data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello!"},
            ],
            "temperature": 0.7,
            "max_tokens": 150,
        }

        response = client.post("/v1/chat/completions", json=request_data)

        assert response.status_code == 200
        data = response.json()

        # Check OpenAI-compatible response format
        assert "id" in data
        assert data["object"] == "chat.completion"
        assert "created" in data
        assert "model" in data
        assert "choices" in data
        assert "usage" in data

        # Check choice format
        choice = data["choices"][0]
        assert choice["index"] == 0
        assert "message" in choice
        assert choice["message"]["role"] == "assistant"
        assert choice["message"]["content"] == "Hello!"
        assert choice["finish_reason"] == "stop"

        # Check usage format
        usage = data["usage"]
        assert "prompt_tokens" in usage
        assert "completion_tokens" in usage
        assert "total_tokens" in usage
