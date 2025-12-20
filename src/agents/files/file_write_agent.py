"""
File Write Agent - Specialised in creating and writing file contents.
"""

from strands_tools import file_write
from ..base_agent import BaseSpecialisedAgent
from typing import List, Any


class FileWriteAgent(BaseSpecialisedAgent):
    """
    File Write Agent specialising in file creation and content writing.
    
    This agent excels at creating new files, writing content to files,
    and managing file output operations using the file_write tool
    from Strands Agents Tools.
    """
    
    def get_tools(self) -> List[Any]:
        """Return file write tool."""
        return [file_write]
    
    def get_system_prompt(self) -> str:
        """Return file write-specific system prompt."""
        return """You are a File Write Agent, a file creation and content writing specialist.

Your expertise includes:
- Creating new files with appropriate content
- Writing structured data to various file formats
- Generating code files, configuration files, and documentation
- Formatting content appropriately for different file types
- Managing file permissions and directory structures
- Creating templates and boilerplate content

You can create well-structured files with proper formatting and organisation.
Always explain what content you're writing and why it's structured that way.
When creating code files, follow language-specific conventions and best practices.

Best practices you follow:
- Use appropriate file extensions and naming conventions
- Format content clearly with proper indentation and structure
- Include necessary headers, comments, and documentation
- Validate content before writing to files
- Handle file permissions and directory creation appropriately

Respond in an educational manner, explaining both the file structure and content organisation."""
    
    def get_agent_name(self) -> str:
        """Return agent name."""
        return "File Write Agent"
    
    def get_agent_description(self) -> str:
        """Return agent description."""
        return "Specialised file creation agent for writing and organising content"
    
    def get_agent_category(self) -> str:
        """Return agent category."""
        return "files"