# neo4j_client.py
from neo4j import GraphDatabase, Driver
from typing import List, Dict, Any

class Neo4jClient:
    def __init__(self, uri, user, password):
        self._uri = uri
        self._user = user
        self._password = password
        self._driver: Optional[Driver] = None
        self._connect()

    def _connect(self):
        """Establishes connection to Neo4j."""
        try:
            print(f"Connecting to Neo4j at {self._uri} with user '{self._user}'...")
            self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))
            self._driver.verify_connectivity()
            print("Neo4j connection established successfully.")
        except Exception as e:
            print(f"Error connecting to Neo4j: {e}")
            self._driver = None # Ensure driver is None on failure

    def run_cypher(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Executes a single Cypher query.
        Returns a list of records, where each record is a dictionary.
        """
        if not self._driver:
            print("No active Neo4j connection. Attempting to reconnect...")
            self._connect()
            if not self._driver:
                print("Failed to reconnect to Neo4j. Skipping query.")
                return []

        with self._driver.session() as session:
            try:
                result = session.run(query, parameters)
                return [record.data() for record in result]
            except Exception as e:
                print(f"Error executing Cypher query:\n{query}\nError: {e}")
                raise  # Re-raise the exception to handle it in the calling code
                # return []

    def close(self):
        """Closes the Neo4j driver."""
        if self._driver:
            self._driver.close()
            print("Neo4j connection closed.")