
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp
from datetime import datetime


class sale_aps_template(models.Model):
    _name = 'sale.aps.template'
    
    name = fields.Char(string='Título', required=True)
    line_ids = fields.One2many('sale.aps.template.line', 'template_id', string="Líneas")
    
    
class sale_aps_template_line(models.Model):
    _name = 'sale.aps.template.line'
    
    name = fields.Char(string='Título', required=True)
    template_id = fields.Many2one('sale.aps.template', string="Plantilla")
    product_id = fields.Many2one('product.template', string="Producto")
    
    
class sale_aps_horas(models.Model):
    _name = 'sale.aps.horas'
    
    name = fields.Char(string='Título', required=True)
    num_horas = fields.Integer(string='Num horas')
    precio_hora = fields.Float(string='Precio hora')
    

    
class sale_aps(models.Model):
    _name = 'sale.aps'

   
    
    partner_id = fields.Many2one('res.partner', string="Cliente", required=True)
    date = fields.Date('Fecha', default=fields.Date.today(), required=True)
    mostrar_detalles = fields.Boolean('Detallar presupuesto')
    
    hora_id = fields.Many2one('sale.aps.horas', string="Tipo de hora")
    user_id = fields.Many2one('res.users', string="Comercial", default=lambda self: self.env.user, required=True)
    
    opportunity_id = fields.Many2one('sale.aps.horas', string="Oportunidad")
    sale_id = fields.Many2one('sale.order', string="Presupuesto/pedido")
    
    observaciones = fields.Text('Notas internas')
    
    ETAPAS = [('BOR','BORRADOR'),   
              ('GEN','GENERADO'),
             ]
    state = fields.Selection(selection=ETAPAS, string='Estado', default='BOR', track_visibility='onchange')
    
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('sale.cotizacion'))
    
    line_ids = fields.One2many('sale.aps.line', 'aps_id', string="Líneas")
    
    precio_total = fields.Float(compute='_compute_precio', string='Precio')
    horas_total = fields.Float(compute='_compute_precio', string='Horas')
    
    
    @api.depends('line_ids', 'hora_id')
    def _compute_precio(self):
        for record in self:
            precio_total = 0.0
            horas_total = 0.0
            
            precio_hora = 55
            if record.hora_id:
                precio_hora = record.hora_id.precio_hora
            for line in record.line_ids:
                precio_total = precio_total + line.precio_materiales + line.precio_subcontratacion + (line.num_horas * precio_hora)
                horas_total = horas_total + line.num_horas
            
            record.horas_total = horas_total
            record.precio_total = precio_total
        
    @api.multi
    def bor_to_gen(self):
        for record in self:
            if not record.sale_id:
            
                
            
                precio_hora = 55
                if record.hora_id:
                    precio_hora = record.hora_id.precio_hora
            
                sale_id = self.env['sale.order'].create({'partner_id': record.partner_id.id, 
                                                          'date_order': datetime.now(), 
                                                         })
                if record.mostrar_detalles == True:
                    for line in record.line_ids:
                    
                        product_id = None
                        uom_id = 1
                        if line.actividad_id.product_id:
                            product_id = line.actividad_id.product_id.product_variant_id.id
                            uom_id = line.actividad_id.product_id.uom_id.id
                            
                        precio_total = line.precio_materiales + line.precio_subcontratacion + (line.num_horas * precio_hora)
                    
                        line_id = self.env['sale.order.line'].create({'order_id': sale_id.id, 
                                                                           'name': line.actividad_id.name, 
                                                                           'product_uom_qty': 1,
                                                                           'customer_lead': 1,
                                                                           'price_unit': precio_total,
                                                                           'product_uom': uom_id,
                                                                           'product_id': product_id,
                                                                           
                                                                          })
                        line_id._compute_tax_id()
                        
                else:
                
                    lista_areas = []
                    for line in record.line_ids:
                    
                        if line.area_id.id not in lista_areas:
                            lista_areas.append(line.area_id.id)
                            product_id = None
                            uom_id = 1
                            if line.actividad_id.product_id:
                                product_id = line.actividad_id.product_id.product_variant_id.id
                                uom_id = line.actividad_id.product_id.uom_id.id
                                
                                
                            #sumamos precios
                            precio_total = 0.0
                            for precio in record.line_ids:
                                if precio.area_id.id == line.area_id.id:
                                    precio_total = precio_total + precio.precio_materiales + precio.precio_subcontratacion + (precio.num_horas * precio_hora)
                        
                            line_id = self.env['sale.order.line'].create({'order_id': sale_id.id, 
                                                                               'name': line.actividad_id.name, 
                                                                               'product_uom_qty': 1,
                                                                               'customer_lead': 1,
                                                                               'price_unit': precio_total,
                                                                               'product_uom': uom_id,
                                                                               'product_id': product_id,
                                                                               
                                                                              })
                            line_id._compute_tax_id()
            
            
                record.sale_id = sale_id.id
            self.state = 'GEN'
        
    @api.multi
    def gen_to_bor(self):
        
        self.state = 'BOR'
        
    
    
    
    
class sale_aps_line(models.Model):
    _name = 'sale.aps.line'
    
    sequence = fields.Integer('Secuencia')
    aps_id = fields.Many2one('sale.aps', string="Presupuesto", required=True, readonly=True, ondelete='cascade')
    area_id = fields.Many2one('sale.aps.template', string="Área", required=True)
    actividad_id = fields.Many2one('sale.aps.template.line', string="Actividad", required=True)
    precio_materiales = fields.Float(string='Precio materiales')
    precio_subcontratacion = fields.Float(string='Precio subcontratación')
    num_horas = fields.Float(string='Num horas')
    


class WizardApsLine(models.TransientModel):
    _name = 'wizard.aps.line'
    

    def _default_sale_aps(self):
        return self.env['sale.aps'].browse(self._context.get('active_id'))


    aps_id = fields.Many2one('sale.aps', string='Presupuesto', default=_default_sale_aps, required=True)
    area_id = fields.Many2one('sale.aps.template', string="Área", required=True)
    actividad_id = fields.Many2one('sale.aps.template.line', string="Actividad", required=True)
    precio_materiales = fields.Float(string='Precio materiales')
    precio_subcontratacion = fields.Float(string='Precio subcontratación')
    num_horas = fields.Float(string='Num horas')
    
    
    


    @api.multi
    def create_line(self): 
        for record in self:
            self.env['sale.aps.line'].create({'aps_id': record.aps_id.id, 
                                              'area_id': record.area_id.id, 
                                              'actividad_id': record.actividad_id.id, 
                                              'precio_materiales': record.precio_materiales,
                                              'precio_subcontratacion': record.precio_subcontratacion,
                                              'num_horas': record.num_horas,
                                             })
    
    
