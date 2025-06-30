from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
import os, json
from pydantic import BaseModel, ValidationError 
from typing import Any, Literal

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MCPClient:
    async def get_tools_from_mcp_server(self):
        mcp_envoy_host = "localhost"#os.getenv("MCP_ENVOY_HOST", "mcp-envoy") # Default to service name
        mcp_envoy_port = os.getenv("MCP_ENVOY_PORT", "9000") # Default to internal Envoy port

        # MCP_SERVER_URL = f"http://{mcp_envoy_host}:{mcp_envoy_port}/mcp/"
        MCP_SERVER_URL = "http://127.0.0.1:8000/mcp/"
        logger.info(f"Agent connecting to MCP server at: {MCP_SERVER_URL}")

        async with streamablehttp_client(MCP_SERVER_URL) as (
            read_stream, 
            write_stream,
            _,):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                # tools_mcp = await session.list_tools()
                # args = {"location" : "Pune"}
                # resp = await session.call_tool(tools_mcp.tools[0].name, arguments = args)
                # print (resp)

                #get tools
                tools = await load_mcp_tools(session)
                logger.info(f"tools returned by mcp server: {tools}")
                return tools

        logger.error("Unable to retreive tools")
        return None 


class ResponseFormat(BaseModel):
    """Respond to the user in this format."""

    status: Literal['input_required', 'completed', 'error'] = 'input_required'
    message: str

class WeatherAgent():
    """ WeatherAgent a specialized assistant for getting weather details """

    SYSTEM_INSTRUCTION = (
        'You are a specialized assistant for retreiving weather details. '
        "Your sole purpose is to use the tools provided by MCP Client to answer questions about getting weather details. "
        'If the user asks about anything other than weather details, '
        'politely state that you cannot help with that topic and can only assist with weather-related queries. '
        'Do not attempt to answer unrelated questions or use tools for other purposes.'
        'Set response status to input_required if the user needs to provide more information.'
        'Set response status to error if there is an error while processing the request.'
        'Set response status to completed if the request is complete.'
    )

    def __init__(self):
        self.agent = None
        self.mcp_session = None
        self._streamable_http_context = None
        self._read_stream = None
        self._write_stream = None

    async def __aenter__(self):
        logger.info("WeatherAgent.__aenter__ called: Starting async initialization...")
        mcp_host = os.getenv("MCP_HOST", "localhost") # Default to service name
        mcp_port = os.getenv("MCP_PORT", "8000") # Default to internal Envoy port

        MCP_SERVER_URL = f"http://{mcp_host}:{mcp_port}/mcp/"
        logger.info(f"Agent connecting to MCP server at: {MCP_SERVER_URL}")

        self._streamable_http_context = streamablehttp_client(MCP_SERVER_URL)
        self._read_stream, self._write_stream, _ = await self._streamable_http_context.__aenter__()
        self.mcp_session = ClientSession(self._read_stream, self._write_stream)
        await self.mcp_session.__aenter__()

        await self.mcp_session.initialize()
                
        #get tools
        tools = await load_mcp_tools(self.mcp_session)
        logger.info(f"tools returned by mcp server: {tools}")
        
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=1.0)

        logger.info("Create react agent")
        self.agent = create_react_agent(llm, 
                                    tools, 
                                    prompt=self.SYSTEM_INSTRUCTION,
                                    response_format=ResponseFormat)
        
        logger.info("WeatherAgent.create() completed: Instance is fully initialized.")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the asynchronous context for WeatherAgent.
        This method ensures the MCP ClientSession and its streams are properly closed.
        """
        logger.info("WeatherAgent.__aexit__ called: Closing MCP session and streams...")
        if self.mcp_session:
            await self.mcp_session.__aexit__(exc_type, exc_val, exc_tb) # Close the MCP session
        if self._streamable_http_context:
            await self._streamable_http_context.__aexit__(exc_type, exc_val, exc_tb) # Close the HTTP streams

        logger.info("MCP session and streams closed.")
        
    async def invoke(self, query, context_id):
        if not self.agent:
            raise RuntimeError("WeatherAgent not initialized. Please use 'async with WeatherAgent()'.")


        config = {'configurable': {'thread_id': context_id}}
        res = await self.agent.ainvoke({'messages': [('user', query)]}, config)
        logger.info(f"\n\n!!!res: {res}")
        return self.get_agent_response(res)
        
    def get_agent_response(self, final_state: dict):
        """Parses the agent's final state into the desired ResponseFormat."""
        try:
            structured_response = final_state.get('structured_response')
            logger.info(f"st_resp:{structured_response}")
            if structured_response and isinstance(
                structured_response, ResponseFormat
            ):
                logger.info(f"structured_response is of type ResponseFormat")
            # Attempt to parse the content of the last AIMessage as ResponseFormat
            # The LLM should generate JSON that matches ResponseFormat due to response_format
            if structured_response.status == 'input_required':
                return {
                    'is_task_complete': False,
                    'require_user_input': True,
                    'content': structured_response.message,
                }
            elif structured_response.status == 'error':
                return {
                    'is_task_complete': False,
                    'require_user_input': True,
                    'content': structured_response.message,
                }
            elif structured_response.status == 'completed':
                return {
                    'is_task_complete': True,
                    'require_user_input': False,
                    'content': structured_response.message,
                }
        except (json.JSONDecodeError, ValidationError) as e:
            logger.error(f"ERROR: Failed to parse agent response into ResponseFormat: {e}")
            # Fallback if parsing fails or LLM didn't return valid JSON
            return {
                'is_task_complete': False,
                'require_user_input': True,
                'content': (
                    f"An internal error occurred while processing the response. "
                    f"Please check the agent's output format. Error: {e}. Raw: {last_ai_message.content}"
                ),
            }
        
        # Fallback if no valid structured_response found or no final AI message
        return {
            'is_task_complete': False,
            'require_user_input': True,
            'content': (
                'We are unable to process your request at the moment. '
                'Please try again.'
            ),
        }
    # def get_agent_response(self, config):
    #     print(f"\n\nconfig: {config}")
    #     current_state = self.agent.get_state(config)
    #     print(f"\n\ncurrent_state:{current_state}")
    #     structured_response = current_state.values.get('structured_response')
    #     if structured_response and isinstance(
    #         structured_response, ResponseFormat
    #     ):
    #         if structured_response.status == 'input_required':
    #             return {
    #                 'is_task_complete': False,
    #                 'require_user_input': True,
    #                 'content': structured_response.message,
    #             }
    #         if structured_response.status == 'error':
    #             return {
    #                 'is_task_complete': False,
    #                 'require_user_input': True,
    #                 'content': structured_response.message,
    #             }
    #         if structured_response.status == 'completed':
    #             return {
    #                 'is_task_complete': True,
    #                 'require_user_input': False,
    #                 'content': structured_response.message,
    #             }

    #     return {
    #         'is_task_complete': False,
    #         'require_user_input': True,
    #         'content': (
    #             'We are unable to process your request at the moment. '
    #             'Please try again.'
    #         ),
    #     }
    
    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']

