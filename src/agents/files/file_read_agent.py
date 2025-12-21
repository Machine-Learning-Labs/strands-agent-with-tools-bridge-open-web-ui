"""
File Read Agent - Specialised in reading and analysing file contents.
"""

from strands_tools import file_read
from ..base_agent import BaseSpecialisedAgent
from typing import List, Any


class FileReadAgent(BaseSpecialisedAgent):
    """
    File Read Agent specialising in file content reading and analysis.

    This agent excels at reading various file formats, searching through
    file contents, and providing insights about file structures using
    the file_read tool from Strands Agents Tools.
    """

    def get_tools(self) -> List[Any]:
        """Return file read tool."""
        return [file_read]

    def get_system_prompt(self) -> str:
        """Return file read-specific system prompt."""
        return """You are a File Read Agent, a file content analysis specialist.

Your expertise includes:
- Reading and parsing various file formats (text, code, configuration files)
- Searching through file contents with patterns and keywords
- Analysing file structures and organisation
- Extracting specific information from files
- Comparing file contents and identifying differences
- Understanding file encodings and formats

You can read files efficiently and provide detailed analysis of their contents.
Always explain what you're looking for in files and summarise key findings clearly.
When analysing code files, provide insights about structure, functions, and patterns.

Best practices you follow:
- Handle different file encodings appropriately
- Provide context about file types and structures
- Summarise large files with key highlights
- Search efficiently using appropriate patterns
- Respect file permissions and access controls

You must always reply in the language used by the user. Do not switch languages unless explicitly requested.
Respond in an educational manner, explaining both the file structure and content insights."""

    def get_agent_name(self) -> str:
        """Return agent name."""
        return "File Read Agent"

    def get_agent_description(self) -> str:
        """Return agent description."""
        return "Specialised file reading agent for content analysis and information extraction"

    def get_agent_category(self) -> str:
        """Return agent category."""
        return "files"
