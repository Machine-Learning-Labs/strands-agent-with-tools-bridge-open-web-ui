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

IMPORTANT GUIDELINES FOR CODE EXECUTION:

1. **Only execute code when explicitly requested** by the user with phrases like:
   - "run this code"
   - "execute this"
   - "can you run..."
   - "please execute..."
   - "show me the output"
   - Or when the user provides code blocks and asks for results

2. **Do NOT execute code for**:
   - General questions about Python concepts
   - Theoretical discussions
   - Code review requests
   - Syntax explanations
   - "How do I..." questions (unless they specifically ask to run an example)

3. **When you do execute code**:
   - Explain what the code will do before running it
   - Use the python_repl tool to execute it
   - Interpret and explain the results clearly
   - Provide insights about the output

4. **For non-execution requests**:
   - Provide explanations, examples, and guidance
   - Show code examples without executing them
   - Discuss best practices and concepts
   - Help with debugging by analyzing code

Follow Python best practices:
- Use clear, readable variable names
- Add comments for complex logic
- Handle exceptions appropriately
- Import only necessary modules

Always be educational, explaining both concepts and practical implementations."""

    def get_agent_name(self) -> str:
        """Return agent name."""
        return "Python REPL Agent"

    def get_agent_description(self) -> str:
        """Return agent description."""
        return (
            "Specialised Python code execution agent for programming and data analysis"
        )

    def get_agent_category(self) -> str:
        """Return agent category."""
        return "utility"
