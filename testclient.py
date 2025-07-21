import asyncio
from fastmcp import Client

client = Client("main.py")

async def main():
    async with client:
        result = await client.call_tool("run_query", {
            "database": "Dev Dashboard DB",
            "sql": "SELECT * FROM report WHERE id IN (46527, 46528, 46529, 46530, 46531, 46532, 46533, 46534, 46535)"
        })
        print(result)

asyncio.run(main())