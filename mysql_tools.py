from typing import Any, Dict
import os
import MySQLdb
from fastmcp.server.context import Context
from fastmcp.utilities.logging import get_logger
from fastmcp.exceptions import ToolError
from mcp_server import mcp
import onepssword

READ_ONLY = os.getenv("READ_ONLY", "false").lower() == "true"

logger = get_logger(__name__)


def is_safe_query(sql: str) -> bool:
    """Basic check for potentially unsafe queries"""
    sql_lower = sql.lower()
    unsafe_keywords = ["insert", "update", "delete", "drop", "alter", "truncate", "create"]
    return not any(keyword in sql_lower for keyword in unsafe_keywords)


@mcp.tool()
def run_query(database: str, sql: str) -> Dict[str, Any]:
    if not is_safe_query(sql) and READ_ONLY:
        raise ToolError('Only SELECT queries are allowed in read-only mode')


    logger.info(f'Looking up details for database: {database}')
    db_args = onepssword.get_mysql_db_args(database)
    logger.info(f'Connecting to database: {db_args["host"]}')
    conn = MySQLdb.connect(**db_args)

    logger.info(f'Running query: {sql}')
    cursor = None
    try:
        # Create dictionary cursor
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        if READ_ONLY:
            cursor.execute("SET TRANSACTION READ ONLY")

        cursor.execute("START TRANSACTION")
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            conn.commit()
            return {"results": results}
        except Exception as e:
            conn.rollback()
            logger.info(f'Error running query: {e}')
            raise e
    finally:
        if cursor:
            cursor.close()
        conn.close()
