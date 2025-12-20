"""
OpenAI-compatible REST API endpoints for Strands Agent integration with Open Web UI.
"""

import time
from typing import Optional
from fastapi import FastAPI, HTTPException, Header, Query

from .models import ChatCompletionRequest, ChatCompletionResponse, ModelList, Model
from .service import ChatService
from .registry import AgentRegistry


# Initialize FastAPI application
app = FastAPI(
    title="Strands Agent OpenAI-Compatible API",
    description="OpenAI-compatible API for Strands Agents integration with Open Web UI",
    version="1.0.0",
)

# Initialize chat service
chat_service = ChatService()


@app.get("/")
async def root():
    """Root endpoint providing API information."""
    return {
        "message": "Strands Agents - Specialised AI Assistant Collection",
        "version": "2.0.0",
        "default_model": "alfred-butler",
        "features": ["text", "images", "multimodal", "specialised-agents"],
        "endpoints": {
            "models": "/v1/models",
            "chat": "/v1/chat/completions",
            "agents": "/v1/agents",
            "agent_info": "/v1/agents/{agent_id}"
        },
        "specialised_agents": len(AgentRegistry.list_agents()),
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agent": "alfred"}


@app.get("/v1/models")
async def list_models() -> ModelList:
    """
    List available models (OpenAI-compatible endpoint).

    Returns a list of available models that Open Web UI can use,
    including the default Alfred agent and all specialised agents.
    """
    models = [
        Model(
            id="alfred-butler", 
            created=int(time.time()), 
            owned_by="strands-agents"
        )
    ]
    
    # Add specialised agents as models
    for agent in AgentRegistry.list_agents():
        models.append(
            Model(
                id=agent["id"],
                created=int(time.time()),
                owned_by="strands-agents"
            )
        )
    
    return ModelList(data=models)


@app.post("/v1/chat/completions")
async def create_chat_completion(
    request: ChatCompletionRequest, 
    authorization: Optional[str] = Header(None),
    agent_id: Optional[str] = Query(None, description="Specific agent to use (defaults to model from request)")
) -> ChatCompletionResponse:
    """
    Create a chat completion (OpenAI-compatible endpoint).

    This endpoint receives chat messages from Open Web UI and processes them
    through the specified Strands agent, returning responses in OpenAI format.

    Args:
        request: Chat completion request with messages
        authorization: Optional API key header
        agent_id: Optional agent ID to use (overrides model in request)

    Returns:
        Chat completion response with agent's reply
    """
    # Validate API key if provided (basic security)
    if authorization:
        # In production, implement proper API key validation
        pass

    # Determine which agent to use
    # Priority: agent_id query param > model from request body
    selected_agent = agent_id if agent_id else None
    
    # If model is specified and it's not alfred-butler, use it as agent_id
    if not selected_agent and request.model != "alfred-butler":
        selected_agent = request.model

    # Process through chat service
    return await chat_service.process_chat_completion(request, selected_agent)


@app.get("/v1/models/{model_id}")
async def get_model(model_id: str) -> Model:
    """
    Retrieve specific model information.

    Args:
        model_id: Model identifier

    Returns:
        Model information
    """
    # Check if it's Alfred
    if model_id == "alfred-butler":
        return Model(id=model_id, created=int(time.time()), owned_by="strands-agents")
    
    # Check if it's a specialised agent
    agent_info = AgentRegistry.get_agent_info(model_id)
    if agent_info:
        return Model(id=model_id, created=int(time.time()), owned_by="strands-agents")
    
    raise HTTPException(status_code=404, detail="Model not found")


@app.get("/v1/agents")
async def list_agents():
    """
    List all available specialised agents.
    
    Returns:
        Dictionary containing all agents organised by category
    """
    return {
        "agents": AgentRegistry.list_agents(),
        "agents_by_category": AgentRegistry.list_agents_by_category(),
        "categories": AgentRegistry.get_available_categories(),
        "total_agents": len(AgentRegistry.list_agents())
    }


@app.get("/v1/agents/{agent_id}")
async def get_agent_info(agent_id: str):
    """
    Get detailed information about a specific agent.
    
    Args:
        agent_id: The unique identifier for the agent
        
    Returns:
        Detailed agent information including tools and capabilities
    """
    agent_info = AgentRegistry.get_agent_info(agent_id)
    if not agent_info:
        raise HTTPException(
            status_code=404, 
            detail=f"Agent '{agent_id}' not found. Use /v1/agents to see available agents."
        )
    return agent_info


@app.get("/v1/agents/category/{category}")
async def get_agents_by_category(category: str):
    """
    Get all agents in a specific category.
    
    Args:
        category: The category name (utility, files, web, etc.)
        
    Returns:
        List of agents in the specified category
    """
    categorised_agents = AgentRegistry.list_agents_by_category()
    if category not in categorised_agents:
        available_categories = ", ".join(AgentRegistry.get_available_categories())
        raise HTTPException(
            status_code=404,
            detail=f"Category '{category}' not found. Available categories: {available_categories}"
        )
    
    return {
        "category": category,
        "agents": categorised_agents[category],
        "count": len(categorised_agents[category])
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
