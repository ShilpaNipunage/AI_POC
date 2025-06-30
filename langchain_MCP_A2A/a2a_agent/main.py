import os, logging
import uvicorn
from a2a.types import (
    AgentSkill,
    AgentCard,
    AgentCapabilities,
)

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore

from agent_executor import WeatherAgentExecutor
import asyncio, click

from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


load_dotenv()

@click.command(context_settings={"auto_envvar_prefix": "WEATHER_AGENT"}) 
@click.option("--host", default = "127.0.0.1", help="Host to host the service")
@click.option("--port", default=9999, help="Port to listen on for HTTP")
@click.option(
    "--log-level",
    default="INFO",
    help="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
)
def main(
    host : str,
    port: int,
    log_level: str,
    ):

  
    
    skill = AgentSkill(
        id = 'weather_details_retriever',
        name = "Returns weather details",
        description= "This agent retruns weather details for user specified location",
        tags = ["weather, weather details"],
        examples= ["How is weather in Pune?"],
    )

    agent_card_url = str(os.getenv("AGENT_CARD_URL"))
    
    print(f"Retreive agent card from : {agent_card_url}")

    public_agent_card = AgentCard(
        name="Weather Agent",
        description="This agent retruns weather details for user specified location.",
        url=agent_card_url,
        version="1.0.0",
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
        defaultInputModes=['text'],
        defaultOutputModes=["text"],
        supportsAuthenticatedExtendedCard=False
    )

    request_handler = DefaultRequestHandler(
        agent_executor=WeatherAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server_app = A2AStarletteApplication(
        agent_card=public_agent_card,
        http_handler=request_handler,
        )
    
    uvicorn.run(server_app.build(), host = host, port = port)

    # --- IMPORTANT CHANGE HERE ---
    # Configure Uvicorn without calling uvicorn.run() directly
    # config = uvicorn.Config(
    #     app=server_app.build(), # Pass the ASGI application built by a2a
    #     host="0.0.0.0",
    #     port=9999,
    #     log_level="info", # Optional: Set log level
    #     loop="asyncio", # Explicitly use asyncio loop (default, but good to be clear)
    #     # Add reload=True if you want auto-reloading during development
    #     # reload=True,
    # )
    
    # # Create a Uvicorn server instance
    # server = uvicorn.Server(config)
    
    # print(f"Starting Uvicorn server on {config.host}:{config.port}...")
    # # Await the server.serve() method to run it within the existing event loop
    # await server.serve()
    # print("Uvicorn server stopped.") # This line will only be reached if the server is shut down


if __name__ == "__main__":
    main()