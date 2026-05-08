from odoo import fields, models


class GfWebhookLog(models.Model):
    _name = 'gf.webhook.log'
    _description = 'Webhook Delivery Log'
    _order = 'create_date desc, id desc'

    rule_id = fields.Many2one('gf.webhook.rule', ondelete='set null')
    event = fields.Char(required=True)
    target_url = fields.Char()
    status = fields.Selection([
        ('prepared', 'Prepared'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('retry', 'Retry Scheduled'),
    ], required=True, default='prepared')
    payload = fields.Text()
    signature = fields.Char()
    response_code = fields.Integer()
    response_body = fields.Text()
