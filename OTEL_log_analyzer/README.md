# OTEL Log Analyzer & Graph Generator

This application parses OpenTelemetry (OTEL) JSON logs, extracts structured information, generates Cypher queries using an LLM (such as OpenAI GPT-4o-mini or Gemini), and loads the resulting graph into a Neo4j database for analysis and visualization.

## 📦 Folder Structure & Key Files
- **GraphGenerator/**  
  Main logic for transforming logs into graph structures and Cypher queries.
- **GraphAnalyzer/**  
  Contains scripts and modules for parsing OTEL logs and generating Cypher queries for Neo4j.
- **data/**  
  Place your OTEL log files here (e.g., `logs.json`).
- **README.md**  
  This documentation file.
