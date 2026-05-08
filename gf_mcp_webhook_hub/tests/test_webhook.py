import json
from unittest.mock import patch, MagicMock
from odoo.tests.common import TransactionCase


class TestWebhookRule(TransactionCase):

    def _create_rule(self, event='sale_order_confirmed'):
        return self.env['gf.webhook.rule'].create({
            'name': 'Test Rule',
            'event': event,
            'target_url': 'https://example.com/hook',
            'secret': 'test-secret-abc',
        })

    def test_signature_deterministic(self):
        rule = self._create_rule()
        payload = {'a': 1, 'b': 'hello'}
        sig1 = rule._signature(payload)
        sig2 = rule._signature(payload)
        self.assertEqual(sig1, sig2)
        self.assertEqual(len(sig1), 64)  # HMAC-SHA256 hex

    def test_signature_differs_with_different_payload(self):
        rule = self._create_rule()
        sig1 = rule._signature({'a': 1})
        sig2 = rule._signature({'a': 2})
        self.assertNotEqual(sig1, sig2)

    def test_signature_differs_with_different_secret(self):
        rule1 = self._create_rule()
        rule2 = self.env['gf.webhook.rule'].create({
            'name': 'Other Rule',
            'event': 'sale_order_confirmed',
            'target_url': 'https://example.com/hook',
            'secret': 'other-secret',
        })
        payload = {'a': 1}
        self.assertNotEqual(rule1._signature(payload), rule2._signature(payload))

    def test_test_signature_creates_log(self):
        rule = self._create_rule()
        rule.test_signature()
        log = self.env['gf.webhook.log'].search([('rule_id', '=', rule.id)])
        self.assertEqual(len(log), 1)
        self.assertEqual(log.status, 'prepared')
        self.assertEqual(log.event, 'test')
        self.assertTrue(log.signature)
        self.assertTrue(log.payload)


class TestWebhookDispatch(TransactionCase):

    def _create_rule(self, event='sale_order_confirmed'):
        return self.env['gf.webhook.rule'].create({
            'name': 'Dispatch Rule',
            'event': event,
            'target_url': 'https://example.com/hook',
            'secret': 'dispatch-secret',
        })

    @patch('odoo.addons.gf_mcp_webhook_hub.models.webhook_mixin.urllib.request.urlopen')
    def test_fire_webhook_on_event(self, mock_urlopen):
        """Calling _gf_fire_webhooks creates a log and attempts HTTP delivery."""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'OK'
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        rule = self._create_rule()
        partner = self.env['res.partner'].create({'name': 'Test Partner'})
        dispatcher = self.env['gf.webhook.dispatch.mixin']
        dispatcher._gf_fire_webhooks('sale_order_confirmed', partner)

        log = self.env['gf.webhook.log'].search([('rule_id', '=', rule.id)])
        self.assertEqual(len(log), 1)
        self.assertEqual(log.status, 'sent')
        self.assertEqual(log.response_code, 200)

    @patch('odoo.addons.gf_mcp_webhook_hub.models.webhook_mixin.urllib.request.urlopen')
    def test_fire_webhook_failure_logs_error(self, mock_urlopen):
        import urllib.error
        mock_urlopen.side_effect = urllib.error.HTTPError(
            'https://example.com/hook', 500, 'Internal Server Error', {}, None
        )

        rule = self._create_rule()
        partner = self.env['res.partner'].create({'name': 'Fail Partner'})
        dispatcher = self.env['gf.webhook.dispatch.mixin']
        dispatcher._gf_fire_webhooks('sale_order_confirmed', partner)

        log = self.env['gf.webhook.log'].search([('rule_id', '=', rule.id)])
        self.assertEqual(len(log), 1)
        self.assertEqual(log.status, 'failed')
        self.assertEqual(log.response_code, 500)

    def test_no_rules_no_logs(self):
        """When no rules match, no logs should be created."""
        partner = self.env['res.partner'].create({'name': 'No Rule Partner'})
        dispatcher = self.env['gf.webhook.dispatch.mixin']
        dispatcher._gf_fire_webhooks('sale_order_confirmed', partner)
        logs = self.env['gf.webhook.log'].search([('event', '=', 'sale_order_confirmed')])
        self.assertFalse(logs)

    def test_inactive_rule_not_fired(self):
        rule = self._create_rule()
        rule.active = False
        partner = self.env['res.partner'].create({'name': 'Inactive Partner'})
        dispatcher = self.env['gf.webhook.dispatch.mixin']
        dispatcher._gf_fire_webhooks('sale_order_confirmed', partner)
        logs = self.env['gf.webhook.log'].search([('rule_id', '=', rule.id)])
        self.assertFalse(logs)
