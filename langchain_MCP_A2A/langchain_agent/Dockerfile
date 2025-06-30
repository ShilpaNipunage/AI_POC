# agent/Dockerfile
# Use a slim Python base image for smaller size
FROM python:3.13-slim-bookworm

# Set the working directory inside the container
WORKDIR /app/agent

# Set environment variable for uv to not use system Python
ENV UV_SYSTEM_PYTHON=false

# Install uv
RUN pip install uv

# Copy uv dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies using uv
# --locked ensures deterministic installs based on uv.lock
RUN uv sync --locked

# Copy the rest of the application code
COPY . .

# Expose a port if the agent were to serve an API, otherwise it's just a client.
# No EXPOSE needed for a client-only app, but including it for conceptual completeness if it were a server.
# EXPOSE 8080 # Example if agent itself served an API

# Command to run the agent application
# We use main.py which calls get_response from langchain_agent.py
CMD ["python", "main.py"]