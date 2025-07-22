# 1Password enabled MySQL MCP Server

## Requirements

- Python 3.10+
- uv
- 1Password CLI


On Mac OS:

```bash
brew install mysql@8.4 uv 1password-cli
```

## Installation

```bash
uv sync
```

Add this to your MCP Server configuration file:

```json
{
    "mcpServers": {
        "sql": {
            "command": "[PATH_TO]/uv",
            "args": [
                "--directory",
                "[CODE_PATH]",
                "run",
                "main.py"
            ],
            "env": {
                "RO_DB_ENTRIES": "Dev Auth DB",
                "RW_DB_ENTRIES": "Dev Dashboard DB"
           }
        }
    }
}
```

