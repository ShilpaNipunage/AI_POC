from dotenv import load_dotenv
import asyncio
from langchain_agent import get_response

async def main():
    print("Hello from agent!")

    load_dotenv()

    print(await get_response("Hows weather in Pune?"))


if __name__ == "__main__":
    asyncio.run(main())
