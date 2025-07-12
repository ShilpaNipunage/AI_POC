from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
import os

class GraphChainExecutor:
    def __init__(self, llm):
        self.llm = llm
        self.graph = self.initialize_graph()
        self.graph_chain = self.initialize_graph_chain()
    
    def initialize_graph(self):
        NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
        NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4j_experiments")

        print(f"Connecting to Neo4j at {NEO4J_URI} with user {NEO4J_USERNAME}")
        graph = Neo4jGraph(
            url=NEO4J_URI,
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD)
        
        print(graph.schema)
        return graph

    def initialize_graph_chain(self):
        graph_chain = GraphCypherQAChain.from_llm(self.llm, graph=self.graph,
                                                allow_dangerous_requests=True,
                                                return_intermediate_steps=True,
                                                use_function_response=True,
                                                verbose=True)
        return graph_chain


    def query_graph(self, query):
        try:
            response = self.graph_chain.run(query)
            return response
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
    
    def query_graph_chain(self, query):
        try:
            print(f"Executing query: {query}")
            # Execute the query using the graph chain
            response = self.graph_chain.invoke(query)
            print(f"Query response: {response}")
            print(f"\\n\n Final response: {response['result']}")
            # Return the response from the graph chain
            return response['result']
        except Exception as e:
            print(f"Error executing query: {e}")
            raise  # Re-raise the exception to handle it in the calling code
