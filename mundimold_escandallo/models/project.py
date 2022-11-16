# -*- coding: utf-8 -*-
# © 2009 NetAndCo (<http://www.netandco.net>).
# © 2011 Akretion Benoît Guillot <benoit.guillot@akretion.com>
# © 2014 prisnet.ch Seraphine Lantible <s.lantible@gmail.com>
# © 2016 Serpent Consulting Services Pvt. Ltd.
# © 2018 Daniel Campos <danielcampos@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo.exceptions import UserError, ValidationError

        
class project_project(models.Model):
    _name = 'project.project'
    _inherit = 'project.project'

   
    escandallo_ids = fields.One2many('project.escandallo', 'project_id', string="Escandallo")
    subcontratista_ids = fields.One2many('project.escandallo.subcontratista', 'project_id', string="Subcontratistas")
    sale_escandallo_count = fields.Integer(compute='_compute_escandallo_count', string='Sale Offer Count')
    
    coste_escandallo = fields.Float(compute='_compute_coste_escandallo', string='Coste escandallo')
    coste_estimado_escandallo = fields.Float(string='Coste estimado escandallo')
    
    coste_subcontratista = fields.Float(compute='_compute_coste_escandallo', string='Coste subcontratistas')
    coste_estimado_subcontratista = fields.Float(string='Coste estimado subcontratistas')
    
    #copiar
    project_copiar_id = fields.Many2one('project.project', string="Copiar escandallo de")
    
    @api.multi
    def copiar_escandallo(self): 
        for record in self:
            if record.project_copiar_id:
                for escandallo in record.project_copiar_id.escandallo_ids:
                
                    if len(self.env['project.escandallo'].search([('project_id', '=', record.id), ('cod_pieza', '=', escandallo.cod_pieza)])) <= 0:
                    
                        if 'NC' not in escandallo.cod_pieza:
                            #creamos
                            self.env['project.escandallo'].create({'project_id': record.id, 
                                                                  'cod_pieza': escandallo.cod_pieza, 
                                                                  'product_id': escandallo.product_id.id, 
                                                                  'quantity': escandallo.quantity,
                                                                  'dimensiones': escandallo.dimensiones,
                                                                  'aleacion': escandallo.aleacion,
                                                                 })
                    

    
    
    @api.depends('subcontratista_ids')
    def _compute_coste_escandallo(self):
        for record in self:
            coste_escandallo = 0.0
            for escandallo in record.escandallo_ids:
                coste_escandallo = coste_escandallo + escandallo.coste_calculado
            coste_subcontratista = 0.0
            for escandallo in record.subcontratista_ids:
                coste_subcontratista = coste_subcontratista + escandallo.coste_calculado
                
                
            record.coste_escandallo = coste_escandallo
            record.coste_subcontratista = coste_subcontratista
    
    def _compute_escandallo_count(self):
        self.sale_escandallo_count = len(self.env['project.escandallo'].search([('project_id', '=', self.id),]))



