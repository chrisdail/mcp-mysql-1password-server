import asyncio
import argparse
from fastmcp import Client

def parse_args():
    parser = argparse.ArgumentParser(description='Test MCP MySQL 1Password client')
    parser.add_argument('--database', '-d',
                       default='Dev Dashboard DB',
                       help='Database name to query (default: Dev Dashboard DB)')
    parser.add_argument('--sql', '-s',
                       default='SELECT 1',
                       help='SQL query to execute (default: SELECT 1)')
    return parser.parse_args()

client = Client("main.py")

async def main():
    args = parse_args()

    async with client:
        result = await client.call_tool("sql_query", {
            "database": args.database,
            "sql": args.sql
        })
        print(result)

asyncio.run(main())
