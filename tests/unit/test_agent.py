"""
Unit tests for AlfredAgent.
"""

import pytest
from unittest.mock import Mock, patch

from src.agents.base.alfred_agent import AlfredAgent


class TestAlfredAgent:
    """Test AlfredAgent class."""

    @patch("src.agents.base_agent.BedrockModel")
    @patch("src.agents.base_agent.Agent")
    def test_init_default_params(self, mock_agent_class, mock_bedrock_model):
        """Test AlfredAgent initialization with default parameters."""
        mock_model = Mock()
        mock_bedrock_model.return_value = mock_model
        mock_agent = Mock()
        mock_agent_class.return_value = mock_agent

        agent = AlfredAgent()

        # Check BedrockModel was created with correct parameters
        mock_bedrock_model.assert_called_once_with(
            model_id="us.amazon.nova-pro-v1:0",
            temperature=0.7,
            max_tokens=4096,
            region_name="us-west-2",
            streaming=False,
        )

        # Check Agent was created with model, tools, and system prompt
        mock_agent_class.assert_called_once()
        call_args = mock_agent_class.call_args
        assert call_args[1]["model"] == mock_model
        assert call_args[1]["tools"] == []  # Alfred has no tools
        assert "Alfred Pennyworth" in call_args[1]["system_prompt"]

        assert agent.model == mock_model
        assert agent.agent == mock_agent

    def test_agent_metadata(self):
        """Test agent metadata methods."""
        with patch("src.agents.base_agent.BedrockModel"), patch(
            "src.agents.base_agent.Agent"
        ):
            agent = AlfredAgent()

            assert agent.get_agent_name() == "Alfred Pennyworth"
            assert "butler" in agent.get_agent_description().lower()
            assert agent.get_agent_category() == "base"
            assert agent.get_tools() == []
            assert agent.get_tool_names() == []

    def test_system_prompt_content(self):
        """Test that system prompt contains expected Alfred characteristics."""
        with patch("src.agents.base_agent.BedrockModel"), patch(
            "src.agents.base_agent.Agent"
        ):
            agent = AlfredAgent()

            prompt = agent.get_system_prompt()
            assert "Alfred Pennyworth" in prompt
            assert "British manners" in prompt
            assert "dry wit" in prompt
            assert "loyalty" in prompt
            assert "Master Wayne" in prompt


class TestAlfredAgentInvoke:
    """Test AlfredAgent invoke methods."""

    @pytest.fixture
    def mock_agent(self):
        """Create a mock agent with proper response structure."""
        with patch("src.agents.base_agent.BedrockModel"), patch(
            "src.agents.base_agent.Agent"
        ) as mock_agent_class:
            mock_agent_instance = Mock()
            mock_agent_class.return_value = mock_agent_instance

            alfred = AlfredAgent()
            alfred.agent = mock_agent_instance
            return alfred, mock_agent_instance

    def test_invoke_successful_response(self, mock_agent):
        """Test successful invoke with proper response structure."""
        alfred, mock_agent_instance = mock_agent

        # Mock successful response
        mock_result = Mock()
        mock_result.message = {
            "content": [{"text": "Good day, sir. How may I assist you?"}]
        }
        mock_agent_instance.return_value = mock_result

        result = alfred.invoke("Hello Alfred")

        assert result == "Good day, sir. How may I assist you?"
        mock_agent_instance.assert_called_once_with("Hello Alfred")

    def test_invoke_empty_content(self, mock_agent):
        """Test invoke with empty content response."""
        alfred, mock_agent_instance = mock_agent

        # Mock response with empty content
        mock_result = Mock()
        mock_result.message = {"content": []}
        mock_agent_instance.return_value = mock_result

        result = alfred.invoke("Hello Alfred")

        assert "difficulty processing your request" in result

    def test_invoke_exception_handling(self, mock_agent):
        """Test invoke exception handling."""
        alfred, mock_agent_instance = mock_agent

        # Mock agent raising exception
        mock_agent_instance.side_effect = Exception("Test error")

        result = alfred.invoke("Hello Alfred")

        assert "I apologise, but I encountered an issue" in result
        assert "Test error" in result
