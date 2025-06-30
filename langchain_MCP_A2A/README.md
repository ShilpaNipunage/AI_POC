# LangGraph Agent with MCP & A2A Integration
This project demonstrates a robust and scalable architecture for an intelligent agent, leveraging LangGraph for agent orchestration, OpenAI's gpt-4o-mini for reasoning, a custom Model Context Protocol (MCP) server for tool serving, and Google's Agent to Agent (A2A) protocol for client communication. Each core component (LangGraph Agent, LLM, MCP Server) is containerized with an Envoy proxy as a sidecar, enhancing inter-service communication, resilience, and observability.

## About the Project
This project addresses the challenge of building complex, modular AI agents that can interact with external tools and other agents in a distributed environment. By containerizing each component with Envoy sidecars, we achieve a highly resilient, observable, and scalable system.

## Architecture Overview
The system comprises several distinct, yet interconnected, services:

*A2A Client*: The primary interface for users to send requests to and receive responses from the LangGraph Agent.

*LangGraph Agent Service*: The brain of the operation, orchestrating interactions using the LangGraph framework. It makes decisions, utilizes the LLM for reasoning, and calls external tools via the MCP client.

*OpenAI LLM Service*: A dedicated service for accessing the gpt-4o-mini model, ensuring consistent access and potentially handling rate limiting or caching internally (though this specific project focuses on the connection to it).

*MCP Server (Tool Server) Service*: Hosts and serves external tools (e.g., get_weather_details) to the LangGraph Agent via Model Context Protocol.

*Envoy Sidecars*: Deployed alongside each Dockerized service (LangGraph Agent, OpenAI LLM, MCP Server) to manage network traffic, provide features like load balancing, circuit breaking, metrics, and distributed tracing, abstracting network concerns from the application logic.

## Getting Started
Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
* Docker & Docker Compose
* Python 3.9+
* uv
* OpenAI API Key

### Installation
Clone the repository:

```
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```
*Install project dependencies using uv:*
The subfolders a2a_client, a2a_agent, langchain_agent and mcp_server have their own uv environment. uv will automatically read pyproject.toml and uv.lock to install the correct dependencies for all Python components.

```uv sync
# Or, if you need to create a new virtual environment:
# uv venv
# source .venv/bin/activate # (or .venv\Scripts\activate for Windows)
# uv sync
```
*Configuration*
Create a .env file in the root directory of the project. This file will hold your environment variables, especially your OpenAI API key.
```
a2a_agent:
WEATHER_AGENT_HOST=localhost
WEATHER_AGENT_PORT=7001
AGENT_CARD_URL=http://localhost:7001/
```
```
langchain_agent:
OPENAI_API_kEY=<openai_key>
MCP_ENVOY_HOST=mcp-envoy
MCP_ENVOY_PORT=9000
```
```
mcp_server:
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=7000
MCP_SERVER_LOG_LEVEL=DEBUG
MCP_SERVER_JSON_RESPONSE=False
```

### Interacting with the Agent
There are 2 ways to interact with the application.
1. Docker option
2. Commandline

#### Option1: Docker option
*Ensure Docker Images are Available:*
The docker-compose.yml will handle building/pulling the necessary images. You don't typically need to build them manually unless debugging.

*Usage*
Starting the Services
All services (LangGraph Agent, LLM Proxy, MCP Server, and their Envoy sidecars) are orchestrated using Docker Compose.

*Build and run all services:*
From the root of the project, execute:

```
docker-compose up --build -d
```
--build: Ensures that your Docker images are built before starting the containers.

-d: Runs the containers in detached mode (in the background).

#### Option2: Commandline
```
#Run MCP server
cd <path>\mcp_server
#Activate uv
.venv\scripts\activate
python weather_custom_host_port_server.py
```
```
#Run a2a agent/langgraph agent
cd <path>\a2a_agent
#Activate uv
.venv\scripts\activate
python main.py
```
Once all services are running, you can interact with the LangGraph agent via the a2a_client.

### *Execute the A2A client:*
If you created a virtual environment with uv venv and activated it:
```
# Ensure your virtual environment is active: 
source .venv/bin/activate
python clients/a2a_client/run_client.py 
```
