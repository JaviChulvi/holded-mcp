from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from holded_mcp.client import HoldedClient


def register(mcp: FastMCP, client: HoldedClient) -> None:

    @mcp.tool()
    async def list_daily_ledger(page: int = 1, starttmp: int | None = None, endtmp: int | None = None) -> Any:
        """List daily ledger entries (paginated, max 500 per page).

        Optional filters:
        - starttmp: Start date as Unix timestamp
        - endtmp: End date as Unix timestamp

        Returns an array of ledger entries with date, description, account details,
        debit/credit amounts, and associated documents.
        """
        params: dict[str, Any] = {"page": page}
        if starttmp is not None:
            params["starttmp"] = starttmp
        if endtmp is not None:
            params["endtmp"] = endtmp
        return await client.get("/dailyledger", module="accounting", params=params)

    @mcp.tool()
    async def create_ledger_entry(data: dict[str, Any]) -> Any:
        """Create a manual accounting ledger entry (double-entry bookkeeping).

        Required fields:
        - date (integer): Entry date as Unix timestamp
        - lines (array): Minimum 2 lines (debits must equal credits). Each line:
            - account (integer): Account number (must match an existing account)
            - debit (number): Debit amount (omit or 0 if credit)
            - credit (number): Credit amount (omit or 0 if debit)
            - description (string, optional): Line description
            - tags (array, optional): Line tags

        Optional fields:
        - notes (string): Entry note/description

        Constraints: Total debits must equal total credits. A single line cannot
        have both debit and credit values.

        Returns: {entryGroupId: "<id>"}
        """
        return await client.post("/entry", module="accounting", json=data)

    @mcp.tool()
    async def list_accounts(starttmp: int | None = None, endtmp: int | None = None, include_empty: bool = False) -> Any:
        """List the chart of accounts.

        Optional filters:
        - starttmp: Start date as Unix timestamp (for balance calculations)
        - endtmp: End date as Unix timestamp
        - include_empty: If true, include accounts with zero balance (default: false)

        Returns an array of account objects with: id, accountNumber, name,
        debit total, credit total, and balance.
        """
        params: dict[str, Any] = {}
        if starttmp is not None:
            params["starttmp"] = starttmp
        if endtmp is not None:
            params["endtmp"] = endtmp
        if include_empty:
            params["includeEmpty"] = 1
        return await client.get("/chartofaccounts", module="accounting", params=params)

    @mcp.tool()
    async def create_account(data: dict[str, Any]) -> Any:
        """Create a new account in the chart of accounts.

        Required fields:
        - prefix (integer): 4-digit account prefix (e.g. 7000). Holded auto-generates
          the next available account number under this prefix (e.g. 70000001).

        Optional fields:
        - name (string): Account name (falls back to parent account name if omitted)
        - color (string): Hex color code for display

        Returns: {accountId: "<id>"}
        """
        return await client.post("/account", module="accounting", json=data)

    @mcp.tool()
    async def get_account(account_id: str) -> Any:
        """Get a single account from the chart of accounts by its ID.

        Returns the account details including number, name, type, and balance.
        """
        return await client.get(f"/accounts/{account_id}", module="accounting")
