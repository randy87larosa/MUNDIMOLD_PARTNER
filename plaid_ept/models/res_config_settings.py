# -*- coding: utf-8 -*-
# Copyright (c) 2017 Emipro Technologies Pvt Ltd (www.emiprotechnologies.com). All rights reserved.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sync_with_plaid = fields.Boolean('Automatic Import with Plaid')
    plaid_client_id = fields.Char(string='Plaid Client ID')
    plaid_secret = fields.Char(string='Plaid Secret')
    plaid_public_key = fields.Char(string='Plaid Public Key')
    plaid_env = fields.Selection([
        ('sandbox', 'SandBox'),
        ('development', 'Development'),
        ('production', 'Production')], string="Plaid Environment")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            sync_with_plaid=bool(get_param('sync_with_plaid')),
            plaid_client_id=get_param('plaid_client_id'),
            plaid_secret=get_param('plaid_secret'),
            plaid_public_key=get_param('plaid_public_key'),
            plaid_env=get_param('plaid_env'),
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('sync_with_plaid', (self.sync_with_plaid or False))
        set_param('plaid_client_id', (self.plaid_client_id or '').strip())
        set_param('plaid_secret', (self.plaid_secret or '').strip())
        set_param('plaid_public_key', (self.plaid_public_key or '').strip())
        set_param('plaid_env', (self.plaid_env or ''))
