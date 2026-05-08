from odoo.tests.common import TransactionCase


class TestAuditLog(TransactionCase):

    def test_create_audit_entry(self):
        log = self.env['gf.mcp.audit.log'].create({
            'action': 'list_models',
            'status': 'allowed',
            'request_ip': '127.0.0.1',
        })
        self.assertEqual(log.action, 'list_models')
        self.assertEqual(log.status, 'allowed')
        self.assertFalse(log.api_key_id)

    def test_audit_with_api_key(self):
        key = self.env['gf.mcp.api.key'].create({'name': 'Audit Key'})
        log = self.env['gf.mcp.audit.log'].create({
            'api_key_id': key.id,
            'action': 'search',
            'model_name': 'res.partner',
            'status': 'allowed',
        })
        self.assertEqual(log.api_key_id.id, key.id)
        self.assertEqual(log.model_name, 'res.partner')

    def test_denied_audit_entry(self):
        log = self.env['gf.mcp.audit.log'].create({
            'action': 'read',
            'model_name': 'account.move',
            'status': 'denied',
            'message': 'Model not allowed',
        })
        self.assertEqual(log.status, 'denied')
        self.assertEqual(log.message, 'Model not allowed')
