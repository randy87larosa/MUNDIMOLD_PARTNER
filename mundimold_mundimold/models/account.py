
from odoo import fields, models, api




class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    exclude_mis = fields.Boolean(string="Excluir informes")
    
    
    
class AccountAsset(models.Model):
    _inherit = 'account.asset'

    elemento = fields.Char(string="Elemento")