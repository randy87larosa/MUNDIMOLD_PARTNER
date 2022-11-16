
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError




class ResCompany(models.Model):
    _inherit = 'res.company'

    #campos genericos
    color1_qweb = fields.Char(string="Color 1 qweb", )
    color2_qweb = fields.Char(string="Color 2 qweb", )
    