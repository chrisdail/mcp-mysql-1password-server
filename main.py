from typing import Any, Dict, List
import os

from mcp_server import mcp

import mysql_tools
import onepssword


DB_ENTRIES = os.getenv("DB_ENTRIES", "").split(",")

@mcp.tool()
def available_databases() -> list[str]:
    return DB_ENTRIES


if __name__ == "__main__":

    required_env_vars = ["DB_ENTRIES"]
    missing = [var for var in required_env_vars if not os.getenv(var)]
    if missing:
        print(f"Environment variables are missing: {', '.join(missing)}")

    print("Starting MCP Server")
    mcp.run()
