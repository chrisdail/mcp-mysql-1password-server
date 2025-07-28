import subprocess
import json
from typing import Dict, Any


def get_1password_item(item_name: str) -> Dict[str, Any]:
    result = subprocess.run(
        ['op', 'item', 'get', item_name, '--format=json'],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)


def get_mysql_db_args(item_name: str) -> Dict[str, Any]:
    # TODO: REMOVE THIS - Temporary for Testing
    if item_name.startswith('Prod'):
        item_name = item_name.replace('Prod', 'Dev')

    item = get_1password_item(item_name)
    fields = {field['id']: field.get('value') for field in item['fields']}

    return {
        'host': fields['hostname'],
        'user': fields['username'],
        'passwd': fields['password'],
        'db': fields['database'],
        'port': int(fields.get('port', '3306')),
        'use_unicode': True,
        'charset': 'utf8mb4',
    }
