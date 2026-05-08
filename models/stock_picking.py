from odoo import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        result = super().button_validate()
        dispatcher = self.env['gf.webhook.dispatch.mixin']
        for picking in self:
            if picking.state == 'done':
                dispatcher._gf_fire_webhooks('stock_picking_done', picking, {
                    'name': picking.name,
                    'picking_type': picking.picking_type_id.display_name,
                    'partner_id': picking.partner_id.id if picking.partner_id else False,
                })
        return result
