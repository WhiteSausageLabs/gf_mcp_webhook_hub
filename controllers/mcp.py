from odoo import http, fields
from odoo.http import request


class GfMcpController(http.Controller):

    def _token_from_request(self):
        auth = request.httprequest.headers.get('Authorization', '')
        if auth.lower().startswith('bearer '):
            return auth.split(' ', 1)[1].strip()
        return request.httprequest.args.get('api_key')

    def _json(self, payload, status=200):
        return request.make_json_response(payload, status=status)

    def _audit(self, api_key, action, model_name=None, status='allowed', message=None, record_id=None):
        request.env['gf.mcp.audit.log'].sudo().create({
            'api_key_id': api_key.id if api_key else False,
            'action': action,
            'model_name': model_name,
            'record_id': record_id or 0,
            'status': status,
            'message': message,
            'request_ip': request.httprequest.remote_addr,
        })
        # Keep denied/error audit entries even if later request handling fails.
        request.env.cr.commit()

    @http.route('/gf_mcp_webhook_hub/mcp', type='http', auth='none', methods=['POST'], csrf=False)
    def mcp_endpoint(self, **kwargs):
        token = self._token_from_request()
        api_key = request.env['gf.mcp.api.key'].sudo().authenticate_token(token)
        if not api_key:
            self._audit(False, 'authenticate', status='denied', message='Invalid or missing API key')
            return self._json({'error': 'unauthorized'}, status=401)

        api_key.sudo().write({'last_used_at': fields.Datetime.now()})
        payload = request.get_json_data(silent=True) or {}
        action = payload.get('action') or 'list_models'
        model_name = payload.get('model')

        try:
            if action == 'list_models':
                self._audit(api_key, action)
                return self._json({'models': api_key.allowed_model_ids.mapped('model')})

            if not model_name or not api_key.is_model_allowed(model_name):
                self._audit(api_key, action, model_name, 'denied', 'Model not allowed')
                return self._json({'error': 'model_not_allowed'}, status=403)

            model = request.env[model_name].sudo()

            if action == 'search':
                domain = payload.get('domain') or []
                limit = min(int(payload.get('limit') or 10), 50)
                ids = model.search(domain, limit=limit).ids
                self._audit(api_key, action, model_name)
                return self._json({'ids': ids})

            if action == 'read':
                ids = payload.get('ids') or []
                fields_list = payload.get('fields') or ['display_name']
                records = model.browse(ids).exists().read(fields_list)
                self._audit(api_key, action, model_name)
                return self._json({'records': records})

            if action == 'count':
                domain = payload.get('domain') or []
                count = model.search_count(domain)
                self._audit(api_key, action, model_name)
                return self._json({'count': count})

            self._audit(api_key, action, model_name, 'denied', 'Unsupported action')
            return self._json({'error': 'unsupported_action'}, status=400)
        except Exception as exc:
            self._audit(api_key, action, model_name, 'error', str(exc))
            return self._json({'error': 'server_error', 'message': str(exc)}, status=500)
