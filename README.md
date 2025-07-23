# 1Password-enabled MySQL MCP Server

A Model Context Protocol (MCP) server that provides secure MySQL database access using credentials stored in 1Password. This server allows AI assistants and other MCP clients to query MySQL databases while maintaining security best practices by keeping database credentials in 1Password rather than in configuration files.

## Requirements

- Python 3.10+
- uv (Python package manager)
- 1Password CLI
- MySQL server access

## Installation

### MacOS

```bash
# Install dependencies
brew install uv 1password-cli

# Install Python dependencies
uv sync
```

### Other Platforms

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install 1Password CLI
# Visit: https://developer.1password.com/docs/cli/get-started/

# Install Python dependencies
uv sync
```

## Setup

### 1. 1Password Configuration

Create database items in 1Password with the following fields:
- `hostname`: MySQL server hostname
- `username`: MySQL username
- `password`: MySQL password
- `database`: Database name
- `port`: MySQL port (optional, defaults to 3306)

### 2. Environment Configuration

Configure the following environment variables:

- `RO_DB_ENTRIES`: Comma-separated list of 1Password item names for read-only databases
- `RW_DB_ENTRIES`: Comma-separated list of 1Password item names for read-write databases

### 3. MCP Server Configuration

Add this to your MCP Server configuration file:

```json
{
    "mcpServers": {
        "mysql": {
            "command": "[PATH_TO]/uv",
            "args": [
                "--directory",
                "[CODE_PATH]",
                "run",
                "main.py"
            ],
            "env": {
                "RO_DB_ENTRIES": "Dev Auth DB,Production Analytics DB",
                "RW_DB_ENTRIES": "Dev Dashboard DB,Staging DB"
            }
        }
    }
}
```

Replace `[PATH_TO]/uv` with the actual path to your uv installation and `[CODE_PATH]` with the path to this project directory.
