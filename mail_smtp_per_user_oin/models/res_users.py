# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2018 Odoo IT now <http://www.odooitnow.com/>
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, fields


class ResUser(models.Model):
    _inherit = 'res.users'

    smtp_server_id = fields.One2many('ir.mail_server', 'user_id',
                                     'Email Server')
