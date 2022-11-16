# -*- coding: utf-8 -*-
# © 2009 NetAndCo (<http://www.netandco.net>).
# © 2011 Akretion Benoît Guillot <benoit.guillot@akretion.com>
# © 2014 prisnet.ch Seraphine Lantible <s.lantible@gmail.com>
# © 2016 Serpent Consulting Services Pvt. Ltd.
# © 2018 Daniel Campos <danielcampos@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
import datetime
from odoo.exceptions import UserError, ValidationError



        
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    escandallo_ids = fields.One2many('project.escandallo', 'purchase_id', string="Escandallo")
    subcontratista_ids = fields.One2many('project.escandallo.subcontratista', 'purchase_id', string="Subcontratista")
    
    fecha_entrega = fields.Date(string='Fecha de entrega', compute='_get_fecha_entrega')
    fecha_factura = fields.Date(string='Fecha de factura', compute='_get_fecha_factura')
    
    
    no_es_pieza = fields.Boolean(string='No es pieza', default=False)
    
    
    @api.depends('picking_ids', 'picking_ids.state')
    def _get_fecha_entrega(self):
        for record in self:
            fecha_entrega = None
            for pick in record.picking_ids:
                if pick.state == 'done':
                    if pick.date_done:
                        fecha_entrega = pick.date_done.date()
            record.fecha_entrega = fecha_entrega
            
            
    @api.depends('invoice_ids', 'invoice_ids.state')
    def _get_fecha_factura(self):
        for record in self:
            fecha_factura = None
            for invoice in record.invoice_ids:
                fecha_factura = invoice.date_invoice
            record.fecha_factura = fecha_factura
            
            
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    dimensiones = fields.Char(string='Dimensiones')
    aleacion = fields.Char(string='Aleación')
    entregar_a_id = fields.Many2one('res.partner', string="Entrega a")
    cuadreado = fields.Boolean(string='Cuadreado')
    cod_pieza = fields.Char(string="Cod", default="000")
    peso = fields.Float(digits=(6, 2), string='Peso (kg)')
    



class WizardPurchaseAddPieza(models.TransientModel):
    _name = 'wizard.purchase.add.pieza'
    

    def _default_purchase(self):
        return self.env['project.escandallo'].browse(self._context.get('active_id'))


    purchase_id = fields.Many2one('purchase.order', string='Pedido', default=_default_purchase, required=True, readonly=True)
    project_id = fields.Many2one('project.project', string='Proyecto', required=True)
    escandallo_id = fields.Many2one('project.escandallo', string='Escandallo', required=True)
    fecha_prevista = fields.Date(string='Fecha prevista')
    entregar_a_id = fields.Many2one('res.partner', string="Entrega a")

    
    
    @api.multi
    def add_line_wizard(self): 
        for record in self:
        
            if record.purchase_id.state == 'purchase' or record.purchase_id.state == 'done' or record.purchase_id.state == 'cancel':
                raise UserError('Error: el pedido debe estar en estado borrador para añadir líneas')
                
            if record.escandallo_id.purchase_id:
                raise UserError('Error: La pieza de escandallo seleccionada ya tiene un pedido confirmado')

            description_prod = record.escandallo_id.product_id.name
            #if elem.dimensiones:
            #    description_prod = description_prod + '\n' + 'Dimensiones: ' + elem.dimensiones
            #if elem.aleacion:
            #    description_prod = description_prod + '\n' + 'Aleación: ' + elem.aleacion
                
            date_planned = fields.Date.today()
            if record.fecha_prevista:
                date_planned = record.fecha_prevista
                
            entregar_a_id = None
            if record.entregar_a_id:
                entregar_a_id = record.entregar_a_id.id
        
            line_id = self.env['purchase.order.line'].create({'order_id': record.purchase_id.id, 
                                                               'name': description_prod, 
                                                               'cod_pieza': record.escandallo_id.cod_pieza, 
                                                               'product_uom_qty': record.escandallo_id.quantity,
                                                               'product_qty': record.escandallo_id.quantity,
                                                               'price_unit': 0.0,
                                                               'date_planned': date_planned,
                                                               'product_uom': record.escandallo_id.product_id.uom_id.id,
                                                               'product_id': record.escandallo_id.product_id.product_variant_id.id,
                                                               'escandallo_id': record.escandallo_id.id,
                                                               'dimensiones': record.escandallo_id.dimensiones,
                                                               'aleacion': record.escandallo_id.aleacion,
                                                               'peso': record.escandallo_id.peso,
                                                               'entregar_a_id': entregar_a_id,
                                                               'cuadreado': record.escandallo_id.cuadreado,
                                                               'account_analytic_id': record.escandallo_id.project_id.analytic_account_id.id,
                                                              })
            line_id._compute_tax_id()