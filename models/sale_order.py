from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        result = super().action_confirm()
        dispatcher = self.env['gf.webhook.dispatch.mixin']
        for order in self:
            dispatcher._gf_fire_webhooks('sale_order_confirmed', order, {
                'name': order.name,
                'amount_total': order.amount_total,
                'currency': order.currency_id.name,
                'partner_id': order.partner_id.id,
            })
        return result
