import asyncio
from fastmcp import Client

client = Client("main.py")

async def main():
    async with client:
        result = await client.call_tool("run_query", {
            "database": "Dev Dashboard DB",
            "sql": "SELECT 1"
        })
        print(result)

asyncio.run(main())