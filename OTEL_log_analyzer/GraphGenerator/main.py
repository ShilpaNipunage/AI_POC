# main.py
import json
from GraphGenerator.log_parser_cypher_gen import read_logs_from_file, process_resource_log_data
from neo4j_client import Neo4jClient
from dotenv import load_dotenv
import os


def main():
    log_file_path = "..\\data\\mini_log.json" # Path to your log file

    load_dotenv(override=True)  # Load environment variables from .env file

    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4j_experiments")

    # Initialize Neo4j Client
    neo4j_client = Neo4jClient(uri = NEO4J_URI, user=NEO4J_USERNAME, password=NEO4J_PASSWORD)

    # Ensure Neo4j is connected before proceeding
    if not neo4j_client._driver:
        print("Exiting due to Neo4j connection failure.")
        return
    

    neo4j_client.run_cypher("MATCH (n) DETACH DELETE n")
    print("Cleared existing database.")

    print(f"Starting Knowledge Graph construction from {log_file_path}...")

    processed_records_count = 0
    # read_logs_from_file now yields each complete { "resourceLogs": [...] } JSON object from the file.
    for otel_log_export_unit in read_logs_from_file(log_file_path):
        # print(f"\n\notel_log_export_unit:{otel_log_export_unit}")
        # break
        # process_resource_log_data takes one such unit and extracts all individual log records from it.
        cypher_query_list = process_resource_log_data(otel_log_export_unit)
        
        print("****** No of Cypher queries generated:", len(cypher_query_list))
        for cypher_query in cypher_query_list:
            try:
                print(f"\nExecuting Cypher:\n{cypher_query}") # Uncomment to see generated Cypher
                result = neo4j_client.run_cypher(cypher_query)
                # if(result == []):
                #     break

                processed_records_count += 1
                if processed_records_count % 10 == 0:
                    print(f"Processed {processed_records_count} individual log records...")
            except Exception as e:
                print(f"Error executing Cypher query: {e}")
                break
        
    print(f"\nFinished processing {processed_records_count} individual log records.")
    print("Knowledge Graph construction complete.")

    # Close Neo4j connection
    neo4j_client.close()

if __name__ == "__main__":
    main()