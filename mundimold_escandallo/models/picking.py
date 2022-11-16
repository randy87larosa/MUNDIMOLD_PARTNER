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



class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    product_subco_id = fields.Many2one('product.template', string="Operación subcontratación")
    
    @api.multi
    def add_operacion_subco(self): 
        for record in self:
            if record.state == "draft":
        
                if record.project_id and record.product_subco_id:
            
                    for subco in self.env['project.escandallo.subcontratista'].search([('project_id', '=', record.project_id.id), 
                                                                          ('product_id', '=', record.product_subco_id.id)]):
                                                                          
                        line_id = self.env['stock.move'].create({'picking_id': record.id, 
                                                                  'product_id': subco.escandallo_id.product_id.product_variant_id.id, 
                                                                  'cod_pieza': subco.escandallo_id.cod_pieza,
                                                                  'aleacion': subco.escandallo_id.aleacion,
                                                                  'dimensiones': subco.escandallo_id.dimensiones,
                                                                  'product_uom_qty': subco.escandallo_id.quantity,
                                                                  'name': subco.escandallo_id.product_id.name,
                                                                  'product_uom': subco.escandallo_id.product_id.uom_id.id,
                                                                  'location_id': record.location_id.id,
                                                                  'location_dest_id': record.location_dest_id.id,

                                                                 })
                                                             
    @api.multi
    def add_all_qty(self):
        for record in self:
            if record.state != "done" and record.state != "cancel":
                for line in record.move_ids_without_package:
                    line.quantity_done = line.product_uom_qty
                    
    
    

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    dimensiones = fields.Char(string='Dimensiones', compute='_get_datos_escandallo')
    aleacion = fields.Char(string='Aleación', compute='_get_datos_escandallo')
    cod_pieza = fields.Char(string="Cod", compute='_get_datos_escandallo')
    
    escandallo_id = fields.Many2one('project.escandallo', string="Pieza")
    related_project_id = fields.Many2one('project.project', string="Proyecto relacionado", related='picking_id.project_id', store=True)
    
    @api.onchange('escandallo_id')
    def _onchange_escandallo_id(self):
        if self.escandallo_id:
            self.product_id = self.escandallo_id.product_id.product_variant_id.id
            self.product_uom_qty = self.escandallo_id.quantity
    
    @api.depends('purchase_line_id')
    def _get_datos_escandallo(self):
        for record in self:
            dimensiones = ''
            aleacion = ''
            cod_pieza = ''
            
            if record.purchase_line_id:
                dimensiones = record.purchase_line_id.dimensiones
                aleacion = record.purchase_line_id.aleacion
                cod_pieza = record.purchase_line_id.cod_pieza
                
            elif record.escandallo_id:
                dimensiones = record.escandallo_id.dimensiones
                aleacion = record.escandallo_id.aleacion
                cod_pieza = record.escandallo_id.cod_pieza
            
            record.dimensiones = dimensiones
            record.aleacion = aleacion
            record.cod_pieza = cod_pieza
    
    
    

        