class project_escandallo(models.Model):
    _name = 'project.escandallo'
    _description = "Escandallo"
    _order = 'project_id, cod_pieza'

    project_id = fields.Many2one('project.project', string="Proyecto", required=True)
    cod_proyecto = fields.Char(string="Cod proyecto", related='project_id.sequence_name', store=True)
    cod_pieza = fields.Char(string="Cod", default="000")
    product_id = fields.Many2one('product.template', string="Producto", required=True)
    quantity = fields.Float(digits=(6, 2), string='Cantidad', required=True)
    dimensiones = fields.Char(string='Dimensiones')
    aleacion = fields.Char(string='Aleación')
    entregar_a_id = fields.Many2one('res.partner', string="Entrega a")
    cuadreado = fields.Boolean(string='Cuadreado')
    peso = fields.Float(digits=(6, 2), string='Peso (kg)')
    
    forecast_id = fields.Many2one('account.bank.statement.line', string="Previsión pago", readonly=True)
    stock = fields.Boolean(string='En stock', default=False)
    
    fecha_pedido = fields.Date(string='Fecha pedido', compute='_get_fechas_pedido')
    fecha_prevista_recepcion = fields.Date(string='Fecha prevista recepción', compute='_get_fechas_pedido', store=True)
    fecha_recepcion = fields.Date(string='Fecha recepción', compute='_get_fechas_pedido', store=True)
    fecha_factura = fields.Date(string='Fecha factura', compute='_get_fechas_pedido')
    fecha_pago = fields.Date(string='Fecha de pago', compute='_get_fechas_pedido')
    
    fecha_pedido_manual = fields.Date(string='Fecha pedido (manual)')
    fecha_prevista_recepcion_manual = fields.Date(string='Fecha prevista recepción (manual)')
    fecha_recepcion_manual = fields.Date(string='Fecha recepción (manual)')
    fecha_factura_manual = fields.Date(string='Fecha factura (manual)')
    fecha_pago_manual = fields.Date(string='Fecha de pago (manual)')
    
    diseno_3d = fields.Boolean(string='Pieza 3D')
    diseno_2d = fields.Boolean(string='Plano 2D')
    diseno_torno = fields.Boolean(string='Torno')
    tratamiento = fields.Boolean(string='Trat')
    tratamiento_id = fields.Many2one('product.template', string="Tratamiento")
    etiqueta = fields.Boolean(string='Etiqueta')
    montaje = fields.Boolean(string='Montaje')
    pieza_subcontratista = fields.Boolean(string='Pieza subcontratista', default=False)
    actualizar = fields.Boolean(string='Actualizar')
    
    coste = fields.Float(digits=(6, 2), string='Coste manual', default=0.0)
    coste_calculado = fields.Float(compute='_compute_coste_calculado', string='Coste calculado')
    analytic_line_id = fields.Many2one('account.analytic.line', string="Coste computado", readonly=True)
    
    subcontratista_ids = fields.One2many('project.escandallo.subcontratista', 'escandallo_id', string="Escandallo")
    
    coste_subcontratistas = fields.Float(compute='_compute_coste_subcontratistas', string='Coste subcontratistas')
    txt_subcontratista = fields.Char(compute='_compute_coste_subcontratistas', string='Subcontratistas')
    
    #compras
    supplier_id = fields.Many2one('res.partner', string="Proveedor", compute='_get_datos_compras')
    num_solicitudes = fields.Integer(string="Num solicitudes", compute='_get_datos_compras')
    purchase_id = fields.Many2one('purchase.order', string="Orden de compra", compute='_get_datos_compras', store=True)
    purchase_line_ids = fields.One2many('purchase.order.line', 'escandallo_id', string="Líneas pedido")
    
    
    @api.multi
    def compute_cost(self): 
        for record in self:
            if record.stock == True and record.analytic_line_id == None and record.coste > 0.0:
                line_id = self.env['account.analytic.line'].create({'date': fields.Date.today(), 
                                                                      'name': "[STOCK] -> " + record.product_id.name, 
                                                                      'account_id': record.project_id.analytic_account_id.id, 
                                                                      'amount': record.coste * (-1),
                                                                      'unit_amount': 1,
                                                                      'product_id': record.product_id.id,
                                                                     })
                record.analytic_line_id = line_id.id
                
    
    
    @api.multi
    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, "%s: %s" % (record.cod_pieza, record.product_id.name)))
        return res
        
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search([('cod_pieza', operator, name)] + args, limit=limit)
        if not recs:
            recs = self.search([('product_id.name', operator, name)] + args, limit=limit)
        return recs.name_get()
        
        
    @api.depends('coste', 'purchase_line_ids')
    def _compute_coste_calculado(self):
        for record in self:
            coste = 0.0
            if record.coste > 0.0:
                coste = record.coste
            else:
                for line in record.purchase_line_ids:
                    if line.product_id:
                        if record.product_id.product_variant_id.id == line.product_id.id:
                            if line.order_id.state == 'purchase' or line.order_id.state == 'done':
                                coste = coste + line.price_subtotal
                
            record.coste_calculado = coste

    
    
    @api.multi
    def create_forecast_bank_line(self): 
        for record in self:
            if not record.forecast_id:
                journal_id = None
                for journal in self.env['account.journal'].search([('treasury_planning', '=', True),]):
                    journal_id = journal
                if journal_id:
                    bank_id = None
                    for bank in self.env['account.bank.statement'].search([('journal_id', '=', journal_id.id),('state', '=', 'open')]):
                        bank_id = bank
                    if bank_id:
                    
                        partner_id = None
                        if record.supplier_id:
                            partner_id = record.supplier_id.id
                            
                        account_analytic_id = None
                        if record.project_id.analytic_account_id:
                            account_analytic_id = record.project_id.analytic_account_id.id
                    
                    
                        line_id = self.env['account.bank.statement.line'].create({'date': record.fecha_pago, 
                                                                                  'name': record.project_id.name + ' - ' + record.supplier_id.name + ' - ' + record.product_id.name, 
                                                                                  'statement_id': bank_id.id, 
                                                                                  'amount': record.coste * (-1),
                                                                                  'amount_currency': record.coste * (-1),
                                                                                  'cf_forecast': True,
                                                                                  'partner_id': partner_id,
                                                                                  'account_analytic_id': account_analytic_id,
                                                                                 })
                    record.forecast_id = line_id.id
                    
    @api.multi
    def delete_forecast_bank_line(self): 
        for record in self:
            if record.forecast_id:
                record.forecast_id.unlink()
                record.forecast_id = None
                
                
    @api.multi
    def actualizar_datos(self): 
        for record in self:
            if record.actualizar == True:
                record.actualizar = False
            else:
                record.actualizar = True
    
    
    @api.depends('subcontratista_ids',
                 'purchase_line_ids',
                 'purchase_line_ids.order_id.state',
                 'pieza_subcontratista',
                 'actualizar')
    def _get_datos_compras(self):
        for record in self:
        
            purchase_id = None
            supplier_id = None
            for line in record.purchase_line_ids:
                if not line.subcontratista_id:
                    if line.order_id.state == 'purchase' or line.order_id.state == 'done':
                        purchase_id = line.order_id.id
                        supplier_id = line.order_id.partner_id.id 
            if record.pieza_subcontratista == True and purchase_id == None:
                for line in record.purchase_line_ids:
                    if line.order_id.state == 'purchase' or line.order_id.state == 'done':
                        purchase_id = line.order_id.id
                        supplier_id = line.order_id.partner_id.id 
                
            record.num_solicitudes = len(record.purchase_line_ids)
            record.purchase_id = purchase_id
            record.supplier_id = supplier_id
    
    
    @api.depends('subcontratista_ids')
    def _compute_coste_subcontratistas(self):
        for record in self:
            coste_subcontratistas = 0.0
            lista_subcontratista = []
            for subco in record.subcontratista_ids:
                coste_subcontratistas = coste_subcontratistas + subco.coste
                txt = subco.product_id.name
                if subco.supplier_id:
                    txt = txt + ' -> ' + subco.supplier_id.name
                    if subco.fecha_recepcion:
                        txt = txt + ' (REC ' + str(subco.fecha_recepcion) + ')'
                    elif subco.fecha_prevista_recepcion:
                        txt = txt + ' (PREV ' + str(subco.fecha_prevista_recepcion) + ')'
                lista_subcontratista.append(txt)
                
                
                
                
            record.txt_subcontratista = '\n'.join(lista_subcontratista)
            record.coste_subcontratistas = coste_subcontratistas
    
    @api.depends('purchase_id',
                 'purchase_id.state',
                 'purchase_id.order_line',
                 'purchase_id.order_line.date_planned',
                 'purchase_id.order_line.qty_received',
                 'purchase_id.state',
                 'purchase_id.fecha_entrega',
                 'purchase_id.picking_ids.state',
                 'fecha_pedido_manual', 
                 'fecha_prevista_recepcion_manual', 
                 'fecha_recepcion_manual', 
                 'fecha_factura_manual',
                 'fecha_pago_manual',
                 'actualizar',
                 'purchase_line_ids.move_ids',
                 'purchase_line_ids.qty_received',
                 'purchase_line_ids.date_planned')
    def _get_fechas_pedido(self):
        for record in self:
            fecha_pedido = None
            fecha_prevista_recepcion = None
            fecha_recepcion = None
            fecha_factura = None
            
            if record.fecha_pedido_manual:
                fecha_pedido = record.fecha_pedido_manual
            else:
                if record.purchase_id:
                    fecha_pedido = record.purchase_id.date_order.date()
                    
            #PREVISION DE RECEPCION
            if record.purchase_id:
                for elem in record.purchase_line_ids:
                    if elem.order_id.id == record.purchase_id.id:
                        fecha_prevista_recepcion = elem.date_planned.date()
                #fecha_prevista_recepcion = record.purchase_id.date_planned.date()
            else:
                if record.fecha_prevista_recepcion_manual:
                    fecha_prevista_recepcion = record.fecha_prevista_recepcion_manual
            

            #RECEPCION
            if record.fecha_recepcion_manual:
                fecha_recepcion = record.fecha_recepcion_manual
            else:
                for elem in record.purchase_line_ids:
                    if elem.order_id.id == record.purchase_id.id:
                        if elem.qty_received >= elem.product_qty:
                            for move in elem.move_ids:
                                fecha_recepcion = move.date.date()
                #if record.purchase_id:
                #    fecha_recepcion = record.purchase_id.fecha_entrega
                    
            if record.fecha_factura_manual:
                fecha_factura = record.fecha_factura_manual
            else:
                if record.purchase_id:
                    fecha_factura = record.purchase_id.fecha_factura

            record.fecha_pago = record.fecha_pago_manual
            record.fecha_pedido = fecha_pedido
            record.fecha_prevista_recepcion = fecha_prevista_recepcion
            record.fecha_recepcion = fecha_recepcion
            record.fecha_factura = fecha_factura
    
    
    
    
    @api.multi
    def action_view_form_project_escandallo(self):
        view = self.env.ref('mundimold_escandallo.view_project_escandallo_form')
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'project.escandallo',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'res_id': self.id,
            'context': self.env.context,
        }
        
        
    @api.multi
    def action_view_form_purchase_order(self):
        view = self.env.ref('purchase.purchase_order_form')
        purchase_id = None
        if self.purchase_id:
            purchase_id = self.purchase_id.id
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'purchase.order',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'res_id': purchase_id,
            'context': self.env.context,
        }
        
        
    @api.multi
    def action_view_list_purchase_order(self):
        view = self.env.ref('purchase.purchase_order_tree')
        list_ids = []
        for line in self.purchase_line_ids:
            list_ids.append(line.order_id.id)
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Compras Escandallo',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'context': 'purchase.order',
            #'views': [(view.id, 'tree')],
            #'view_id': view.id,
            'domain': [('id', 'in', list_ids)],
            'context': {},
        }

