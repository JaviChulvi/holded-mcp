# Holded MCP Server

An open-source [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server for the [Holded](https://www.holded.com) API. Connect any MCP-compatible AI assistant to your Holded account and manage invoicing, CRM, projects, team, and accounting through natural language.

Built with Python, [FastMCP](https://github.com/jlowin/fastmcp), and [httpx](https://www.python-httpx.org/).

## Features

- **Invoicing** — Create and manage invoices, estimates, sales orders, credit notes, receipts, proformas, and purchase documents.
- **Contacts** — Full CRUD for clients, suppliers, leads, debtors, and creditors.
- **Products** — Manage your product catalog, pricing, stock levels across warehouses.
- **CRM** — Work with sales funnels, leads/deals, and activities.
- **Projects** — Create projects, tasks, and track time.
- **Team / HR** — Manage employees, clock in/out, and attendance records.
- **Accounting** — Access the chart of accounts and daily ledger entries.
- **Treasury** — List and create bank/cash accounts.

## Setup

### Prerequisites

- Python 3.10+
- A [Holded](https://www.holded.com) account with an [API key (Settings &gt; API)](https://app.holded.com/account/setup#settings:/api)

### Installation

```bash
pip install -e .

# Set your Holded API key
export HOLDED_API_KEY=your_api_key_here
```

## Configuration

### `HOLDED_API_KEY` (required)

Your Holded API key. You can find it in Holded under **Settings > API**.

### `HOLDED_ALLOWED_METHODS` (optional)

Controls which HTTP methods the server is permitted to use. This acts as a safety mechanism to prevent unintended write or delete operations.

| Value                   | Behavior                                             |
| ----------------------- | ---------------------------------------------------- |
| `ALL` (default)       | All methods allowed — full read/write/delete access |
| `GET`                 | Read-only mode — only list and get operations work  |
| `GET,POST`            | Read + create — no updates or deletions             |
| `GET,POST,PUT`        | Read, create, and update — no deletions             |
| `GET,POST,PUT,DELETE` | Same as `ALL` — explicit full access              |

Examples:

```bash
# Read-only mode (safe for exploration)
export HOLDED_ALLOWED_METHODS=GET

# Allow reads and creating new records
export HOLDED_ALLOWED_METHODS=GET,POST

# Full access (default)
export HOLDED_ALLOWED_METHODS=ALL
```

> **Tip:** Start with `GET` to safely explore your data, then expand permissions as needed.

## Usage

### Claude Code

```bash
claude mcp add holded -- python -m holded_mcp.server
```

Or add to `.claude/settings.json`:

```json
{
  "mcpServers": {
    "holded": {
      "command": "python",
      "args": ["-m", "holded_mcp.server"],
      "env": {
        "HOLDED_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Cursor

Add to your Cursor MCP configuration (`.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "holded": {
      "command": "python",
      "args": ["-m", "holded_mcp.server"],
      "env": {
        "HOLDED_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Windsurf

Add to your Windsurf MCP configuration (`~/.windsurf/mcp.json`):

```json
{
  "mcpServers": {
    "holded": {
      "command": "python",
      "args": ["-m", "holded_mcp.server"],
      "env": {
        "HOLDED_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### VS Code (Copilot)

Add to your VS Code settings (`.vscode/mcp.json`):

```json
{
  "servers": {
    "holded": {
      "command": "python",
      "args": ["-m", "holded_mcp.server"],
      "env": {
        "HOLDED_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Any MCP-Compatible Client

The server uses **stdio transport** by default. Run it with any MCP client that supports stdio:

```bash
python -m holded_mcp.server
```

Or use the installed entry point:

```bash
holded-mcp
```

## Available Tools

### Contacts

`list_contacts`, `get_contact`, `create_contact`, `update_contact`, `delete_contact`

### Documents

`list_documents`, `get_document`, `create_document`, `update_document`, `delete_document`, `pay_document`, `send_document`, `get_document_pdf`

Document types: `invoice`, `salesreceipt`, `creditnote`, `estimate`, `salesorder`, `waybill`, `proform`, `purchase`, `purchaserefund`, `purchaseorder`

### Products

`list_products`, `get_product`, `create_product`, `update_product`, `delete_product`, `update_stock`

### Treasury

`list_treasuries`, `create_treasury`

### CRM

`list_funnels`, `list_leads`, `get_lead`, `create_lead`, `update_lead`, `delete_lead`, `list_events`, `create_event`

### Projects

`list_projects`, `get_project`, `create_project`, `update_project`, `delete_project`, `list_tasks`, `create_task`, `update_task`, `list_time_records`, `create_time_record`

### Team

`list_employees`, `get_employee`, `create_employee`, `update_employee`, `clock_in`, `clock_out`, `list_time_entries`

### Accounting

`list_daily_ledger`, `create_ledger_entry`, `list_accounts`, `get_account`, `create_account`

## Use Cases

- **Automate invoicing** — Ask your AI assistant to create invoices, send them to clients, and track payments.
- **CRM management** — Manage your sales pipeline, create leads, and log activities without leaving your editor.
- **Project tracking** — Create projects and tasks, log time, and monitor progress through conversation.
- **HR operations** — Manage employees, track attendance, and handle clock in/out.
- **Financial overview** — Query your chart of accounts, review ledger entries, and manage treasury accounts.
- **Bulk operations** — Use AI to process multiple records, generate reports, or migrate data.

## Architecture

The server follows a modular architecture:

- **Entry point** (`server.py`) — Creates the FastMCP instance and registers all tool modules.
- **API client** (`client.py`) — Async HTTP client with auth, method restrictions, and pagination support.
- **Tool modules** (`tools/*.py`) — Each module exports a `register(mcp, client)` function. Modules are purely functional with no cross-dependencies.

## Author

Built by [Javier Chulvi](https://www.linkedin.com/in/javier-chulvi-bernad/).

## License

MIT
