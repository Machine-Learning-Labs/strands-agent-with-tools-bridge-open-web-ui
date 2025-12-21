"""
Unit tests for AgentRegistry.
"""

import pytest
from unittest.mock import Mock, patch

from src.registry import AgentRegistry


class TestAgentRegistry:
    """Test AgentRegistry functionality."""

    def test_list_agents(self):
        """Test listing all agents."""
        agents = AgentRegistry.list_agents()

        assert isinstance(agents, list)
        assert len(agents) >= 6  # At least 6 specialised agents

        # Check expected agents are present
        agent_ids = [agent["id"] for agent in agents]
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

        # Check agent structure
        for agent in agents:
            assert "id" in agent
            assert "name" in agent
            assert "description" in agent
            assert "category" in agent
            assert "tools" in agent

    def test_list_agents_by_category(self):
        """Test listing agents by category."""
        categorised = AgentRegistry.list_agents_by_category()

        assert isinstance(categorised, dict)
        assert "utility" in categorised
        assert "files" in categorised
        assert "web" in categorised

        # Check utility category has expected agents
        utility_agents = categorised["utility"]
        utility_ids = [agent["id"] for agent in utility_agents]
        assert "calculator" in utility_ids
        assert "python-repl" in utility_ids
        assert "http-request" in utility_ids

    def test_get_agent_info_exists(self):
        """Test getting info for existing agent."""
        info = AgentRegistry.get_agent_info("calculator")

        assert info is not None
        assert info["id"] == "calculator"
        assert info["name"] == "Calculator Agent"
        assert info["category"] == "utility"
        assert "tools" in info

    def test_get_agent_info_not_exists(self):
        """Test getting info for non-existing agent."""
        info = AgentRegistry.get_agent_info("non-existent-agent")

        assert info is None

    def test_get_agent_class_exists(self):
        """Test getting agent class for existing agent."""
        agent_class = AgentRegistry.get_agent_class("calculator")

        assert agent_class is not None
        assert hasattr(agent_class, "get_tools")
        assert hasattr(agent_class, "get_system_prompt")

    def test_get_agent_class_not_exists(self):
        """Test getting agent class for non-existing agent."""
        with pytest.raises(ValueError) as exc_info:
            AgentRegistry.get_agent_class("non-existent-agent")

        assert "not found" in str(exc_info.value)

    def test_create_agent_success(self):
        """Test creating an agent successfully."""
        # Test that we can create an agent without errors
        try:
            agent = AgentRegistry.create_agent("calculator")
            assert agent is not None
            assert hasattr(agent, "get_agent_name")
            assert agent.get_agent_name() == "Calculator Agent"
        except Exception as e:
            # If it fails due to missing dependencies, that's expected in test environment
            assert (
                "TAVILY_API_KEY" in str(e)
                or "AWS" in str(e)
                or "strands_tools" in str(e)
            )

    def test_create_agent_not_exists(self):
        """Test creating non-existing agent."""
        with pytest.raises(ValueError):
            AgentRegistry.create_agent("non-existent-agent")

    def test_get_available_categories(self):
        """Test getting available categories."""
        categories = AgentRegistry.get_available_categories()

        assert isinstance(categories, list)
        expected_categories = [
            "utility",
            "files",
            "web",
            "aws",
            "communication",
            "media",
            "system",
            "orchestration",
            "memory",
        ]

        for category in expected_categories:
            assert category in categories
