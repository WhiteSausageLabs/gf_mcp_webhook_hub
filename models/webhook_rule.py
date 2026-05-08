import hmac
import hashlib
import json
from odoo import fields, models


class GfWebhookRule(models.Model):
    _name = 'gf.webhook.rule'
    _description = 'Webhook Rule'
    _inherit = ['mail.thread']
    _order = 'id desc'

    name = fields.Char(required=True, tracking=True)
    active = fields.Boolean(default=True, tracking=True)
    event = fields.Selection([
        ('sale_order_confirmed', 'Sale Order Confirmed'),
        ('invoice_posted', 'Invoice Posted'),
        ('stock_picking_done', 'Stock Picking Done'),
    ], required=True, tracking=True)
    target_url = fields.Char(required=True, tracking=True)
    secret = fields.Char(required=True, help='Used to sign payloads with HMAC-SHA256.')
    retry_count = fields.Integer(default=3)

    def _signature(self, payload):
        self.ensure_one()
        body = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode('utf-8')
        return hmac.new((self.secret or '').encode('utf-8'), body, hashlib.sha256).hexdigest()

    def test_signature(self):
        for rule in self:
            payload = {'event': 'test', 'rule_id': rule.id}
            self.env['gf.webhook.log'].create({
                'rule_id': rule.id,
                'event': 'test',
                'target_url': rule.target_url,
                'status': 'prepared',
                'payload': json.dumps(payload),
                'signature': rule._signature(payload),
            })
