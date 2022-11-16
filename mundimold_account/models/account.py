
from odoo import fields, models, api




class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    partner_vat = fields.Char(string="NIF", related="partner_id.vat")
    
    bank_account_number = fields.Char(compute='_compute_bank_account', string='Cuenta bancaria')
    
    @api.depends('partner_id', 'partner_id.bank_ids')
    def _compute_bank_account(self):
        for record in self:
            banknum = ''
            if record.partner_id:
                for bank in record.partner_id.bank_ids:
                    banknum = bank.acc_number
                    break
            record.bank_account_number = banknum
    