from odoo import fields, models


class GfMcpAuditLog(models.Model):
    _name = 'gf.mcp.audit.log'
    _description = 'MCP Audit Log'
    _order = 'create_date desc, id desc'

    api_key_id = fields.Many2one('gf.mcp.api.key', ondelete='set null')
    action = fields.Char(required=True)
    model_name = fields.Char()
    record_id = fields.Integer()
    status = fields.Selection([
        ('allowed', 'Allowed'),
        ('denied', 'Denied'),
        ('error', 'Error'),
    ], required=True, default='allowed')
    message = fields.Text()
    request_ip = fields.Char()
