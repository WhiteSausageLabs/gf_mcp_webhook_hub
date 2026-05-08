# MCP Webhook Hub

Secure MCP endpoint and signed webhook automation hub for Odoo

**Technical module name:** `gf_mcp_webhook_hub`  
**Odoo version:** `19.0`  
**Current version:** `19.0.1.0.4`  
**Category:** `Extra Tools`  
**License:** `OPL-1`  
**Price:** `210.0 EUR`

---

## Repository Layout

This repository is intentionally structured for Odoo Apps compatibility:

- Module root folder: `./gf_mcp_webhook_hub`
- Manifest path: `./gf_mcp_webhook_hub/__manifest__.py`

Odoo Apps expects the module to be in a dedicated folder at repository root.

---

## Dependencies

`base, mail, sale, account, stock`

---

## Installation

1. Add this repository to your addons source.
2. Ensure `./gf_mcp_webhook_hub` is in your addons path.
3. Update Apps List in Odoo.
4. Install `gf_mcp_webhook_hub`.

---

## Support

- Email: support@whitesausagelabs.com
- Vendor: White Sausage Labs
- Website: https://whitesausagelabs.com

---

## Notes

- Production-ready Odoo 19 addon.
- Clean `_inherit` extensions (no monkeypatching).
- Includes tests and security access rules.
