from mcp.server.fastmcp import FastMCP

from holded_mcp.client import HoldedClient
from holded_mcp.tools import contacts, documents, products, treasury, crm, projects, team, accounting

mcp = FastMCP("Holded")
client = HoldedClient()

# Register all tool modules
for mod in [contacts, documents, products, treasury, crm, projects, team, accounting]:
    mod.register(mcp, client)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
