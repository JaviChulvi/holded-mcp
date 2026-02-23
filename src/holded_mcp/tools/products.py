from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from holded_mcp.client import HoldedClient


def register(mcp: FastMCP, client: HoldedClient) -> None:

    @mcp.tool()
    async def list_products(page: int = 1) -> Any:
        """List all products in Holded (paginated).

        Returns an array of product objects with: id, name, desc, sku, barcode,
        price, tax, cost, purchasePrice, stock, weight, kind, tags.
        """
        return await client.list_paginated("/products", page=page)

    @mcp.tool()
    async def get_product(product_id: str) -> Any:
        """Get a single product by its Holded ID.

        Returns the full product object including pricing, stock levels, and metadata.
        """
        return await client.get(f"/products/{product_id}")

    @mcp.tool()
    async def create_product(data: dict[str, Any]) -> Any:
        """Create a new product in Holded.

        Accepted fields:
        - name (string): Product name
        - desc (string): Description
        - sku (string): Stock keeping unit code
        - barcode (string): Barcode
        - price (number): Selling price
        - tax (number): Tax percentage
        - cost (number): Cost price
        - purchasePrice (number): Purchase price
        - stock (integer): Initial stock quantity
        - weight (number): Product weight
        - kind (string): Product kind/type
        - tags (array of strings): Tags for categorization

        Returns: {status: 1, info: "Created", id: "<product_id>"}
        """
        return await client.post("/products", json=data)

    @mcp.tool()
    async def update_product(product_id: str, data: dict[str, Any]) -> Any:
        """Update an existing product by ID. Partial updates supported.

        Accepts the same fields as create_product. Only included fields are modified.
        """
        return await client.put(f"/products/{product_id}", json=data)

    @mcp.tool()
    async def delete_product(product_id: str) -> Any:
        """Delete a product by its Holded ID. This action is irreversible."""
        return await client.delete(f"/products/{product_id}")

    @mcp.tool()
    async def update_stock(product_id: str, data: dict[str, Any]) -> Any:
        """Update stock levels for a product across warehouses and variants.

        The data must follow this structure:
        {
            "stock": {
                "<warehouseId>": {
                    "<productId_or_variantId>": <quantity>
                }
            }
        }

        This allows setting stock for multiple warehouses and product variants in a single call.

        Returns: {status: 1, info: "Updated", id: "<product_id>"}
        """
        return await client.put(f"/products/{product_id}/stock", json=data)
