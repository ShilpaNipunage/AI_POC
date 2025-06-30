from mcp.server.fastmcp import FastMCP


mcp = FastMCP ("WeatherServer")

@mcp.tool()
async def get_weather(location : str) -> str:
    """ Get weather for location """
    return "Static Weather: cloudy"


if __name__ == "__main__":
    mcp.run(transport = "streamable-http")