from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    contacto_id = fields.Many2one('res.partner', string='Contacto',)
    summary_sale = fields.Char(string='Título presupuesto',)
