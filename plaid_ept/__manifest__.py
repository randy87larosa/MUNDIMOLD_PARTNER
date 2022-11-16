# -*- coding: utf-8 -*-
# Copyright (c) 2017 Emipro Technologies Pvt Ltd (www.emiprotechnologies.com). All rights reserved.
{
    
     # App information
    'name': 'Online Bank Synchronization using Plaid',
    'category': 'Accounting',
    'version': '12.0',
    'summary': 'Using this App you can sync your bank feeds with Odoo using Plaid.com.',
    'license': 'OPL-1',
	
	 # Author

    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'http://www.emiprotechnologies.com',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',
	
    # Dependencies

    'depends': ['account'],
    
    # Views
    'data': [
        'security/ir.model.access.csv',
        'view/plaid_templates.xml',
        'view/assets.xml',
        'view/plaid_bank_account_view.xml',
        'view/account_journal.xml',
        'view/res_config_settings_view.xml',
        'wizard/account_plaid_wizard.xml',
        'data/ir_cron.xml',
    ],
    
   'demo': [],
   
   # Odoo Store Specific
	'images': ['static/description/Online-Bank-Synchronization-using-Plaid.jpg'],
    'live_test_url': 'https://www.emiprotechnologies.com/free-trial?app=plaid-ept&version=12&edition=enterprise',
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': '299',
    'currency': 'EUR',
}

