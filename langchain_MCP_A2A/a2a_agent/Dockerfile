# mcp_server/Dockerfile
# Use a slim Python base image
FROM python:3.13-slim-bookworm

# Set the working directory inside the container
WORKDIR /app/a2a_agent

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

# Expose the port that the WeatherAgent.py will listen on
EXPOSE 9000

# Command to run the MCP server using uvicorn
CMD ["/app/a2a_agent/.venv/bin/python", "main.py" ]