project_escandallo()      



    




class purchase_order_line(models.Model):
    _inherit = 'purchase.order.line'

    escandallo_id = fields.Many2one('project.escandallo', string="Escandallo")
    subcontratista_id = fields.Many2one('project.escandallo.subcontratista', string="Subcontratista")
    
    supplier_pieza_id = fields.Many2one('res.partner', string="Proveedor pieza", compute='_get_datos_escandallo')
    fecha_prevista_recepcion = fields.Date(string='Fecha prevista recepción', compute='_get_datos_escandallo')
    
    @api.depends('escandallo_id',
                 'escandallo_id.purchase_id')
    def _get_datos_escandallo(self):
        for record in self:
            supplier_pieza_id = None
            fecha_prevista_recepcion = None
            if record.escandallo_id.purchase_id:
                supplier_pieza_id = record.escandallo_id.supplier_id.id
                fecha_prevista_recepcion = record.escandallo_id.fecha_prevista_recepcion
            record.supplier_pieza_id = supplier_pieza_id
            record.fecha_prevista_recepcion = fecha_prevista_recepcion
                




class project_escandallo_subcontratista(models.Model):
    _name = 'project.escandallo.subcontratista'
    _description = "Escandallo"
    _order = 'cod_pieza'

    escandallo_id = fields.Many2one('project.escandallo', string="Escandallo", required=True)
    
    cod_pieza = fields.Char(string="Cod", related='escandallo_id.cod_pieza', store=True)
    pieza_id = fields.Many2one('product.template', string="Pieza", related='escandallo_id.product_id')
    
    project_id = fields.Many2one('project.project', string="Proyecto", related='escandallo_id.project_id')
    product_id = fields.Many2one('product.template', string="Producto", required=True)
    name = fields.Char(string='Detalles operación', required=False)
    quantity = fields.Float(digits=(6, 2), string='Cantidad', default=1.0, required=True)
    quantity_pieza = fields.Float(digits=(6, 2), string='Cantidad', related='escandallo_id.quantity')

    
    forecast_id = fields.Many2one('account.bank.statement.line', string="Previsión pago", readonly=True)
    
    supplier_id = fields.Many2one('res.partner', string="Proveedor", compute='_get_datos_compras', store=False)
    num_solicitudes = fields.Integer(string="Num solicitudes", compute='_get_datos_compras')
    purchase_id = fields.Many2one('purchase.order', string="Orden de compra", compute='_get_datos_compras', store=True)
    purchase_line_ids = fields.One2many('purchase.order.line', 'subcontratista_id', string="Líneas pedido")
    
    entregar_a_id = fields.Many2one('res.partner', string="Entrega a")
    
    
    fecha_pedido = fields.Date(string='Fecha pedido', compute='_get_fechas_pedido')
    fecha_prevista_recepcion = fields.Date(string='Fecha prevista recepción', compute='_get_fechas_pedido')
    fecha_recepcion = fields.Date(string='Fecha recepción', compute='_get_fechas_pedido')
    fecha_factura = fields.Date(string='Fecha factura', compute='_get_fechas_pedido')
    fecha_pago = fields.Date(string='Fecha de pago', compute='_get_fechas_pedido')
    
    fecha_pedido_manual = fields.Date(string='Fecha pedido (manual)')
    fecha_prevista_recepcion_manual = fields.Date(string='Fecha prevista recepción (manual)')
    fecha_recepcion_manual = fields.Date(string='Fecha recepción (manual)')
    fecha_factura_manual = fields.Date(string='Fecha factura (manual)')
    fecha_pago_manual = fields.Date(string='Fecha de pago (manual)')
    
    coste = fields.Float(digits=(6, 2), string='Coste', required=True)
    coste_calculado = fields.Float(compute='_compute_coste_calculado', string='Coste calculado')
    
    partner_ids = fields.Many2many('res.partner', string='Proveedores')
    actualizar = fields.Boolean(string='Actualizar')
    
    fecha_envio = fields.Date(string='Envio doc')
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_hr_documentos_subco_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Documentos")
    
    
    
    @api.depends('coste', 'purchase_line_ids')
    def _compute_coste_calculado(self):
        for record in self:
            coste = 0.0
            if record.coste > 0.0:
                coste = record.coste
            else:
                for line in record.purchase_line_ids:
                    if line.order_id.state == 'purchase' or line.order_id.state == 'done':
                        coste = coste + line.price_subtotal
                
            record.coste_calculado = coste
    
    
    
    @api.multi
    def action_view_form_project_subcontratista(self):
        view = self.env.ref('mundimold_escandallo.view_project_escandallo_subcontratista_form')
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'project.escandallo.subcontratista',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'res_id': self.id,
            'context': self.env.context,
        }
    
    
    
    @api.depends('purchase_line_ids',
                 'purchase_line_ids.order_id.state',
                 'actualizar')
    def _get_datos_compras(self):
        for record in self:
        
            purchase_id = None
            supplier_id = None
            for line in record.purchase_line_ids:

                if line.order_id.state == 'purchase' or line.order_id.state == 'done':
                    purchase_id = line.order_id.id
                    supplier_id = line.order_id.partner_id.id 
                
            record.num_solicitudes = len(record.purchase_line_ids)
            record.purchase_id = purchase_id
            record.supplier_id = supplier_id
    
    
    
    @api.multi
    def create_forecast_bank_line(self): 
        for record in self:
            if not record.forecast_id:
                journal_id = None
                for journal in self.env['account.journal'].search([('treasury_planning', '=', True),]):
                    journal_id = journal
                if journal_id:
                    bank_id = None
                    for bank in self.env['account.bank.statement'].search([('journal_id', '=', journal_id.id),('state', '=', 'open')]):
                        bank_id = bank
                    if bank_id:
                    
                        partner_id = None
                        if record.supplier_id:
                            partner_id = record.supplier_id.id
                            
                        account_analytic_id = None
                        if record.project_id.analytic_account_id:
                            account_analytic_id = record.project_id.analytic_account_id.id
                    
                        line_id = self.env['account.bank.statement.line'].create({'date': record.fecha_pago, 
                                                                                  'name': record.project_id.name + ' - ' + record.supplier_id.name + ' - ' + record.product_id.name, 
                                                                                  'statement_id': bank_id.id, 
                                                                                  'amount': record.coste * (-1),
                                                                                  'amount_currency': record.coste * (-1),
                                                                                  'cf_forecast': True,
                                                                                  'partner_id': partner_id,
                                                                                  'account_analytic_id': account_analytic_id,
                                                                                 })
                    record.forecast_id = line_id.id
                    
    @api.multi
    def delete_forecast_bank_line(self): 
        for record in self:
            if record.forecast_id:
                record.forecast_id.unlink()
                record.forecast_id = None
    
    
    
    
    @api.depends('purchase_id',
                 'purchase_id.state',
                 'purchase_id.order_line',
                 'purchase_id.order_line.date_planned',
                 'purchase_id.order_line.qty_received',
                 'purchase_id.state',
                 'purchase_id.fecha_entrega',
                 'purchase_id.picking_ids.state',
                 'fecha_pedido_manual', 
                 'fecha_prevista_recepcion_manual', 
                 'fecha_recepcion_manual', 
                 'fecha_factura_manual',
                 'fecha_pago_manual',
                 'actualizar')
    def _get_fechas_pedido(self):
        for record in self:
            fecha_pedido = None
            fecha_prevista_recepcion = None
            fecha_recepcion = None
            fecha_factura = None
            
            if record.fecha_pedido_manual:
                fecha_pedido = record.fecha_pedido_manual
            else:
                if record.purchase_id:
                    fecha_pedido = record.purchase_id.date_order.date()
                    
            #PREVISION DE RECEPCION
            if record.purchase_id:
                for elem in record.purchase_line_ids:
                    if elem.order_id.id == record.purchase_id.id:
                        fecha_prevista_recepcion = elem.date_planned.date()
                #fecha_prevista_recepcion = record.purchase_id.date_planned.date()
            else:
                if record.fecha_prevista_recepcion_manual:
                    fecha_prevista_recepcion = record.fecha_prevista_recepcion_manual
                    
            #RECEPCION        
            if record.fecha_recepcion_manual:
                fecha_recepcion = record.fecha_recepcion_manual
            else:
                for elem in record.purchase_line_ids:
                    if elem.order_id.id == record.purchase_id.id:
                        if elem.qty_received >= elem.product_qty:
                            for move in elem.move_ids:
                                fecha_recepcion = move.date.date()
                #if record.purchase_id:
                #    fecha_recepcion = record.purchase_id.fecha_entrega
                    
            if record.fecha_factura_manual:
                fecha_factura = record.fecha_factura_manual
            else:
                if record.purchase_id:
                    fecha_factura = record.purchase_id.fecha_factura

            record.fecha_pago = record.fecha_pago_manual
            record.fecha_pedido = fecha_pedido
            record.fecha_prevista_recepcion = fecha_prevista_recepcion
            record.fecha_recepcion = fecha_recepcion
            record.fecha_factura = fecha_factura
    
    

