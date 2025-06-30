# mcp_server/Dockerfile
# Use a slim Python base image
FROM python:3.13-slim-bookworm

# Set the working directory inside the container
WORKDIR /app/mcp_server

# Set environment variable for uv
ENV UV_SYSTEM_PYTHON=false

# Install uv
RUN pip install uv

# Copy uv dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies using uv
RUN uv sync --locked

# Copy the rest of the application code
COPY . .

# Expose the port that the weather_server.py will listen on
EXPOSE 8000

# Command to run the MCP server using uvicorn
CMD ["/app/mcp_server/.venv/bin/python", "weather_custom_host_port_server.py" ] 
# "weather_server.py"]