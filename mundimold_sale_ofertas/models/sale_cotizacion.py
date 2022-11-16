
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

    
class sale_order(models.Model):
    _inherit = 'sale.order'


    plazo_entrega = fields.Char(string='Plazo de entrega')
    
    
    is_proforma = fields.Boolean(string='¿Proforma?')
    
    oferta_extensa = fields.Boolean(string='¿Oferta extensa?')
    
    category_mold_id = fields.Many2one('product.moldrent.category', string="Categoría Molde",)
    subcategory_mold_id = fields.Many2one('product.moldrent.category', string="Subcategoría Molde",)
    
    description = fields.Char(string='Denominación artículo')
    atencion = fields.Char(string='Att')
    validez = fields.Char(string='Validez')
    cargar_platilla = fields.Char(string='Plantilla', default="PLANTILLA")
    plantilla_id = fields.Many2one('sale.order', string="Plantilla a cargar")
    observaciones = fields.Text('Notas internas')
    
    
    a1 = fields.Html("Especificaciones artículo")
    
    b1 = fields.Html("Cotización")
    
    c1 = fields.Html("Características generales")
    
    line_oferta_ids = fields.One2many('sale.order.oferta.line', 'sale_id', string="Líneas oferta", copy=True)
    
    
    c2 = fields.Html("Forma y plazo de pago")
    c3 = fields.Html("Prueba del molde")
    c4 = fields.Html("Fases del proyecto")
    c5 = fields.Html("Ciclos de producción")
    c6 = fields.Html("Envío de muestras")
    c7 = fields.Html("Envío de calidad de las muestras")
    c8 = fields.Html("Documentación e instrucciones")
    c9 = fields.Html("Garantías")
    c10 = fields.Html("Confidencialidad")
    c11 = fields.Html("Contactos")
    c12 = fields.Html("Texto legal")
    
    
    total_oferta_extensa = fields.Float(string="Subtotal oferta", readonly=True, compute="_get_total_oferta", store=True)
    
    producto_lineas = fields.Char(string="Productos", readonly=True, compute="_get_productos")
    
    @api.depends('order_line','order_line.product_id')
    def _get_productos(self):
        for record in self:
            listado_productos = []
            for line in record.order_line:
                if line.product_id:
                    listado_productos.append(line.product_id.name)
                    
            listado_productos = list(set(listado_productos))
            
            record.producto_lineas = ', '.join(listado_productos)
    
    @api.depends('line_oferta_ids','line_oferta_ids.precio')
    def _get_total_oferta(self):
        for record in self:
            total = 0.0
            for line in record.line_oferta_ids:
                total = total + line.precio
                
            if total <= 0.0:
                total = record.amount_untaxed
            record.total_oferta_extensa = total
    
    @api.multi
    def action_load_template(self):
        for record in self:
            if record.plantilla_id:
                #plantillas = self.env['sale.order'].search([('description', '=', record.cargar_platilla)])
                #if len(plantillas) <= 0:
                #    plantillas = self.env['sale.order'].search([('name', '=', record.cargar_platilla)])
                    
                #if len(plantillas) <= 0:
                #    raise ValidationError("Error: No se ha encontrado la cotización indicada en la plantilla")
                
                pl = record.plantilla_id
                if record.a1 == None or record.a1 == '' or record.a1 == '<p><br></p>':
                    record.a1 = pl.a1
                if record.b1 == None or record.b1 == '' or record.b1 == '<p><br></p>':
                    record.b1 = pl.b1
                if record.c1 == None or record.c1 == '' or record.c1 == '<p><br></p>':
                    record.c1 = pl.c1
                if record.c2 == None or record.c2 == '' or record.c2 == '<p><br></p>':
                    record.c2 = pl.c2
                if record.c3 == None or record.c3 == '' or record.c3 == '<p><br></p>':
                    record.c3 = pl.c3
                if record.c4 == None or record.c4 == '' or record.c4 == '<p><br></p>':
                    record.c4 = pl.c4
                if record.c5 == None or record.c5 == '' or record.c5 == '<p><br></p>':
                    record.c5 = pl.c5
                if record.c6 == None or record.c6 == '' or record.c6 == '<p><br></p>':
                    record.c6 = pl.c6
                if record.c7 == None or record.c7 == '' or record.c7 == '<p><br></p>':
                    record.c7 = pl.c7
                if record.c8 == None or record.c8 == '' or record.c8 == '<p><br></p>':
                    record.c8 = pl.c8
                if record.c9 == None or record.c9 == '' or record.c9 == '<p><br></p>':
                    record.c9 = pl.c9
                if record.c10 == None or record.c10 == '' or record.c10 == '<p><br></p>':
                    record.c10 = pl.c10
                if record.c11 == None or record.c11 == '' or record.c11 == '<p><br></p>':
                    record.c11 = pl.c11
                if record.c12 == None or record.c12 == '' or record.c12 == '<p><br></p>':
                    record.c12 = pl.c12
                
                if len(record.line_oferta_ids) <= 0:
                    for line in pl.line_oferta_ids:
                        prod_id = None
                        if line.product_id:
                            prod_id = line.product_id.id
                        self.env['sale.order.oferta.line'].create({'sequence': line.sequence, 
                                                                  'sale_id': record.id, 
                                                                  'product_id': prod_id, 
                                                                  'name': line.name,
                                                                  'precio': line.precio,
                                                                  'ciclo_produccion': line.ciclo_produccion,
                                                                  'plazo_entrega': line.plazo_entrega,
                                                                 })
                    
    
    
    

        

    
    
    
    
    
class sale_order_oferta_line(models.Model):
    _name = 'sale.order.oferta.line'
    
    sequence = fields.Integer('Secuencia')
    sale_id = fields.Many2one('sale.order', string="Presupuesto", required=True, readonly=True, ondelete='cascade')
    sale_line_id = fields.Many2one('sale.order.line', string="Línea pedido", readonly=True)
    product_id = fields.Many2one('product.template', string="Producto")
    name = fields.Char('Concepto')
    precio = fields.Float('Precio', digits = (12,2))
    ciclo_produccion = fields.Char('Ciclo producción (segundos)')
    plazo_entrega = fields.Char('Plazo entrega (semanas)')
    
    
    @api.multi
    def action_create_line(self):
        for record in self:
            if not record.sale_line_id:
            
                if not record.product_id:
                    raise ValidationError("Error: Es necesario indicar un producto para crear la línea de pedido")
                else:
                    #creamos linea
                    line_id = self.env['sale.order.line'].create({'order_id': record.sale_id.id, 
                                                                   'name': record.name, 
                                                                   'product_uom_qty': 1.0,
                                                                   'product_qty': 1.0,
                                                                   'price_unit': record.precio,
                                                                   'product_uom': record.product_id.uom_id.id,
                                                                   'product_id': record.product_id.product_variant_id.id
                                                                  })
                    line_id._compute_tax_id()
                    record.sale_line_id = line_id.id
    
    
    
    
    
    
    
    
