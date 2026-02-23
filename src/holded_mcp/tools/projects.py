from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from holded_mcp.client import HoldedClient


def register(mcp: FastMCP, client: HoldedClient) -> None:

    @mcp.tool()
    async def list_projects(page: int = 1) -> Any:
        """List all projects in Holded (paginated).

        Returns an array of project objects with: id, name, desc, tags, category,
        contactId, contactName, date, dueDate, status, lists, billable, expenses,
        estimates, sales, timeTracking, price, numberOfTasks, completedTasks, labels.
        """
        return await client.list_paginated("/projects", module="projects", page=page)

    @mcp.tool()
    async def get_project(project_id: str) -> Any:
        """Get a single project by ID, including summary and task counts.

        Returns the full project object with all fields including profitability data.
        """
        return await client.get(f"/projects/{project_id}", module="projects")

    @mcp.tool()
    async def create_project(data: dict[str, Any]) -> Any:
        """Create a new project in Holded.

        Required fields:
        - name (string): Project name

        Optional fields:
        - desc (string): Project description
        - contactId (string): Associated contact/client ID
        - contactName (string): Client name
        - date (integer): Start date as Unix timestamp
        - dueDate (integer): Due date as Unix timestamp
        - status (string): Project status
        - tags (array of strings): Tags
        - billable (boolean): Whether project is billable
        - price (number): Project price/budget
        - labels (array): Project labels

        Returns: {status: 1, info: "Created", id: "<project_id>"}
        """
        return await client.post("/projects", module="projects", json=data)

    @mcp.tool()
    async def update_project(project_id: str, data: dict[str, Any]) -> Any:
        """Update a project by ID. Partial updates supported.

        Updatable fields: name, desc, tags, contactName, date, dueDate, status,
        lists, billable, price, labels. Only included fields are modified.
        """
        return await client.put(f"/projects/{project_id}", module="projects", json=data)

    @mcp.tool()
    async def delete_project(project_id: str) -> Any:
        """Delete a project by ID. This action is irreversible."""
        return await client.delete(f"/projects/{project_id}", module="projects")

    @mcp.tool()
    async def list_tasks(project_id: str | None = None, page: int = 1) -> Any:
        """List tasks, optionally filtered by project (paginated).

        Returns an array of task objects with: id, projectId, listId, name, desc,
        labels, comments (array of {commentId, createdAt, userId, message}),
        date, dueDate, userId, createdAt, updatedAt, status, billable, featured.
        """
        if project_id:
            return await client.list_paginated(f"/projects/{project_id}/tasks", module="projects", page=page)
        return await client.list_paginated("/tasks", module="projects", page=page)

    @mcp.tool()
    async def create_task(data: dict[str, Any]) -> Any:
        """Create a new task in a project.

        Required fields:
        - projectId (string): The project this task belongs to
        - listId (string): The list/column within the project
        - name (string): Task name

        Optional fields:
        - desc (string): Task description
        - labels (array): Task labels
        - userId (string): Assigned user ID
        - date (integer): Start date as Unix timestamp
        - dueDate (integer): Due date as Unix timestamp
        - billable (boolean): Whether task time is billable
        - featured (boolean): Pin/highlight the task

        Returns: {status: 1, info: "Created", id: "<task_id>"}
        """
        return await client.post("/tasks", module="projects", json=data)

    @mcp.tool()
    async def update_task(task_id: str, data: dict[str, Any]) -> Any:
        """Update a task by ID. Partial updates supported.

        Accepts the same optional fields as create_task. Only included fields are modified.
        """
        return await client.put(f"/tasks/{task_id}", module="projects", json=data)

    @mcp.tool()
    async def list_time_records(project_id: str, page: int = 1) -> Any:
        """List time tracking records for a project (paginated).

        Returns an array of time record objects with: id, projectId, taskId,
        userId, duration, costHour, desc, date.
        """
        return await client.list_paginated(f"/projects/{project_id}/times", module="projects", page=page)

    @mcp.tool()
    async def create_time_record(project_id: str, data: dict[str, Any]) -> Any:
        """Create a time tracking record for a project.

        Required fields:
        - duration (number): Time spent (in hours or minutes depending on config)
        - costHour (number): Cost per hour rate

        Optional fields:
        - desc (string): Description of work done
        - userId (string): Employee/user who performed the work
        - taskId (string): Associated task ID

        Returns: {status: 1, info: "Created", id: "<time_record_id>"}
        """
        return await client.post(f"/projects/{project_id}/times", module="projects", json=data)
