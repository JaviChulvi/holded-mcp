from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from holded_mcp.client import HoldedClient


def register(mcp: FastMCP, client: HoldedClient) -> None:

    @mcp.tool()
    async def list_funnels() -> Any:
        """List all CRM funnels (sales pipelines) in Holded.

        Returns an array of funnel objects with: id, name, stages (array of
        {stageId, key, name, desc}), labels (array of {labelId, labelName, labelColor}),
        customFields, preferences, won ({num, value}), leads, lost.
        """
        return await client.get("/funnels", module="crm")

    @mcp.tool()
    async def list_leads(page: int = 1) -> Any:
        """List all CRM leads/deals (paginated).

        Returns an array of lead objects with: id, name, funnelId, stageId,
        contactId, contactName, value, potential, dueDate, status, tags.
        """
        return await client.list_paginated("/leads", module="crm", page=page)

    @mcp.tool()
    async def get_lead(lead_id: str) -> Any:
        """Get a single CRM lead/deal by its ID.

        Returns the full lead object including funnel position, contact info,
        value, notes, tasks, and activity history.
        """
        return await client.get(f"/leads/{lead_id}", module="crm")

    @mcp.tool()
    async def create_lead(data: dict[str, Any]) -> Any:
        """Create a new CRM lead/deal in a funnel.

        Required fields:
        - funnelId (string): The funnel/pipeline ID (get from list_funnels)
        - name (string): Lead/deal name

        Optional fields:
        - contactId (string): Link to an existing contact
        - contactName (string): Contact name (for display)
        - stageId (string): Stage ID or exact stage name within the funnel
        - value (integer): Deal monetary value
        - potential (integer): Win probability percentage (0-100)
        - dueDate (integer): Expected close date as Unix timestamp

        Returns: {status: 1, info: "Created", id: "<lead_id>"}
        """
        return await client.post("/leads", module="crm", json=data)

    @mcp.tool()
    async def update_lead(lead_id: str, data: dict[str, Any]) -> Any:
        """Update a CRM lead/deal by ID. Partial updates supported.

        Accepts the same fields as create_lead. Only included fields are modified.
        Use this to move a lead between stages, update its value, etc.
        """
        return await client.put(f"/leads/{lead_id}", module="crm", json=data)

    @mcp.tool()
    async def delete_lead(lead_id: str) -> Any:
        """Delete a CRM lead/deal by ID. This action is irreversible."""
        return await client.delete(f"/leads/{lead_id}", module="crm")

    @mcp.tool()
    async def list_events(lead_id: str | None = None) -> Any:
        """List CRM events/activities. If lead_id is provided, lists events for that lead only.

        Returns an array of event objects with: id, name, contactId, contactName,
        kind (event type), desc, startDate, endDate, status, tags, locationDesc,
        leadId, funnelId.
        """
        if lead_id:
            return await client.get(f"/leads/{lead_id}/events", module="crm")
        return await client.get("/events", module="crm")

    @mcp.tool()
    async def create_event(data: dict[str, Any]) -> Any:
        """Create a new CRM event/activity.

        Required fields:
        - name (string): Event name/title

        Optional fields:
        - contactId (string): Associated contact ID
        - contactName (string): Contact name
        - kind (string): Event type
        - desc (string): Description
        - startDate (integer): Start time as Unix timestamp
        - duration (integer): Duration in seconds
        - status (integer): Event status code
        - tags (array of strings): Event tags
        - locationDesc (string): Location description
        - leadId (string): Associated lead ID
        - funnelId (string): Associated funnel ID
        - userId (string): Assigned user ID

        Returns: {status: 1, info: "Created", id: "<event_id>"}
        """
        return await client.post("/events", module="crm", json=data)
