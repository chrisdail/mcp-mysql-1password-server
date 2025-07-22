from typing import Any, Dict, List
import os

from mcp_server import mcp

import mysql_tools
import onepssword


RO_DB_ENTRIES = os.getenv('RO_DB_ENTRIES', '').split(',') or []
RW_DB_ENTRIES = os.getenv('RW_DB_ENTRIES', '').split(',') or []


@mcp.tool()
def available_databases() -> Dict[str, List[str]]:
    return {
        'read_only_databases': RO_DB_ENTRIES,
        'read_write_databases': RW_DB_ENTRIES,
    }


if __name__ == '__main__':
    print('Starting MCP Server')
    mcp.run()
