from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from holded_mcp.client import HoldedClient


def register(mcp: FastMCP, client: HoldedClient) -> None:

    @mcp.tool()
    async def list_contacts(page: int = 1) -> Any:
        """List all contacts (paginated, max 500 per page).

        Returns an array of contact objects with fields: id, customId, name, code (NIF/CIF/VAT),
        tradeName, email, mobile, phone, type, iban, swift, clientRecord, supplierRecord,
        billAddress, defaults, socialNetworks, tags, notes, contactPersons, shippingAddresses,
        customFields.
        """
        return await client.list_paginated("/contacts", page=page)

    @mcp.tool()
    async def get_contact(contact_id: str) -> Any:
        """Get a single contact by its Holded ID.

        Returns the full contact object including all fields: name, email, phone, mobile,
        code (NIF/CIF/VAT), type, billAddress, shippingAddresses, defaults (dueDays,
        paymentMethod, discount, currency, language), tags, notes, contactPersons, etc.
        """
        return await client.get(f"/contacts/{contact_id}")

    @mcp.tool()
    async def create_contact(data: dict[str, Any]) -> Any:
        """Create a new contact in Holded.

        Accepted fields:
        - name (string): Contact name
        - CustomId (string): Custom reference identifier
        - code (string): NIF/CIF/VAT number
        - email (string): Email address
        - mobile (string): Mobile phone
        - phone (string): Phone number
        - type (string): One of "client", "supplier", "debtor", "creditor", "lead"
        - isperson (boolean): true = person, false = company
        - iban (string): Bank IBAN
        - swift (string): SWIFT code
        - billAddress (object): {address, city, postalCode, province, country}
        - shippingAddresses (array): Array of address objects
        - defaults (object): {dueDays, paymentMethod, discount, currency, language, expensesAccountRecord}
        - groupId (string): Contact group ID
        - tags (array of strings): Tags for categorization
        - note (string): Free-text notes
        - contactPersons (array): [{name, phone, email}]

        Returns: {status: 1, info: "Created", id: "<contact_id>"}
        """
        return await client.post("/contacts", json=data)

    @mcp.tool()
    async def update_contact(contact_id: str, data: dict[str, Any]) -> Any:
        """Update an existing contact by ID. Only included fields are modified.

        Accepts the same fields as create_contact. Partial updates are supported —
        only the fields present in the request body will be changed.

        Returns: {status: 1, info: "Updated", id: "<contact_id>"}
        """
        return await client.put(f"/contacts/{contact_id}", json=data)

    @mcp.tool()
    async def delete_contact(contact_id: str) -> Any:
        """Delete a contact by its Holded ID.

        This action is irreversible. Returns: {status: 1, info: "Deleted"}
        """
        return await client.delete(f"/contacts/{contact_id}")
