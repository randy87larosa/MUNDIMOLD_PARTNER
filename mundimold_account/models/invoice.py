
from odoo import fields, models, api




class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    no_print_project = fields.Boolean(string="No imprimir proyecto", default=False)
    
