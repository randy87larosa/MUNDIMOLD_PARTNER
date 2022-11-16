# -*- coding: utf-8 -*-
{
    'name': 'Unicoding Fixed Left and Top Pivot Columns',
    'version': "12.0.2.0.1",
    'website': 'https://www.unicoding.by',
    'summary': 'Fixed Left and top Pivot Columns(Sticky). For Odoo Enterprise & Community.',
    'description': "Fixed Left and top Pivot Columns(Sticky). For Odoo Enterprise & Community",
    "author": "Unicoding.by",
    "license": "OPL-1",
    "support": "info@unicoding.by",
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
    ],
    "depends": ['web', 'base_setup'],
    "sequence": 7,
    "category": "Productivity",
    'data': [
        'views/res_config_settings_views.xml',
        'views/webclient_templates.xml',        
    ],
    'qweb': [
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 19.99,
    'currency': 'EUR'
}
