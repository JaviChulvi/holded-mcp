from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from holded_mcp.client import HoldedClient


def register(mcp: FastMCP, client: HoldedClient) -> None:

    @mcp.tool()
    async def list_treasuries() -> Any:
        """List all treasury (bank/cash) accounts in Holded.

        Returns an array of treasury objects with: id, name, type (e.g. "bank"),
        balance, accountNumber, iban, swift, bank, bankname.
        """
        return await client.get("/treasury")

    @mcp.tool()
    async def create_treasury(data: dict[str, Any]) -> Any:
        """Create a new treasury account in Holded.

        Required fields:
        - name (string): Account name
        - type (string): Account type (e.g. "bank", "cash")

        Optional fields:
        - balance (integer): Initial balance
        - accountNumber (integer): Must match an existing accounting account number;
          if blank, a 572-prefixed account is auto-created
        - iban (string): IBAN number
        - swift (string): SWIFT/BIC code
        - bank (string): Bank identifier
        - bankname (string): Bank name

        Returns: {status: 1, info: "Created", id: "<treasury_id>"}
        """
        return await client.post("/treasury", json=data)
