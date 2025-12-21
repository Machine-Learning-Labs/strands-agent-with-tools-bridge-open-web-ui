"""
Tavily Search Agent - Specialised in real-time web search and information retrieval.
"""

import os
from strands_tools.tavily import tavily_search
from ..base_agent import BaseSpecialisedAgent
from typing import List, Any


class TavilySearchAgent(BaseSpecialisedAgent):
    """
    Tavily Search Agent specialising in real-time web search.

    This agent excels at performing intelligent web searches,
    finding current information, and retrieving relevant content
    using the tavily_search tool from Strands Agents Tools.

    Requires TAVILY_API_KEY environment variable to be set.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialise the Tavily Search Agent.

        Validates that the TAVILY_API_KEY environment variable is set
        before initialising the parent class.

        Raises:
            ValueError: If TAVILY_API_KEY is not set or is empty
        """
        self._validate_tavily_api_key()
        super().__init__(*args, **kwargs)

    def _validate_tavily_api_key(self) -> None:
        """
        Validate that the Tavily API key is properly configured.

        Raises:
            ValueError: If TAVILY_API_KEY is not set or is empty
        """
        api_key = os.getenv("TAVILY_API_KEY")

        if not api_key:
            raise ValueError(
                "TAVILY_API_KEY environment variable is required for the Tavily Search Agent. "
                "Please set it in your .env file or environment variables. "
                "You can get an API key from https://tavily.com/"
            )

        if api_key.strip() == "":
            raise ValueError(
                "TAVILY_API_KEY environment variable is empty. "
                "Please provide a valid Tavily API key."
            )

        # Check if it's still the example placeholder
        if api_key.startswith("tvly-***-"):
            raise ValueError(
                "TAVILY_API_KEY appears to be the example placeholder. "
                "Please replace it with your actual Tavily API key from https://tavily.com/"
            )

    def get_tools(self) -> List[Any]:
        """Return Tavily search tool."""
        return [tavily_search]

    def get_system_prompt(self) -> str:
        """Return Tavily search-specific system prompt."""
        return """You are a Tavily Search Agent, a real-time web search and information retrieval specialist.

Your expertise includes:
- Performing intelligent web searches with relevant keywords
- Finding current news, trends, and up-to-date information
- Searching across different topics (general, news, research, etc.)
- Filtering and ranking search results by relevance
- Extracting key information from search results
- Providing comprehensive summaries of findings

You can search the web effectively and provide accurate, current information.
Always explain your search strategy and summarise findings clearly.
When presenting results, highlight the most relevant and reliable sources.

Best practices you follow:
- Use specific, targeted search queries
- Verify information from multiple sources when possible
- Provide source attribution for all information
- Filter results by relevance and reliability
- Summarise complex information clearly
- Stay current with real-time information

Important: If you encounter any issues with the Tavily API (such as authentication errors), 
inform the user that they may need to check their TAVILY_API_KEY configuration.

Respond in an educational manner, explaining both your search approach and the information found."""

    def get_agent_name(self) -> str:
        """Return agent name."""
        return "Tavily Search Agent"

    def get_agent_description(self) -> str:
        """Return agent description."""
        return (
            "Specialised real-time web search agent for current information retrieval"
        )

    def get_agent_category(self) -> str:
        """Return agent category."""
        return "web"
