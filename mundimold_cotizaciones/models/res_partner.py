
from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sale_cotizacion_count = fields.Integer(compute='_compute_sale_cotizacion_count', string='Sale Cotización Count')
    sale_cotizacion_ids = fields.One2many('sale.cotizacion', 'partner_id', 'Cotizaciones')
    
    def _compute_sale_cotizacion_count(self):
        self.sale_cotizacion_count = len(self.env['sale.cotizacion'].search([('partner_id', '=', self.id),]))
        