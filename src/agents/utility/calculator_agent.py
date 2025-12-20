"""
Calculator Agent - Specialised in mathematical calculations.
"""

from strands_tools import calculator
from ..base_agent import BaseSpecialisedAgent
from typing import List, Any


class CalculatorAgent(BaseSpecialisedAgent):
    """
    Calculator Agent specialising in mathematical calculations.
    
    This agent excels at performing arithmetic operations, 
    mathematical functions, and numerical computations using
    the calculator tool from Strands Agents Tools.
    """
    
    def get_tools(self) -> List[Any]:
        """Return calculator tool."""
        return [calculator]
    
    def get_system_prompt(self) -> str:
        """Return calculator-specific system prompt."""
        return """You are a Calculator Agent, a mathematical computation specialist.

Your expertise includes:
- Arithmetic operations (addition, subtraction, multiplication, division)
- Advanced mathematical functions (trigonometry, logarithms, exponentials)
- Statistical calculations and data analysis
- Unit conversions and mathematical transformations
- Complex mathematical problem solving

You provide accurate, step-by-step mathematical solutions and explanations.
Always show your working when solving complex problems and use the calculator 
tool for all numerical computations to ensure precision and accuracy.

Respond in a clear, educational manner suitable for learning purposes.
When explaining solutions, break down complex problems into manageable steps."""
    
    def get_agent_name(self) -> str:
        """Return agent name."""
        return "Calculator Agent"
    
    def get_agent_description(self) -> str:
        """Return agent description."""
        return "Specialised mathematical computation agent for arithmetic and advanced calculations"
    
    def get_agent_category(self) -> str:
        """Return agent category."""
        return "utility"