from typing import Any, Dict
import MySQLdb
from fastmcp.server.context import Context
from fastmcp.utilities.logging import get_logger
from fastmcp.exceptions import ToolError
from mcp_server import mcp
import onepssword

logger = get_logger(__name__)


def is_safe_query(sql: str) -> bool:
    """Basic check for potentially unsafe queries"""
    sql_lower = sql.lower()
    unsafe_keywords = ["insert", "update", "delete", "drop", "alter", "truncate", "create"]
    return not any(keyword in sql_lower for keyword in unsafe_keywords)


@mcp.tool()
def run_query(database: str, sql: str, ctx: Context) -> Dict[str, Any]:
    logger.info(f'Connecting to database: {database}')
    db_args = onepssword.get_mysql_db_args(database)
    conn = MySQLdb.connect(**db_args)

    if not is_safe_query(sql):
        raise ToolError('Only SELECT queries are allowed')

    logger.info(f'Running query: {sql}')

    cursor = None
    try:
        # Create dictionary cursor
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        # Start read-only transaction
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
