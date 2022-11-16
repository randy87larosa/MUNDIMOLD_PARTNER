from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    #################
    subcontratado_ok = fields.Boolean(string="Puede ser subcontratado", )
    pesos_ids = fields.One2many('product.pesos', 'product_id', string="Precios")
    
    
    
    
class product_pesos(models.Model):
    _name = 'product.pesos'
    _description = "Pesos producto"
   
    product_id = fields.Many2one('product.template', string="Producto", required=True)
    supplier_id = fields.Many2one('res.partner', string="Proveedor", required=True)
    aleacion = fields.Char(string='Aleación')
    dimensiones = fields.Char(string='Dimensiones')
    precio = fields.Float(digits=(6, 2), string='Precio')
    descuento = fields.Float(digits=(6, 2), string='% Descuento')
    precio_final = fields.Float(digits=(6, 2), string='Precio final', compute='_compute_precio')
    
    @api.depends('precio', 'descuento')
    def _compute_precio(self):
        for record in self:
            precio_final = 0.0
            if record.descuento <= 0.0:
                precio_final = record.precio
            else:
                precio_final = record.precio - ((record.descuento/100)*record.precio)
            record.precio_final = precio_final