from odoo.tests.common import TransactionCase


class TestMcpWebhookHubSecurityModels(TransactionCase):

    def test_api_key_hash_and_scope(self):
        model = self.env['ir.model'].search([('model', '=', 'res.partner')], limit=1)
        key = self.env['gf.mcp.api.key'].create({
            'name': 'Test Key',
            'allowed_model_ids': [(6, 0, model.ids)],
        })
        self.assertTrue(key.key_hash)
        self.assertTrue(key.read_only)
        self.assertTrue(key.is_model_allowed('res.partner'))
        self.assertFalse(key.is_model_allowed('sale.order'))

    def test_webhook_signature_is_stable(self):
        rule = self.env['gf.webhook.rule'].create({
            'name': 'Test Rule',
            'event': 'sale_order_confirmed',
            'target_url': 'https://example.com/webhook',
            'secret': 'test-secret',
        })
        payload = {'event': 'test', 'rule_id': rule.id}
        self.assertEqual(rule._signature(payload), rule._signature(payload))
        rule.test_signature()
        log = self.env['gf.webhook.log'].search([('rule_id', '=', rule.id)], limit=1)
        self.assertEqual(log.status, 'prepared')
        self.assertTrue(log.signature)
