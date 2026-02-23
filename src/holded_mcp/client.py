from __future__ import annotations

import os
from typing import Any

import httpx

BASE_URLS = {
    "invoicing": "https://api.holded.com/api/invoicing/v1",
    "crm": "https://api.holded.com/api/crm/v1",
    "projects": "https://api.holded.com/api/projects/v1",
    "team": "https://api.holded.com/api/team/v1",
    "accounting": "https://api.holded.com/api/accounting/v1",
}


class HoldedClient:
    def __init__(self, api_key: str | None = None, allowed_methods: str | None = None) -> None:
        self.api_key = api_key or os.environ.get("HOLDED_API_KEY", "")
        if not self.api_key:
            raise ValueError("HOLDED_API_KEY is required")
        raw = allowed_methods or os.environ.get("HOLDED_ALLOWED_METHODS", "ALL")
        self._allowed_methods: set[str] | None = (
            None if raw.strip().upper() == "ALL"
            else {m.strip().upper() for m in raw.split(",") if m.strip()}
        )
        self._client = httpx.AsyncClient(
            headers={"key": self.api_key, "Content-Type": "application/json"},
            timeout=30.0,
        )

    def _check_method(self, method: str) -> None:
        if self._allowed_methods is not None and method not in self._allowed_methods:
            raise PermissionError(
                f"HTTP {method} is not allowed. Allowed methods: {', '.join(sorted(self._allowed_methods))}"
            )

    def _url(self, path: str, module: str = "invoicing") -> str:
        return f"{BASE_URLS[module]}{path}"

    async def get(self, path: str, *, module: str = "invoicing", params: dict[str, Any] | None = None) -> Any:
        self._check_method("GET")
        resp = await self._client.get(self._url(path, module), params=params)
        resp.raise_for_status()
        return resp.json()

    async def post(self, path: str, *, module: str = "invoicing", json: dict[str, Any] | None = None) -> Any:
        self._check_method("POST")
        resp = await self._client.post(self._url(path, module), json=json)
        resp.raise_for_status()
        return resp.json()

    async def put(self, path: str, *, module: str = "invoicing", json: dict[str, Any] | None = None) -> Any:
        self._check_method("PUT")
        resp = await self._client.put(self._url(path, module), json=json)
        resp.raise_for_status()
        return resp.json()

    async def delete(self, path: str, *, module: str = "invoicing") -> Any:
        self._check_method("DELETE")
        resp = await self._client.delete(self._url(path, module))
        resp.raise_for_status()
        return resp.json()

    async def list_paginated(self, path: str, *, module: str = "invoicing", page: int = 1) -> Any:
        return await self.get(path, module=module, params={"page": page})

    async def close(self) -> None:
        await self._client.aclose()
