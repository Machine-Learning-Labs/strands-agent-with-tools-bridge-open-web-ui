"""
Base agent class for all specialised agents.
"""

from abc import ABC, abstractmethod
from strands import Agent
from strands.models import BedrockModel
from typing import List, Optional, Any


class BaseSpecialisedAgent(ABC):
    """
    Abstract base class for all specialised agents.

    Each agent is designed to excel at specific tasks using dedicated tools
    from the Strands Agents Tools library. This base class provides common
    functionality whilst allowing each agent to define its own specialisation.
    """

    def __init__(
        self,
        model_id: str = "us.amazon.nova-pro-v1:0",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        region_name: str = "us-west-2",
    ):
        """
        Initialise the specialised agent.

        Args:
            model_id: AWS Bedrock model identifier
            temperature: Model temperature for response generation (0.0-1.0)
            max_tokens: Maximum tokens for response generation
            region_name: AWS region for Bedrock service
        """
        self.model = BedrockModel(
            model_id=model_id,
            temperature=temperature,
            max_tokens=max_tokens,
            region_name=region_name,
            streaming=False,
        )

        self.agent = Agent(
            model=self.model,
            tools=self.get_tools(),
            system_prompt=self.get_system_prompt(),
        )

    @abstractmethod
    def get_tools(self) -> List[Any]:
        """
        Return the specific tools for this agent.

        Returns:
            List of tools that this agent specialises in using
        """
        pass

    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Return the system prompt for this agent.

        Returns:
            System prompt that defines the agent's personality and expertise
        """
        pass

    @abstractmethod
    def get_agent_name(self) -> str:
        """
        Return the agent's display name.

        Returns:
            Human-readable name for this agent
        """
        pass

    @abstractmethod
    def get_agent_description(self) -> str:
        """
        Return the agent's description.

        Returns:
            Brief description of what this agent does
        """
        pass

    def get_agent_category(self) -> str:
        """
        Return the agent's category.

        Returns:
            Category this agent belongs to (utility, files, web, etc.)
        """
        return "general"

    def get_tool_names(self) -> List[str]:
        """
        Return the names of tools this agent uses.

        Returns:
            List of tool names
        """
        tools = self.get_tools()
        return [getattr(tool, "__name__", str(tool)) for tool in tools]

    def invoke(self, message) -> str:
        """
        Process a message through the specialised agent.

        Args:
            message: User's input message (str or list of ContentBlocks)

        Returns:
            Agent's response as a string
        """
        try:
            result = self.agent(message)

            if result.message and "content" in result.message:
                content = result.message["content"]
                if isinstance(content, list) and len(content) > 0:
                    return content[0].get("text", "")

            return "I apologise, but I'm having difficulty processing your request at the moment."

        except Exception as e:
            return f"I apologise, but I encountered an issue: {str(e)}"

    async def ainvoke(self, message) -> str:
        """
        Asynchronously process a message through the specialised agent.

        Args:
            message: User's input message (str or list of ContentBlocks)

        Returns:
            Agent's response as a string
        """
        # For now, we'll use the synchronous version
        # In production, you might want to implement true async support
        return self.invoke(message)
