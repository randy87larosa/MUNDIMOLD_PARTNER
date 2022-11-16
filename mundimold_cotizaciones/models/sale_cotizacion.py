
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

    
class sale_cotizacion(models.Model):
    _name = 'sale.cotizacion'

    name = fields.Char(string='Cotización', required=True, copy=False, readonly=True, index=True, default=lambda self: "/")
    
    description = fields.Char(string='Denominación artículo', required=True)
    partner_id = fields.Many2one('res.partner', string="Cliente", required=True)
    opportunity_id = fields.Many2one('crm.lead', string="Oportunidad")
    atencion = fields.Char(string='Att', required=True )
    date = fields.Date('Fecha', default=fields.Date.today(), required=True)
    user_id = fields.Many2one('res.users', string="Comercial", default=lambda self: self.env.user, required=True)
    validez = fields.Char(string='Validez', required=True )
    cargar_platilla = fields.Char(string='Plantilla', default="PLANTILLA")
    
    observaciones = fields.Text('Notas internas')
    
    ETAPAS = [('ESP','EN ESPERA'),   
              ('ACE','ACEPTADO'),
              ('REC','RECHAZADO'),
             ]
    state = fields.Selection(selection=ETAPAS, string='Estado', default='ESP', track_visibility='onchange')
    
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('sale.cotizacion'))
    
    a1 = fields.Html("Especificaciones artículo")
    
    
    
    b1 = fields.Html("Cotización")
    
    c1 = fields.Html("Características generales")
    
    line_ids = fields.One2many('sale.cotizacion.line', 'cotizacion_id', string="Líneas")
    
    
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
    
    @api.multi
    def action_load_template(self):
        for record in self:
            if record.cargar_platilla:
                plantillas = self.env['sale.cotizacion'].search([('description', '=', record.cargar_platilla)])
                if len(plantillas) <= 0:
                    plantillas = self.env['sale.cotizacion'].search([('description', '=', record.name)])
                    
                if len(plantillas) <= 0:
                    raise ValidationError("Error: No se ha encontrado la cotización indicada en la plantilla")
                else:
                    pl = plantillas[0]
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
                    
                    if len(record.line_ids) <= 0:
                        for line in pl.line_ids:
                            prod_id = None
                            if line.product_id:
                                prod_id = line.product_id.id
                            self.env['sale.cotizacion.line'].create({'sequence': line.sequence, 
                                                                      'cotizacion_id': record.id, 
                                                                      'product_id': prod_id, 
                                                                      'name': line.name,
                                                                      'precio': line.precio,
                                                                      'ciclo_produccion': line.ciclo_produccion,
                                                                      'plazo_entrega': line.plazo_entrega,
                                                                     })
                    
    
    
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sale.cotizacion'
                )
        return super().create(vals_list)
        
        
    @api.multi
    def esp_to_ace(self):
        self.state = 'ACE'
        
    @api.multi
    def esp_to_rec(self):
        self.state = 'REC'
        
    @api.multi
    def ace_to_esp(self):
        self.state = 'ESP'
        
    @api.multi
    def rec_to_esp(self):
        self.state = 'ESP'

    
    
    
    
    
class sale_presupuesto_line(models.Model):
    _name = 'sale.cotizacion.line'
    
    sequence = fields.Integer('Secuencia')
    cotizacion_id = fields.Many2one('sale.cotizacion', string="Presupuesto", required=True, readonly=True, ondelete='cascade')
    product_id = fields.Many2one('product.template', string="Producto")
    name = fields.Char('Concepto')
    precio = fields.Float('Precio', digits = (12,2))
    ciclo_produccion = fields.Char('Ciclo producción (segundos)')
    plazo_entrega = fields.Char('Plazo entrega (semanas)')
    
    
    
    
    
    
    
    
