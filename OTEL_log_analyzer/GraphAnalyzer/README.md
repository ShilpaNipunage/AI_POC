# GraphAnalyzer

This folder contains the **GraphAnalyzer** app, which analyzes the Neo4j knowledge graph generated from OpenTelemetry (OTEL) logs. It leverages [LangChain](https://python.langchain.com/) and Large Language Models (LLMs) to enable natural language querying and advanced graph analysis.

## What Does This App Do?

- Connects to the Neo4j database containing the OTEL knowledge graph.
- Uses LangChain to translate user questions into Cypher queries.
- Employs an LLM to interpret questions, generate queries, and provide insightful answers based on graph data.
- Enables users to ask complex questions about services, logs, traces, and their relationships in natural language.

## Project Setup (with [uv])

This project uses [uv] for fast Python dependency management and a `pyproject.toml` file for dependencies.

### 1. Install `uv`

If you don't have `uv` installed:
```sh
pip install uv
```

### 2. Install the Project in Editable Mode

To install the project and its dependencies, run:
```sh
uv sync
```

## Environment Variables

This project requires several environment variables to be set for configuration. You can set these in a `.env` file in the project root or export them in your shell.

```dotenv
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<password>
OPENAI_API_KEY=<your_openai_api_key>
```
### Folder & File Overview
**main.py**
Entry point. Loads environment variables, initializes Neo4j and LangChain, and starts the question-answering loop.

**graph_chain_executor.py**
Integrates LangChain with Neo4j. Handles the translation of user questions into Cypher queries using LLMs, executes those queries, and returns answers.

**neo4j_client.py**
Handles Neo4j connection and Cypher query execution.

**.env**
Stores environment variables for Neo4j and LLM access.

**README.md**
This documentation file.

## How LangChain and LLM Are Used
- **LangChain** is used to bridge the gap between natural language and graph database queries. It enables the app to:
   - Accept user questions in plain English.
   - Use an LLM (such as OpenAI GPT) to interpret the user's intent and generate the appropriate Cypher query for Neo4j.
   - Execute the Cypher query on the graph and retrieve results.
   - Use the LLM to summarize or explain the results in a user-friendly way.
- This allows users to perform advanced graph analytics and get insights from their OTEL logs without needing to know Cypher or graph database internals.

## How to Run the Application
1. Ensure Neo4j is running and populated with the OTEL knowledge graph.
2. Ensure your .env file is set up with valid credentials and API keys.
3. Run the app from this directory:

## Running the Application

To start the application, run:

```sh
python main.py
```

4. Enter your questions in natural language when prompted. The app will use LangChain and the LLM to analyze the graph and provide answers.