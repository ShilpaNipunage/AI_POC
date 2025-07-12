# GraphGenerator

This folder contains the **GraphGenerator** app, which parses OpenTelemetry (OTEL) logs and constructs a knowledge graph in Neo4j using generated Cypher queries.

## What is Neo4j?

[Neo4j](https://neo4j.com/) is a popular graph database that stores data as nodes, relationships, and properties, making it ideal for representing complex, interconnected data. In this project, Neo4j is used to build a knowledge graph from OTEL logs, allowing for advanced querying and visualization of relationships between services, traces, and log events.

## Data Model

The code generates a knowledge graph with the following data model:

- **Nodes**:
  - `Service`: Represents a service. Properties include `service_name`, `service_instance_id`, `version` and other OTEL resource attributes.
  - `Scope`: Represents a scope associated with a log record. Properties include 'scope_name'.
  - `Operation`: Represents an individual operation executed as part of the scope. Properties `body`.
  - `Trace` : Represents Trace id
  - `Span` : Represents span id 

- **Relationships**:
  - `(:Service)-[:HAS_SCOPE]->(:Scope)`: Connects a service to its scope.
  - `(:Trace)-[:IN_TRACE]->(:Scope)`: Connects a scope to the trace.
  - `(:Trace)-[:HAS_SERVICE]->(:Service)`: Connects a trace to a service.
  - `(:Scope)-[:MADE_OPERATION]->(:Operation)`: Refers to the operation performed in the scope.

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
To activate uv environment, run (windows):
```sh
.\.venv\Scripts\activate
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
