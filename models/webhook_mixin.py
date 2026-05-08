import json
import urllib.error
import urllib.request
from odoo import models


class GfWebhookDispatchMixin(models.AbstractModel):
    _name = 'gf.webhook.dispatch.mixin'
    _description = 'Webhook Dispatch Mixin'

    def _gf_fire_webhooks(self, event, record, extra_payload=None):
        rules = self.env['gf.webhook.rule'].sudo().search([
            ('active', '=', True),
            ('event', '=', event),
        ])
        for rule in rules:
            payload = {
                'event': event,
                'model': record._name,
                'record_id': record.id,
                'display_name': record.display_name,
                'company_id': record.company_id.id if 'company_id' in record._fields and record.company_id else False,
            }
            if extra_payload:
                payload.update(extra_payload)
            signature = rule._signature(payload)
            log = self.env['gf.webhook.log'].sudo().create({
                'rule_id': rule.id,
                'event': event,
                'target_url': rule.target_url,
                'status': 'prepared',
                'payload': json.dumps(payload, sort_keys=True),
                'signature': signature,
            })
            self._gf_send_webhook_log(log, payload, signature)

    def _gf_send_webhook_log(self, log, payload, signature):
        body = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode('utf-8')
        req = urllib.request.Request(
            log.target_url,
            data=body,
            method='POST',
            headers={
                'Content-Type': 'application/json',
                'X-Odoo-Webhook-Signature': signature,
                'User-Agent': 'gf-mcp-webhook-hub/19.0',
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                response_body = resp.read(4096).decode('utf-8', errors='replace')
                log.sudo().write({
                    'status': 'sent' if 200 <= resp.status < 300 else 'failed',
                    'response_code': resp.status,
                    'response_body': response_body,
                })
        except urllib.error.HTTPError as exc:
            log.sudo().write({
                'status': 'failed',
                'response_code': exc.code,
                'response_body': exc.read(4096).decode('utf-8', errors='replace'),
            })
        except Exception as exc:
            log.sudo().write({
                'status': 'failed',
                'response_body': str(exc),
            })
