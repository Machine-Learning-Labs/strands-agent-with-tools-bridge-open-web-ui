"""
Python REPL Agent - Specialised in Python code execution and analysis.
"""

from strands_tools import python_repl
from ..base_agent import BaseSpecialisedAgent
from typing import List, Any


class PythonReplAgent(BaseSpecialisedAgent):
    """
    Python REPL Agent specialising in Python code execution.
    
    This agent excels at running Python code, data analysis,
    scripting, and providing programming assistance using
    the python_repl tool from Strands Agents Tools.
    """
    
    def get_tools(self) -> List[Any]:
        """Return Python REPL tool."""
        return [python_repl]
    
    def get_system_prompt(self) -> str:
        """Return Python REPL-specific system prompt."""
        return """You are a Python REPL Agent, a Python programming and execution specialist.

Your expertise includes:
- Python code execution and debugging
- Data analysis with pandas, numpy, matplotlib
- File processing and manipulation
- Algorithm implementation and testing
- Library exploration and demonstration
- Code optimisation and best practices

You can execute Python code safely using the python_repl tool.
Always explain your code before running it, and interpret the results clearly.
When working with data, provide insights and visualisations where appropriate.

Follow Python best practices:
- Use clear, readable variable names
- Add comments for complex logic
- Handle exceptions appropriately
- Import only necessary modules

Respond in an educational manner, explaining both the code and its output."""
    
    def get_agent_name(self) -> str:
        """Return agent name."""
        return "Python REPL Agent"
    
    def get_agent_description(self) -> str:
        """Return agent description."""
        return "Specialised Python code execution agent for programming and data analysis"
    
    def get_agent_category(self) -> str:
        """Return agent category."""
        return "utility"