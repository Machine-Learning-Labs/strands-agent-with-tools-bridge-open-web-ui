"""
Registry for all available specialised agents.
"""

from typing import Dict, Type, List, Optional
from .agents.base_agent import BaseSpecialisedAgent

# Import utility agents
from .agents.utility.calculator_agent import CalculatorAgent
from .agents.utility.python_repl_agent import PythonReplAgent
from .agents.utility.http_request_agent import HttpRequestAgent

# Import file agents
from .agents.files.file_read_agent import FileReadAgent
from .agents.files.file_write_agent import FileWriteAgent

# Import web agents
from .agents.web.tavily_search_agent import TavilySearchAgent

# Import base agents
from .agents.base.alfred_agent import AlfredAgent


class AgentRegistry:
    """
    Central registry for all available specialised agents.

    This registry manages the mapping between agent names and their corresponding
    classes, providing a centralised way to discover and instantiate agents.
    """

    # Registry mapping agent IDs to their classes
    _agents: Dict[str, Type[BaseSpecialisedAgent]] = {
        # Base agents
        "alfred-butler": AlfredAgent,
        # Utility agents
        "calculator": CalculatorAgent,
        "python-repl": PythonReplAgent,
        "http-request": HttpRequestAgent,
        # File agents
        "file-read": FileReadAgent,
        "file-write": FileWriteAgent,
        # Web agents
        "tavily-search": TavilySearchAgent,
    }

    # Category mapping for organisation
    _categories = {
        "base": ["alfred-butler"],
        "utility": ["calculator", "python-repl", "http-request"],
        "files": ["file-read", "file-write"],
        "web": ["tavily-search"],
        "aws": [],
        "communication": [],
        "media": [],
        "system": [],
        "orchestration": [],
        "memory": [],
    }

    @classmethod
    def get_agent_class(cls, agent_id: str) -> Type[BaseSpecialisedAgent]:
        """
        Get an agent class by its ID.

        Args:
            agent_id: The unique identifier for the agent

        Returns:
            The agent class

        Raises:
            ValueError: If the agent ID is not found
        """
        if agent_id not in cls._agents:
            available_agents = ", ".join(cls._agents.keys())
            raise ValueError(
                f"Agent '{agent_id}' not found. Available agents: {available_agents}"
            )
        return cls._agents[agent_id]

    @classmethod
    def create_agent(cls, agent_id: str, **kwargs) -> BaseSpecialisedAgent:
        """
        Create an instance of the specified agent.

        Args:
            agent_id: The unique identifier for the agent
            **kwargs: Additional arguments to pass to the agent constructor

        Returns:
            An instance of the specified agent
        """
        agent_class = cls.get_agent_class(agent_id)
        return agent_class(**kwargs)

    @classmethod
    def list_agents(cls) -> List[Dict[str, str]]:
        """
        List all available agents with their metadata.

        Returns:
            List of dictionaries containing agent information
        """
        agents = []
        for agent_id, agent_class in cls._agents.items():
            # Create temporary instance to get metadata
            try:
                temp_instance = agent_class()
                agents.append(
                    {
                        "id": agent_id,
                        "name": temp_instance.get_agent_name(),
                        "description": temp_instance.get_agent_description(),
                        "category": temp_instance.get_agent_category(),
                        "tools": temp_instance.get_tool_names(),
                    }
                )
            except Exception as e:
                # If agent creation fails, provide basic info
                agents.append(
                    {
                        "id": agent_id,
                        "name": agent_class.__name__,
                        "description": f"Agent class: {agent_class.__name__}",
                        "category": cls._get_category_for_agent(agent_id),
                        "tools": [],
                        "error": str(e),
                    }
                )
        return agents

    @classmethod
    def list_agents_by_category(cls) -> Dict[str, List[Dict[str, str]]]:
        """
        List all agents organised by category.

        Returns:
            Dictionary with categories as keys and agent lists as values
        """
        all_agents = cls.list_agents()
        categorised = {}

        for category in cls._categories.keys():
            categorised[category] = [
                agent for agent in all_agents if agent.get("category") == category
            ]

        return categorised

    @classmethod
    def get_agent_info(cls, agent_id: str) -> Optional[Dict[str, str]]:
        """
        Get detailed information about a specific agent.

        Args:
            agent_id: The unique identifier for the agent

        Returns:
            Dictionary containing agent information, or None if not found
        """
        if agent_id not in cls._agents:
            return None

        try:
            agent_class = cls._agents[agent_id]
            temp_instance = agent_class()
            return {
                "id": agent_id,
                "name": temp_instance.get_agent_name(),
                "description": temp_instance.get_agent_description(),
                "category": temp_instance.get_agent_category(),
                "tools": temp_instance.get_tool_names(),
                "class_name": agent_class.__name__,
                "module": agent_class.__module__,
            }
        except Exception as e:
            return {
                "id": agent_id,
                "error": str(e),
                "class_name": cls._agents[agent_id].__name__,
            }

    @classmethod
    def _get_category_for_agent(cls, agent_id: str) -> str:
        """
        Get the category for a specific agent ID.

        Args:
            agent_id: The agent identifier

        Returns:
            The category name, or 'general' if not found
        """
        for category, agent_ids in cls._categories.items():
            if agent_id in agent_ids:
                return category
        return "general"

    @classmethod
    def get_available_categories(cls) -> List[str]:
        """
        Get list of all available categories.

        Returns:
            List of category names
        """
        return list(cls._categories.keys())

    @classmethod
    def register_agent(
        cls,
        agent_id: str,
        agent_class: Type[BaseSpecialisedAgent],
        category: str = "general",
    ):
        """
        Register a new agent in the registry.

        Args:
            agent_id: Unique identifier for the agent
            agent_class: The agent class to register
            category: Category to place the agent in
        """
        cls._agents[agent_id] = agent_class

        if category not in cls._categories:
            cls._categories[category] = []

        if agent_id not in cls._categories[category]:
            cls._categories[category].append(agent_id)
