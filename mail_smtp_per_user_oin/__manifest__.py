# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2018 Odoo IT now <http://www.odooitnow.com/>
# See LICENSE file for full copyright and licensing details.
#
##############################################################################
{
    'name': 'Mail SMTP Server Per User',
    'summary': 'Send mails from Odoo using your own mail.',

    'version': '12.0.1.0',
    'category': 'Mail',

    'description': """
Mail SMTP Server Per User
=========================
This module allows send mails from Odoo using your own mail.
""",

    'author': 'Odoo IT now',
    'website': 'http://www.odooitnow.com/',
    'license': 'Other proprietary',

    'depends': ['base', 'mail'],

    'data': [
        'views/ir_mail_server_view.xml'
    ],
    'images': ['images/OdooITnow_screenshot.png'],

    'price': 20.0,
    'currency': 'EUR',

    'installable': True,
    'auto_install': False
}
