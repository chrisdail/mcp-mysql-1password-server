from typing import Any, Dict, List
import os
import pymysql
from fastmcp.utilities.logging import get_logger
from fastmcp.exceptions import ToolError
from mcp_server import mcp
import onepssword


RO_DB_ENTRIES = [name.strip() for name in os.getenv('RO_DB_ENTRIES', '').split(',')]
RW_DB_ENTRIES = [name.strip() for name in os.getenv('RW_DB_ENTRIES', '').split(',')]

logger = get_logger(__name__)


def is_safe_query(sql: str) -> bool:
    """Check for potentially unsafe queries"""
    unsafe_keywords = ['INSERT ', 'UPDATE ', 'DELETE ', 'DROP ', 'ALTER ', 'TRUNCATE ', 'CREATE ', 'SET ']
    return not any(keyword in sql.upper() for keyword in unsafe_keywords)


def is_read_only_database(database: str) -> bool:
    """Check if the database is in the read-only list"""
    return database in RO_DB_ENTRIES


@mcp.tool()
def available_databases() -> Dict[str, List[str]]:
    """
    Returns the available databases and if they are read-only or read-write.
    These are suitable for use in the `database` parameter of the `run_query` tool.
    """
    return {
        'read_only_databases': RO_DB_ENTRIES,
        'read_write_databases': RW_DB_ENTRIES,
    }


@mcp.tool()
def sql_query(database: str, sql: str) -> Dict[str, Any]:
    """
    Executes a SQL query on the specified database.
    The `database` parameter should be one of the ones returned by the `available_databases` tool.
    The `sql` parameter should be a valid SQL query. Add LIMIT 100 to SELECT queries intended to return multipls rows.
    """

    if not is_safe_query(sql) and is_read_only_database(database):
        raise ToolError('Only SELECT queries are allowed for read-only databases')

    logger.info(f'Looking up details for database: {database}')
    db_args = onepssword.get_mysql_db_args(database)

    logger.info(f'Connecting to database: {db_args["host"]}')
    conn = pymysql.connect(**db_args)

    logger.info(f'Running query: {sql}')
    cursor = None
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        if is_read_only_database(database):
            cursor.execute('SET TRANSACTION READ ONLY')

        cursor.execute('START TRANSACTION')
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
