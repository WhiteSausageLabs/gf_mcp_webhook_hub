import hashlib
import secrets
from odoo import api, fields, models, _


class GfMcpApiKey(models.Model):
    _name = 'gf.mcp.api.key'
    _description = 'MCP API Key'
    _inherit = ['mail.thread']
    _order = 'id desc'

    name = fields.Char(required=True, tracking=True)
    active = fields.Boolean(default=True, tracking=True)
    key_hash = fields.Char(copy=False, readonly=True)
    key_preview = fields.Char(readonly=True, copy=False)
    allowed_model_ids = fields.Many2many('ir.model', string='Allowed Models')
    read_only = fields.Boolean(default=True, tracking=True)
    last_used_at = fields.Datetime(readonly=True)
    note = fields.Text()

    @api.model_create_multi
    def create(self, vals_list):
        plain_tokens = {}
        for i, vals in enumerate(vals_list):
            if not vals.get('key_hash'):
                token = secrets.token_urlsafe(32)
                vals['key_hash'] = self._hash_token(token)
                vals['key_preview'] = token[:8] + '\u2026' + token[-4:]
                plain_tokens[i] = token
        records = super().create(vals_list)
        for i, record in enumerate(records):
            if i in plain_tokens:
                record.message_post(body=_('API key created. Copy it from the creation response or regenerate if lost.'))
        return records

    @api.model
    def _hash_token(self, token):
        return hashlib.sha256(token.encode('utf-8')).hexdigest()

    @api.model
    def authenticate_token(self, token):
        if not token:
            return self.browse()
        key_hash = self._hash_token(token)
        return self.sudo().search([('key_hash', '=', key_hash), ('active', '=', True)], limit=1)

    def is_model_allowed(self, model_name):
        self.ensure_one()
        return model_name in self.allowed_model_ids.mapped('model')
