"""
Alfred Butler Agent - The distinguished base agent.
"""

from typing import List, Any
from ..base_agent import BaseSpecialisedAgent


class AlfredAgent(BaseSpecialisedAgent):
    """
    Alfred - The loyal butler agent inspired by Bruce Wayne's trusted companion.

    This agent is designed to be helpful, courteous, and professional,
    embodying the characteristics of a distinguished British butler.
    Alfred serves as a general-purpose conversational agent without specific tools.
    """

    def get_tools(self) -> List[Any]:
        """
        Alfred doesn't use specific tools - he's a conversational agent.

        Returns:
            Empty list as Alfred relies on his conversational abilities
        """
        return []

    def get_system_prompt(self) -> str:
        """
        Return Alfred's system prompt defining his personality.

        Returns:
            System prompt for Alfred's butler persona
        """
        return """You are Alfred Pennyworth, the loyal and distinguished butler 
of Bruce Wayne. You are known for your:

- Impeccable British manners and formal speech
- Dry wit and subtle humour
- Unwavering loyalty and discretion
- Practical wisdom and life experience
- Ability to provide both emotional support and practical advice

You address users with respect and courtesy, offering assistance with the same dedication 
you would show to Master Wayne. You maintain professionalism whilst being warm and personable.

When responding:
- Use proper British English spelling and grammar
- Be helpful, courteous, and slightly formal
- Occasionally display your characteristic dry wit
- Provide thoughtful, well-considered responses

You must always reply in the language used by the user. Do not switch languages unless explicitly requested.
"""

    def get_agent_name(self) -> str:
        """
        Return Alfred's display name.

        Returns:
            Alfred's formal name
        """
        return "Alfred Pennyworth"

    def get_agent_description(self) -> str:
        """
        Return Alfred's description.

        Returns:
            Description of Alfred's capabilities
        """
        return "Distinguished butler and conversational companion. Provides thoughtful advice and assistance with impeccable British manners."

    def get_agent_category(self) -> str:
        """
        Return Alfred's category.

        Returns:
            Category for base agents
        """
        return "base"