project_escandallo_subcontratista()   





class WizardEscandalloSubco(models.TransientModel):
    _name = 'wizard.escandallo.subco'
    

    def _default_escandallo(self):
        return self.env['project.escandallo'].browse(self._context.get('active_ids'))


    escandallo_ids = fields.Many2many('project.escandallo', string='Escandallo', default=_default_escandallo, required=True)
    product_id = fields.Many2one('product.template', string="Producto", required=True)
    name = fields.Char(string='Detalles operación', required=False)
    


    @api.multi
    def create_lineas_subco(self): 
        for record in self:
            lista_sub = []
            for escnadallo in record.escandallo_ids:
                purchase_id = self.env['project.escandallo.subcontratista'].create({'escandallo_id': escnadallo.id, 
                                                                                    'product_id': record.product_id.id, 
                                                                                    'name': record.name,
                                                                                    'coste': 0.0,
                                                                                    'quantity': 1,
                                                                                   })
                lista_sub.append(purchase_id.id)
        
        
            linea_ids = self.env['project.escandallo.subcontratista'].browse(lista_sub)
            
            view = self.env.ref('mundimold_escandallo.wizard_subcontratista_form_view')
            wiz = self.env['wizard.subcontratista'].create({'linea_ids': linea_ids,
                                                            'fecha_prevista': None,
                                                            'partner_ids': None})

            return {
                'name': 'Generar presupuesto subcontratistas',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'wizard.subcontratista',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': self.env.context,
            }
            
            








