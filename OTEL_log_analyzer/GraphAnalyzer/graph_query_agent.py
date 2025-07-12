from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from graph_chain_executor import GraphChainExecutor

# class GraphChainTool():
#     """
#     A tool that extends GraphChainExecutor to provide a method for querying the graph database.
    
#     Args:
#         llm: The language model to use for generating responses.
#     """
#     def __init__(self, llm):
#         self.g_executor = GraphChainExecutor(llm)

#     @tool
#     def query_graph(self, query: str) -> str:
#         """
#         Query the graph database with the provided Cypher query.
        
#         Args:
#             query (str): The Cypher query to execute on the graph database.
            
#         Returns:
#             str: The result of the query execution.
#         """

#         response = self.g_executor.query_graph_chain(query)
#         return response['result'] if 'result' in response else str(response)


llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
g_executor = GraphChainExecutor(llm)

@tool
def query_graph(query: str) -> str:
        """
        Query the graph database with the provided Cypher query.
        
        Args:
            query (str): The Cypher query to execute on the graph database.
            
        Returns:
            str: The result of the query execution.
        """
        
        response = g_executor.query_graph_chain(query)
        return response['result'] if 'result' in response else str(response)

class GraphQueryAgent():
    """
    A class that creates a graph query agent using the prebuilt React agent.
    
    This agent can be used to query a graph database using Cypher queries.
    """

    def __init__(self, llm):
        # self.llm = llm
        # g_executor = GraphChainExecutor(llm)

        self.agent = create_graph_query_agent()

    

    def run(self, query: str) -> str:
        """
        Run the graph query agent with the provided query.
        
        Args:
            query (str): The Cypher query to execute.
            
        Returns:
            str: The response from the graph query agent.
        """
        return self.agent.invoke({'messages': [('user', query)]})

        
    
def create_graph_query_agent():
    """
    Create a graph query agent using the prebuilt React agent.
    
    Returns:
        Agent: The graph query agent.
    """

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
    # gc_tool = GraphChainTool(llm=llm)

    # @tool
    # def query_graph(self, query: str) -> str:
    #     """
    #     Query the graph database with the provided Cypher query.
        
    #     Args:
    #         query (str): The Cypher query to execute on the graph database.
            
    #     Returns:
    #         str: The result of the query execution.
    #     """
    #     # llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
    #     # g_executor = GraphChainExecutor(llm)
    #     response = self.g_executor.query_graph_chain(query)
    #     return response['result'] if 'result' in response else str(response)

    return create_react_agent(
        model="gpt-4o-mini",
        tools=[query_graph], #[query_graph],
        prompt="You are a helpful assistant that can query a graph database using Cypher queries."
        )