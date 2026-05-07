<p align="center">
  <img src="assets/hero.jpg" alt="MCP Webhook Hub by White Sausage Labs" width="100%">
</p>

# MCP Webhook Hub for Odoo 19

**Secure AI access and signed automation events for Odoo.**

MCP Webhook Hub gives teams a controlled bridge between Odoo, AI agents, and automation platforms: read-only MCP-style access, scoped API keys, full audit logs, and HMAC-signed outbound webhooks.

Built by **White Sausage Labs** — focused Odoo automation tools with a security-first release gate.

> This repository is the public product page and documentation repository.  
> The commercial Odoo module is distributed through the Odoo Apps Store under the OPL-1 license.  
> The paid module source code is not published here.

---

## Why this exists

AI agents and workflow tools are increasingly useful around ERP data — but direct, unscoped access to Odoo is risky.

MCP Webhook Hub keeps v1 intentionally narrow:

- **Read-only MCP access** — no create/write/delete endpoint
- **Model allowlists** — each key only sees explicitly allowed models
- **Hashed tokens** — API keys are not stored in plain text
- **Audit trail** — every request is logged with action, model, status, and IP
- **Signed webhooks** — outbound event payloads use HMAC-SHA256
- **Delivery logs** — response status, code, and body are tracked

---

## Product visuals

![AI-safe Odoo access](assets/visual_architecture.jpg)

![Security first](assets/visual_security.jpg)

![Verified webhooks](assets/visual_webhooks.jpg)

![Product-grade releases](assets/visual_release_gate.jpg)

---

## Features

| Area | Capability |
| --- | --- |
| MCP Endpoint | `list_models`, `search`, `read`, `count` |
| Authentication | Bearer token or `api_key` parameter |
| Security | SHA-256 token hash, read-only mode, model allowlists |
| Audit | Allowed, denied, and error requests are logged |
| Webhooks | Business events delivered to external HTTP endpoints |
| Signing | HMAC-SHA256 signature header |
| Logs | Delivery status, response code, response body |
| Odoo Version | 19.0 |

---

## MCP endpoint

```http
POST /gf_mcp_webhook_hub/mcp
Authorization: Bearer <token>
Content-Type: application/json
```

Example request:

```json
{
  "action": "search",
  "model": "res.partner",
  "domain": [["is_company", "=", true]],
  "limit": 10
}
```

Supported actions:

| Action | Description |
| --- | --- |
| `list_models` | Lists models available to the API key |
| `search` | Searches records by Odoo domain and returns IDs |
| `read` | Reads selected fields from selected records |
| `count` | Counts records matching a domain |

No create, write, unlink, or raw SQL operations are exposed in v1.

---

## Webhook events

| Event | Trigger |
| --- | --- |
| `sale_order_confirmed` | Sale order is confirmed |
| `invoice_posted` | Invoice or credit note is posted |
| `stock_picking_done` | Delivery or receipt is validated |

Each outbound request includes:

```http
X-Odoo-Webhook-Signature: <hmac-sha256>
Content-Type: application/json
User-Agent: gf-mcp-webhook-hub/19.0
```

---

## Screenshots

### Scoped API keys

![API Keys](screenshots/api-keys.png)

### Signed webhook rules

![Webhook Rules](screenshots/webhook-rules.png)

### MCP audit trail

![Audit Logs](screenshots/audit-logs.png)

### Webhook delivery logs

![Webhook Logs](screenshots/webhook-logs.png)

---

## Release quality

The Odoo module release gate currently checks:

- Manifest parses and uses OPL-1
- Required Odoo Apps Store files exist
- Static module checks pass
- Docker install test on Odoo 19 passes
- 19 module tests pass with 0 failures / 0 errors
- Release ZIP is packaged cleanly

---

## Availability

Odoo Apps Store listing: coming soon.

## Support

Use the Odoo Apps Store messaging system for purchase-related support and bug reports.

Support covers confirmed bugs in the purchased Odoo 19 version. It does not include custom development, migration to other Odoo versions, or third-party integration setup.

## License

The commercial Odoo module is licensed under **OPL-1**.

This public documentation repository does not contain the commercial module source code.
