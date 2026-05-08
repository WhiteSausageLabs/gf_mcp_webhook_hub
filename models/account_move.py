from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        result = super().action_post()
        dispatcher = self.env['gf.webhook.dispatch.mixin']
        for move in self:
            if move.is_invoice(include_receipts=True):
                dispatcher._gf_fire_webhooks('invoice_posted', move, {
                    'name': move.name,
                    'move_type': move.move_type,
                    'amount_total': move.amount_total,
                    'currency': move.currency_id.name,
                    'partner_id': move.partner_id.id,
                })
        return result
