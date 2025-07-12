from dotenv import load_dotenv
from pprint import pprint

load_dotenv(override=True)

# from GraphChainExecutor import GraphChainExecutor
from langchain_openai import ChatOpenAI
from graph_query_agent import GraphQueryAgent


def main():
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    # g_executor = GraphChainExecutor(llm)

    g_executor = GraphQueryAgent(llm)

    # query = "Which services are present in the graph?"
    # query = "Which operations langchain-mcp-a2a-weather-server: mcp-server service is executing in the graph?"
    # query = "To which other services 'langchain-mcp-a2a-weather-server: a2a-agent' service is connecting to in the graph. What are the types of those services?"
    query = "Analyze all the services from the graph, find their scope and operations and indentify what types of services are present, their frameoworks and what kind of operations they are trying to make."
    
    # print(f"\n\nQuery:{query}\nResponse:{g_executor.query_graph_chain(query)}")
    response = g_executor.run(query)
    last_message = response['messages'][-1]
    if hasattr(last_message, "content"):
        print(f"\n\nQuery:{query}\nResponse_contents:")
        pprint(last_message.content)
    else:
        # If the content is not in the last message, print the entire response
        print(f"\n\nQuery:{query}\nResponse_last_msg:")
        pprint(last_message)
    

if __name__ == "__main__":
    main()
