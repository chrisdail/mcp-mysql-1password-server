from typing import Any, Dict
import os
import pymysql
from fastmcp.utilities.logging import get_logger
from fastmcp.exceptions import ToolError
from mcp_server import mcp
import onepssword

RO_DB_ENTRIES = os.getenv('RO_DB_ENTRIES', '').split(',')
RW_DB_ENTRIES = os.getenv('RW_DB_ENTRIES', '').split(',')

logger = get_logger(__name__)


def is_safe_query(sql: str) -> bool:
    """Check for potentially unsafe queries"""
    sql_lower = sql.lower()
    unsafe_keywords = ['insert', 'update', 'delete', 'drop', 'alter', 'truncate', 'create']
    return not any(keyword in sql_lower for keyword in unsafe_keywords)


def is_read_only_database(database: str) -> bool:
    """Check if the database is in the read-only list"""
    return database in RO_DB_ENTRIES


@mcp.tool()
def run_query(database: str, sql: str) -> Dict[str, Any]:
    if not is_safe_query(sql) and is_read_only_database(database):
        raise ToolError('Only SELECT queries are allowed for read-only databases')


    logger.info(f'Looking up details for database: {database}')
    db_args = onepssword.get_mysql_db_args(database)
    logger.info(f'Connecting to database: {db_args["host"]}')
    conn = pymysql.connect(**db_args)

    logger.info(f'Running query: {sql}')
    cursor = None
    try:
        # Create dictionary cursor
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        if is_read_only_database(database):
            cursor.execute('SET TRANSACTION READ ONLY')

        cursor.execute('START TRANSACTION')
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            conn.commit()
            return {'results': results}
        except Exception as e:
            conn.rollback()
            logger.info(f'Error running query: {e}')
            raise e
    finally:
        if cursor:
            cursor.close()
        conn.close()
