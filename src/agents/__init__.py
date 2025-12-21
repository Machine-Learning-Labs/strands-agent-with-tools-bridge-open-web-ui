"""
Specialised Agents Package

This package contains specialised agents, each designed to excel at specific tasks
using dedicated tools from the Strands Agents Tools library.
"""

from .base_agent import BaseSpecialisedAgent

# Import all base agents
from .base.alfred_agent import AlfredAgent

# Import all utility agents
from .utility.calculator_agent import CalculatorAgent
from .utility.python_repl_agent import PythonReplAgent
from .utility.http_request_agent import HttpRequestAgent

# Import all file agents
from .files.file_read_agent import FileReadAgent
from .files.file_write_agent import FileWriteAgent

# Import all web agents
from .web.tavily_search_agent import TavilySearchAgent

__all__ = [
    "BaseSpecialisedAgent",
    "AlfredAgent",
    "CalculatorAgent",
    "PythonReplAgent",
    "HttpRequestAgent",
    "FileReadAgent",
    "FileWriteAgent",
    "TavilySearchAgent",
]
