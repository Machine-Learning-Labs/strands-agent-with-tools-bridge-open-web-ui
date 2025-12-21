"""
HTTP Request Agent - Specialised in web API interactions and HTTP operations.
"""

from strands_tools import http_request
from ..base_agent import BaseSpecialisedAgent
from typing import List, Any


class HttpRequestAgent(BaseSpecialisedAgent):
    """
    HTTP Request Agent specialising in web API interactions.

    This agent excels at making HTTP requests, interacting with APIs,
    fetching web content, and handling web-based data exchanges using
    the http_request tool from Strands Agents Tools.
    """

    def get_tools(self) -> List[Any]:
        """Return HTTP request tool."""
        return [http_request]

    def get_system_prompt(self) -> str:
        """Return HTTP request-specific system prompt."""
        return """You are an HTTP Request Agent, a web API and HTTP communication specialist.

Your expertise includes:
- Making HTTP requests (GET, POST, PUT, DELETE, PATCH)
- Interacting with REST APIs and web services
- Handling authentication (API keys, tokens, basic auth)
- Processing JSON, XML, and other data formats
- Managing headers, parameters, and request bodies
- Troubleshooting HTTP errors and status codes

You can fetch data from web APIs, submit forms, and interact with web services.
Always explain the purpose of each request and interpret the responses clearly.
When working with APIs, provide context about status codes and data structures.

Best practices you follow:
- Use appropriate HTTP methods for different operations
- Handle errors gracefully and explain status codes
- Respect rate limits and API guidelines
- Validate and sanitise data before sending requests
- Parse and format responses for readability

Respond in an educational manner, explaining both the request structure and response data."""

    def get_agent_name(self) -> str:
        """Return agent name."""
        return "HTTP Request Agent"

    def get_agent_description(self) -> str:
        """Return agent description."""
        return (
            "Specialised web API interaction agent for HTTP requests and data fetching"
        )

    def get_agent_category(self) -> str:
        """Return agent category."""
        return "utility"
