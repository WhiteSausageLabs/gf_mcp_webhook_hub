# MCP Webhook Hub for Odoo 19

Secure read-only MCP endpoint and signed webhook automation hub for Odoo.

Built by **White Sausage Labs**.

> This repository is the public product page and documentation repository.  
> The commercial Odoo module is distributed through the Odoo Apps Store under the OPL-1 license.

## What it does

MCP Webhook Hub connects AI agents and automation systems to Odoo with:

- Read-only MCP-style endpoint for Odoo data access
- Scoped API keys with explicit model allowlists
- SHA-256 hashed API tokens at rest
- Audit logs for every API request
- Signed outbound webhooks using HMAC-SHA256
- Delivery logs with status, response code, and response body
- Events for sale order confirmation, invoice posting, and stock picking validation

## MCP endpoint

`POST /gf_mcp_webhook_hub/mcp`

Supported read-only actions:

| Action | Description |
| --- | --- |
| `list_models` | Lists models available to the API key |
| `search` | Searches records by Odoo domain and returns IDs |
| `read` | Reads selected fields from selected records |
| `count` | Counts records matching a domain |

No create, write, or delete operations are exposed in v1.

## Webhook events

| Event | Trigger |
| --- | --- |
| `sale_order_confirmed` | Sale order is confirmed |
| `invoice_posted` | Invoice or credit note is posted |
| `stock_picking_done` | Delivery/receipt is validated |

Each webhook request includes an `X-Odoo-Webhook-Signature` header with a HMAC-SHA256 signature.

## Screenshots

![API Keys](screenshots/api-keys.png)

![Webhook Rules](screenshots/webhook-rules.png)

![Audit Logs](screenshots/audit-logs.png)

![Webhook Logs](screenshots/webhook-logs.png)

## Availability

Odoo Apps Store listing: coming soon.

## Support

Use the Odoo Apps Store messaging system for purchase-related support and bug reports.

Support covers confirmed bugs in the purchased Odoo 19 version. It does not include custom development, migration to other Odoo versions, or third-party integration setup.

## License

The commercial Odoo module is licensed under **OPL-1**.

This public documentation repository does not contain the commercial module source code.
