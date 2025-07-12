# GraphGenerator

This folder contains the **GraphGenerator** app, which parses OpenTelemetry (OTEL) logs and constructs a knowledge graph in Neo4j using generated Cypher queries.

## What is Neo4j?

[Neo4j](https://neo4j.com/) is a popular graph database that stores data as nodes, relationships, and properties, making it ideal for representing complex, interconnected data. In this project, Neo4j is used to build a knowledge graph from OTEL logs, allowing for advanced querying and visualization of relationships between services, traces, and log events.

## Data Model

The code generates a knowledge graph with the following data model:

- **Nodes**:
  - `Service`: Represents a microservice or application component. Properties include `service_name`, `service_namespace`, and other OTEL resource attributes.
  - `Resource`: Represents a resource associated with a log record. Properties may include `resource_attributes` as key-value pairs.
  - `LogRecord`: Represents an individual log entry. Properties include `timestamp`, `severity_text`, `severity_number`, `trace_id`, `span_id`, `body`, and additional OTEL log attributes.

- **Relationships**:
  - `(:Service)-[:HAS_RESOURCE]->(:Resource)`: Connects a service to its resource.
  - `(:Resource)-[:GENERATED]->(:LogRecord)`: Connects a resource to the log records it generated.
  - `(:Service)-[:GENERATED]->(:LogRecord)`: (In some cases) Directly connects a service to its log records.
  - `(:LogRecord)-[:RELATED_TO]->(:LogRecord)`: (Optional) Connects related log records, e.g., by trace or span relationships.

- **Properties**:
  - Each node and relationship can have properties such as `service_name`, `resource attributes`, `timestamp`, `severity_text`, `trace_id`, `span_id`, and `body`, depending on the OTEL log structure.

This model enables you to query for patterns, dependencies, and flows within your distributed system logs, such as which services generated which logs, how logs are related by traces, and the attributes of each log.

## Project Setup (with [uv])

This project uses [uv] for fast Python dependency management and uses a `pyproject.toml` file to specify dependencies.

### 1. Install `uv`

If you don't have `uv` installed:
```sh
pip install uv
```

### 2. Install dependencies

From this folder, run:
```sh
uv sync
```

### 3. Set up environment variables

Create a `.env` file in this folder with the following contents (edit as needed):
```
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=<user_name>
NEO4J_PASSWORD=<password>
```

## How to Run the Application

1. Ensure Neo4j is running and accessible with the credentials in your `.env` file.
2. Place your OTEL log file at `../data/logs.json` or update the path in `main.py`.
3. Run the app from this directory:
```sh
python main.py
```

The script will clear the Neo4j database, parse the log file, and populate the knowledge graph.