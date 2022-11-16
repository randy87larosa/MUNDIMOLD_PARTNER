# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2018 Odoo IT now <http://www.odooitnow.com/>
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, fields, api, tools
from odoo.addons.base.models.ir_mail_server import extract_rfc2822_addresses


class IrMailServer(models.Model):
    _inherit = 'ir.mail_server'

    user_id = fields.Many2one('res.users', string='Owner')

    _sql_constraints = [
        ('smtp_user_uniq', 'unique(user_id)',
         'That user already has a SMTP server.')
    ]

    @api.model
    def send_email(self, message, mail_server_id=None, smtp_server=None, smtp_port=None,
                   smtp_user=None, smtp_password=None, smtp_encryption=None, smtp_debug=False,
                   smtp_session=None):
        from_rfc2822 = extract_rfc2822_addresses(message['From'])[-1]
        server_id = self.env['ir.mail_server'].search([
            ('smtp_user', '=', from_rfc2822)])
        if server_id and server_id[0]:
            message['Return-Path'] = from_rfc2822
        return super(IrMailServer, self).send_email(message, mail_server_id, smtp_server,
                smtp_port, smtp_user, smtp_password, smtp_encryption, smtp_debug,
                smtp_session)


class MailMail(models.Model):
    _inherit = 'mail.mail'

    @api.multi
    def send(self, auto_commit=False, raise_exception=False):
        for email in self.env['mail.mail'].sudo().browse(self.ids):
            reply_to = email.email_from
            from_rfc2822 = extract_rfc2822_addresses(reply_to)[-1]
            server_id = self.env['ir.mail_server'].search([
                ('smtp_user', '=', from_rfc2822)])
            server_id = server_id and server_id[0] or False
            if server_id:
                self.write(
                    {'mail_server_id': server_id[0].id,
                     'reply_to': reply_to})
        return super(MailMail, self).send(auto_commit=auto_commit,
                                          raise_exception=raise_exception)
