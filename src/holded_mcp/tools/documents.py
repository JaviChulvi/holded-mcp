from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from holded_mcp.client import HoldedClient


def register(mcp: FastMCP, client: HoldedClient) -> None:

    @mcp.tool()
    async def list_documents(doc_type: str, page: int = 1) -> Any:
        """List documents of a given type (paginated).

        doc_type must be one of: invoice, salesreceipt, creditnote, estimate, salesorder,
        waybill, proform, purchase, purchaserefund, purchaseorder.

        Optional query filters (pass via page param for pagination):
        - starttmp/endtmp (integer): Unix timestamp range filter
        - contactid (string): Filter by contact ID
        - paid (integer): 0=unpaid, 1=paid, 2=partially paid
        - sort (string): "created-asc" or "created-desc"

        Returns an array of document objects with: id, contact, contactName, desc, date,
        dueDate, notes, products, tax, subtotal, discount, total, language, status,
        docNumber, currency, paymentsTotal, paymentsPending.
        """
        return await client.list_paginated(f"/documents/{doc_type}", page=page)

    @mcp.tool()
    async def get_document(doc_type: str, document_id: str) -> Any:
        """Get a single document by type and ID.

        doc_type: invoice, salesreceipt, creditnote, estimate, salesorder, waybill,
        proform, purchase, purchaserefund, purchaseorder.

        Returns the full document object including items, totals, payment status, and metadata.
        """
        return await client.get(f"/documents/{doc_type}/{document_id}")

    @mcp.tool()
    async def create_document(doc_type: str, data: dict[str, Any]) -> Any:
        """Create a new document (invoice, estimate, purchase order, etc.) in Holded.

        doc_type: invoice, salesreceipt, creditnote, estimate, salesorder, waybill,
        proform, purchase, purchaserefund, purchaseorder.

        Key fields:
        - contactId (string): Link to existing contact, OR use contactName/contactEmail
          to create inline
        - date (integer): Document date as Unix timestamp
        - dueDate (integer): Payment deadline as Unix timestamp
        - items (array): Line items, each with:
            - name (string): Item name
            - desc (string): Item description
            - units (number): Quantity
            - subtotal (number): Unit price (before tax)
            - discount (number): Discount percentage
            - tax (integer): Tax/IVA percentage
            - sku (string): SKU code
            - serviceId (string): Link to existing product
        - desc (string): Document description
        - notes (string): Additional notes
        - currency (string): ISO currency code (e.g. "EUR", "USD")
        - currencyChange (number): Exchange rate
        - language (string): Document language
        - paymentMethodId (string): Payment method ID
        - numSerieId (string): Numbering series ID
        - invoiceNum (string): Custom invoice number
        - tags (array of strings): Document tags
        - salesChannelId (string): Sales channel ID
        - applyContactDefaults (boolean): Apply contact's default settings (true by default)

        Shipping fields: shippingAddress, shippingPostalCode, shippingCity,
        shippingProvince, shippingCountry.

        Returns: {status: 1, id: "<doc_id>", invoiceNum: "F170009", contactId: "<id>"}
        """
        return await client.post(f"/documents/{doc_type}", json=data)

    @mcp.tool()
    async def update_document(doc_type: str, document_id: str, data: dict[str, Any]) -> Any:
        """Update an existing document by type and ID. Partial updates supported.

        Accepts the same fields as create_document. Only included fields are modified.
        """
        return await client.put(f"/documents/{doc_type}/{document_id}", json=data)

    @mcp.tool()
    async def delete_document(doc_type: str, document_id: str) -> Any:
        """Delete a document by type and ID. This action is irreversible."""
        return await client.delete(f"/documents/{doc_type}/{document_id}")

    @mcp.tool()
    async def pay_document(doc_type: str, document_id: str, data: dict[str, Any]) -> Any:
        """Record a payment on a document.

        Required fields:
        - date (integer): Payment date as Unix timestamp
        - amount (number): Payment amount

        Optional fields:
        - treasury (string): Treasury account ID to register the payment against
        - desc (string): Payment description

        Returns: {status: 1, invoiceId: "<id>", invoiceNum: "<num>", paymentId: "<id>"}
        """
        return await client.post(f"/documents/{doc_type}/{document_id}/pay", json=data)

    @mcp.tool()
    async def send_document(doc_type: str, document_id: str, data: dict[str, Any]) -> Any:
        """Send a document to one or more recipients via email.

        Required fields:
        - emails (string): Comma-separated email addresses

        Optional fields:
        - subject (string): Email subject (min 10 characters)
        - message (string): Email body (min 20 characters)
        - mailTemplateId (string): Email template ID

        Returns: {status: 1, info: "Document sent"}
        """
        return await client.post(f"/documents/{doc_type}/{document_id}/send", json=data)

    @mcp.tool()
    async def get_document_pdf(doc_type: str, document_id: str) -> Any:
        """Get the PDF content of a document as base64-encoded data.

        Returns: {status: 1, data: "<base64-encoded PDF>"}
        """
        return await client.get(f"/documents/{doc_type}/{document_id}/pdf")
