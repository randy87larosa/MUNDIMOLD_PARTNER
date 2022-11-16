# -*- coding: utf-8 -*-
# Copyright (c) 2017 Emipro Technologies Pvt Ltd (www.emiprotechnologies.com). All rights reserved.

from odoo import api, fields, models

class PlaidAccountWizard(models.TransientModel):
    _name = 'account.plaid.wizard'
    _description = 'Wizard for Plaid account synchronization'