class WizardEscandalloPurchase(models.TransientModel):
    _name = 'wizard.escandallo.purchase'
    

    def _default_escandallo(self):
        return self.env['project.escandallo'].browse(self._context.get('active_ids'))


    escandallo_ids = fields.Many2many('project.escandallo', string='Escandallo', default=_default_escandallo, required=True)
    partner_ids = fields.Many2many('res.partner', string='Proveedores', required=True)
    fecha_prevista = fields.Date(string='Fecha prevista')
    entregar_a_id = fields.Many2one('res.partner', string="Entrega a")


    @api.onchange('fecha_prevista')
    def _onchange_referencia_cliente(self):
        for escandallo in self.escandallo_ids:
            escandallo.fecha_prevista_recepcion_manual = self.fecha_prevista
            
    @api.onchange('entregar_a_id')
    def _onchange_entregar_a_id(self):
        for escandallo in self.escandallo_ids:
            if self.entregar_a_id:
                escandallo.entregar_a_id = self.entregar_a_id.id
    
    
    
    @api.multi
    def create_purchases_wizard(self): 
        for record in self:
            
            
            for prov in record.partner_ids:
               
                purchase_id = self.env['purchase.order'].create({'partner_id': prov.id, 
                                                                  'date_order': datetime.now(), 
                                                                 })
                for elem in record.escandallo_ids:
                
                    #Comprobamos que no existe
                    existe = False
                    #for pur in elem.purchase_line_ids:
                    #    if pur.order_id.partner_id.id == prov.id:
                    #        existe = True
                    #        break
                
                    if existe == False:
                        description_prod = elem.product_id.name
                        #if elem.dimensiones:
                        #    description_prod = description_prod + '\n' + 'Dimensiones: ' + elem.dimensiones
                        #if elem.aleacion:
                        #    description_prod = description_prod + '\n' + 'Aleación: ' + elem.aleacion
                            
                        date_planned = fields.Date.today()
                        if elem.fecha_prevista_recepcion_manual:
                            date_planned = elem.fecha_prevista_recepcion_manual
                            
                        entregar_a_id = None
                        if elem.entregar_a_id:
                            entregar_a_id = elem.entregar_a_id.id
                    
                        line_id = self.env['purchase.order.line'].create({'order_id': purchase_id.id, 
                                                                           'name': description_prod, 
                                                                           'cod_pieza': elem.cod_pieza, 
                                                                           'product_uom_qty': elem.quantity,
                                                                           'product_qty': elem.quantity,
                                                                           'price_unit': 0.0,
                                                                           'date_planned': date_planned,
                                                                           'product_uom': elem.product_id.uom_id.id,
                                                                           'product_id': elem.product_id.product_variant_id.id,
                                                                           'escandallo_id': elem.id,
                                                                           'dimensiones': elem.dimensiones,
                                                                           'aleacion': elem.aleacion,
                                                                           'peso': elem.peso,
                                                                           'entregar_a_id': entregar_a_id,
                                                                           'cuadreado': elem.cuadreado,
                                                                           'account_analytic_id': elem.project_id.analytic_account_id.id,
                                                                          })
                        line_id._compute_tax_id()



                        
                        
