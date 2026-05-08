from odoo.tests.common import TransactionCase


class TestApiKey(TransactionCase):

    def test_create_generates_hash_and_preview(self):
        model = self.env['ir.model'].search([('model', '=', 'res.partner')], limit=1)
        key = self.env['gf.mcp.api.key'].create({
            'name': 'Test Key',
            'allowed_model_ids': [(6, 0, model.ids)],
        })
        self.assertTrue(key.key_hash)
        self.assertIn('…', key.key_preview)
        self.assertEqual(len(key.key_hash), 64)  # sha256 hex

    def test_authenticate_valid_token(self):
        model = self.env['ir.model'].search([('model', '=', 'res.partner')], limit=1)
        key = self.env['gf.mcp.api.key'].create({
            'name': 'Auth Test',
            'allowed_model_ids': [(6, 0, model.ids)],
        })
        # We need to get the plain token; re-derive from the hash is not possible.
        # Instead, we hash a known token and set it manually.
        import secrets
        token = secrets.token_urlsafe(32)
        key_hash = self.env['gf.mcp.api.key']._hash_token(token)
        key.write({'key_hash': key_hash})

        found = self.env['gf.mcp.api.key'].authenticate_token(token)
        self.assertEqual(found.id, key.id)

    def test_authenticate_invalid_token(self):
        result = self.env['gf.mcp.api.key'].authenticate_token('garbage-token-999')
        self.assertFalse(result)

    def test_authenticate_none(self):
        result = self.env['gf.mcp.api.key'].authenticate_token(None)
        self.assertFalse(result)

    def test_is_model_allowed(self):
        partner_model = self.env['ir.model'].search([('model', '=', 'res.partner')], limit=1)
        user_model = self.env['ir.model'].search([('model', '=', 'res.users')], limit=1)
        key = self.env['gf.mcp.api.key'].create({
            'name': 'Scope Test',
            'allowed_model_ids': [(6, 0, partner_model.ids)],
        })
        self.assertTrue(key.is_model_allowed('res.partner'))
        self.assertFalse(key.is_model_allowed('res.users'))

    def test_inactive_key_not_found(self):
        import secrets
        token = secrets.token_urlsafe(32)
        key_hash = self.env['gf.mcp.api.key']._hash_token(token)
        key = self.env['gf.mcp.api.key'].create({
            'name': 'Inactive',
            'key_hash': key_hash,
            'active': False,
        })
        found = self.env['gf.mcp.api.key'].authenticate_token(token)
        self.assertFalse(found)
