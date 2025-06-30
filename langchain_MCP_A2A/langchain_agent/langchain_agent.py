from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
import os

async def get_response(query : str)-> str:

    mcp_envoy_host = "localhost"#os.getenv("MCP_ENVOY_HOST", "mcp-envoy") # Default to service name
    mcp_envoy_port = os.getenv("MCP_ENVOY_PORT", "9000") # Default to internal Envoy port

    MCP_SERVER_URL = f"http://{mcp_envoy_host}:{mcp_envoy_port}/mcp/"
    # MCP_SERVER_URL = "http://127.0.0.1:8000/mcp/"
    print(f"Agent connecting to MCP server at: {MCP_SERVER_URL}")

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
            print(f"tools returned by mcp server: {tools}")

            llm = ChatOpenAI(model="gpt-4o-mini", temperature=1.0)

            agent = create_react_agent(llm, tools)

            resp = await agent.ainvoke({"messages" : [HumanMessage(content=query)]})
            final_answer = ""
            if "messages" in resp and resp["messages"]:
                # Iterate through messages in reverse to find the last AIMessage with content
                for message in reversed(resp["messages"]):
                    if isinstance(message, AIMessage) and message.content:
                        final_answer = message.content
                        break # Found the last AIMessage with content, so we can stop

            return final_answer.strip()