class WizardSubcontratista(models.TransientModel):
    _name = 'wizard.subcontratista'
    

    def _default_escandallo(self):
    
        lista_sub = []
        for line in self.env['project.escandallo'].browse(self._context.get('active_ids')):
            for subco in line.subcontratista_ids:
                lista_sub.append(subco.id)
        return self.env['project.escandallo.subcontratista'].browse(lista_sub)


    line_ids = fields.Many2many('project.escandallo.subcontratista', string='Escandallo', default=_default_escandallo, required=True)
    
    partner_ids = fields.Many2many('res.partner', string='Proveedores', required=True)
    fecha_prevista = fields.Date(string='Fecha prevista')
    entregar_a_id = fields.Many2one('res.partner', string="Entrega a")


    @api.onchange('fecha_prevista')
    def _onchange_referencia_cliente(self):
        for line in self.line_ids:
            line.fecha_prevista_recepcion_manual = self.fecha_prevista
            
    @api.onchange('entregar_a_id')
    def _onchange_entregar_a_id(self):
        for line in self.line_ids:
            if self.entregar_a_id:
                line.entregar_a_id = self.entregar_a_id.id


    
    
    @api.multi
    def create_purchases_wizard(self): 
        for record in self:
            for prov in record.partner_ids:
            
                purchase_id = self.env['purchase.order'].create({'partner_id': prov.id, 
                                                                  'date_order': datetime.now(), 
                                                                 })
            
                for elem in record.line_ids:
                
                    
                
                    #Comprobamos que no existe
                    existe = False
                    #for pur in elem.purchase_line_ids:
                    #    if pur.order_id.partner_id.id == prov.id:
                    #        existe = True
                    #        break
                
                    if existe == False:
                    
                    
                        description_prod = 'PIEZA: ' + elem.escandallo_id.product_id.name
                        description_prod = description_prod + '\n'
                    
                        description_prod = description_prod + 'OPERACIÓN: ' + elem.product_id.name
                        if elem.name and elem.name != '':
                            description_prod = description_prod + '\n' + elem.name
                    
                        
                        
                        
                            
                        date_planned = fields.Date.today()
                        if elem.fecha_prevista_recepcion_manual:
                            date_planned = elem.fecha_prevista_recepcion_manual
                            
                        entregar_a_id = None
                        if elem.entregar_a_id:
                            entregar_a_id = elem.entregar_a_id.id
                    
                        line_id = self.env['purchase.order.line'].create({'order_id': purchase_id.id, 
                                                                           'name': description_prod, 
                                                                           'cod_pieza': elem.escandallo_id.cod_pieza, 
                                                                           'product_uom_qty': elem.escandallo_id.quantity,
                                                                           'product_qty': elem.escandallo_id.quantity,
                                                                           'price_unit': 0.0,
                                                                           'date_planned': date_planned,
                                                                           'product_uom': elem.product_id.uom_id.id,
                                                                           'product_id': elem.product_id.product_variant_id.id,
                                                                           'escandallo_id': elem.escandallo_id.id,
                                                                           'subcontratista_id': elem.id,
                                                                           'dimensiones': elem.escandallo_id.dimensiones,
                                                                           'aleacion': elem.escandallo_id.aleacion,
                                                                           'peso': elem.escandallo_id.peso,
                                                                           'entregar_a_id': entregar_a_id,
                                                                           'cuadreado': elem.escandallo_id.cuadreado,
                                                                           'account_analytic_id': elem.project_id.analytic_account_id.id,
                                                                          })
                        line_id._compute_tax_id()


