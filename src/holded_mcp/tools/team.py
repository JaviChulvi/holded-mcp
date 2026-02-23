from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from holded_mcp.client import HoldedClient


def register(mcp: FastMCP, client: HoldedClient) -> None:

    @mcp.tool()
    async def list_employees(page: int = 1) -> Any:
        """List all employees in Holded (paginated, max 500 per page).

        Returns an array of employee objects with: id, name, lastName, email, phone,
        mobile, dateOfBirth, gender, nationality, workplace, teams, reportingTo,
        socialSecurityNum, iban, code (NIF), timeOffPolicyId.
        """
        return await client.list_paginated("/employees", module="team", page=page)

    @mcp.tool()
    async def get_employee(employee_id: str) -> Any:
        """Get a single employee by their Holded ID.

        Returns the full employee object including personal details, contact info,
        employment data, and team assignments.
        """
        return await client.get(f"/employees/{employee_id}", module="team")

    @mcp.tool()
    async def create_employee(data: dict[str, Any]) -> Any:
        """Create a new employee in Holded.

        Required fields:
        - name (string): First name
        - lastName (string): Last name
        - email (string): Email address

        Optional fields:
        - sendInvite (boolean): Send invitation email to the employee
        - phone (string): Phone number
        - mobile (string): Mobile number
        - dateOfBirth (string): Date of birth in dd/mm/yyyy format
        - gender (string): Gender
        - nationality (string): Nationality
        - mainLanguage (string): Preferred language
        - iban (string): Bank account IBAN
        - code (string): NIF/tax ID
        - socialSecurityNum (string): Social security number
        - workplace (string): Workplace/office
        - teams (array): Team assignments
        - reportingTo (string): Manager's employee ID
        - timeOffPolicyId (string): Time-off policy ID

        Returns: {status: 1, info: "Created", id: "<employee_id>"}
        """
        return await client.post("/employees", module="team", json=data)

    @mcp.tool()
    async def update_employee(employee_id: str, data: dict[str, Any]) -> Any:
        """Update an existing employee by ID. Partial updates supported.

        Updatable fields: name, lastName, mainEmail, email, phone, mobile,
        dateOfBirth (dd/mm/yyyy), gender, nationality, mainLanguage, iban,
        code (NIF), socialSecurityNum, workplace, teams, reportingTo,
        timeOffPolicyId, plus address and fiscal details.
        """
        return await client.put(f"/employees/{employee_id}", module="team", json=data)

    @mcp.tool()
    async def clock_in(employee_id: str, data: dict[str, Any] | None = None) -> Any:
        """Clock in an employee (start work shift).

        Optional fields:
        - location (object): Geolocation data (latitude, longitude)

        The clock-in time is recorded as the current server time unless overridden.
        """
        return await client.post(f"/employees/{employee_id}/times/clockin", module="team", json=data)

    @mcp.tool()
    async def clock_out(employee_id: str, data: dict[str, Any] | None = None) -> Any:
        """Clock out an employee (end work shift).

        Optional fields:
        - latitude (number): GPS latitude
        - longitude (number): GPS longitude

        The clock-out time is recorded as the current server time unless overridden.
        """
        return await client.post(f"/employees/{employee_id}/times/clockout", module="team", json=data)

    @mcp.tool()
    async def list_time_entries(employee_id: str, page: int = 1) -> Any:
        """List time/attendance entries for an employee (paginated).

        Returns an array of time entry objects with clock-in/out times,
        break periods, and total hours worked.
        """
        return await client.list_paginated(f"/employees/{employee_id}/times", module="team", page=page)
