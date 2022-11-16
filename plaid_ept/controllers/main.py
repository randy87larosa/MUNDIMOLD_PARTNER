# -*- coding: utf-8 -*-
# Copyright (c) 2017 Emipro Technologies Pvt Ltd (www.emiprotechnologies.com). All rights reserved.
import json
from .. import plaid
import werkzeug
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
from odoo import _
import logging

_logger = logging.getLogger(__name__)


class PlaidEPT(http.Controller):

    @http.route('/plaid/authentication', type='http', auth="public", website=True)
    def plaid_authentication(self):
        ICP_obj = request.env['ir.config_parameter'].sudo()
        PLAID_PUBLIC_KEY = ICP_obj.get_param('plaid_public_key') or ''
        PLAID_ENV = ICP_obj.get_param('plaid_env') or ''
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        webhook_url = werkzeug.urls.url_join(base_url, "plaid/webhook")
        # https://requestb.in/1eqqyqz1
        values = {
            'plaid_public_key': PLAID_PUBLIC_KEY,
            'plaid_environment': PLAID_ENV,
            'webhook_url': webhook_url,
        }
        _logger.info('plaid_authentication values: {}'.format(values))
        return request.render('plaid_ept.plaid_template_ept', values)

    @http.route("/get_plaid_access_token", methods=['POST'], auth="public", csrf=False)
    def get_access_token(self, **post):
        if post.get('accounts[1][id]'):
            return False
        plaid_account_obj = request.env['plaid.bank.account'].sudo()
        plaid_account_obj.create_or_update_plaid_account(post)
        return werkzeug.utils.redirect('/', code=301)

    @http.route('/plaid/reauthentication', type='http', auth="public", website=True)
    def plaid_reauthentication(self, **kwargs):
        try:
            ICP_obj = request.env['ir.config_parameter'].sudo()
            PLAID_PUBLIC_KEY = ICP_obj.get_param('plaid_public_key') or ''
            PLAID_ENV = ICP_obj.get_param('plaid_env') or ''
            values = {
                'plaid_public_key': PLAID_PUBLIC_KEY,
                'plaid_environment': PLAID_ENV,
            }
            plaid_account_id = kwargs.get('plaid_acc', False)
            if plaid_account_id:
                plaid_account_obj = request.env['plaid.bank.account'].sudo()
                plaid_account = plaid_account_obj.search([('id', '=', int(plaid_account_id))])
                client = plaid_account_obj._get_plaid_client_obj()
                response = client.Item.public_token.create(plaid_account.access_token)
                public_token = response.get('public_token', False)
                if public_token:
                    values.update({'generated_public_token': public_token})

            _logger.info('values of Plaid Reauthentication: {}'.format(values))
            return request.render('plaid_ept.plaid_template_update_credentials_ept', values)
        except plaid.errors.PlaidError as e:
            _logger.error('an error from Palid Reauthentication: {}'.format(e.code, str(e)))
            raise ValidationError(_('{} , {}'.format(e.code, str(e))))

    @http.route('/plaid/webhook', type='json', auth="none", csrf=False)
    def plaid_webhook_notification(self, **kwargs):
        code = request.jsonrequest.get('webhook_code', False)
        item = request.jsonrequest.get('item_id', False)
        # item = kwargs.get('item_id', False)
        if item and code and code == 'ITEM_LOGIN_REQUIRED':
            plaid_account_obj = request.env['plaid.bank.account'].sudo()
            plaid_account = plaid_account_obj.search([('item_id', '=', item)])
            if plaid_account:
                plaid_account.write({'update_credentials_required': True})
