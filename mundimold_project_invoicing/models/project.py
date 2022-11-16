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



class mis_report_instance(models.Model):
    _name = 'mis.report.instance'
    _inherit = 'mis.report.instance'
    
    type_name = fields.Char(string="Clasificación")


        
class project_project(models.Model):
    _name = 'project.project'
    _inherit = 'project.project'
    
    
    product_facturacion_id = fields.Many2one('product.template', string="Producto de facturación")

   
    invoice_plan_ids = fields.One2many('project.invoice.plan', 'project_id', string="Planificación facturación")
    invoice_plan_base_amount = fields.Float(compute='_compute_invoice_plan_base_amount', string='Previsión de facturación')
    comments_facturacion = fields.Text(string="Comentarios facturación")
    
    
    invoice_supplier_ids = fields.One2many('project.invoice.supplier', 'project_id', string="Planificación facturación compras")
    invoice_supplier_base_amount = fields.Float(compute='_compute_invoice_plan_base_amount', string='Previsión de facturación compras')
    
    oc_cliente = fields.Char(string="OC Cliente")
    num_oferta = fields.Char(string="Num oferta")

    @api.depends('invoice_plan_ids')
    def _compute_invoice_plan_base_amount(self):
        for record in self:
            invoice_plan_base_amount = 0.0
            for invoice in record.invoice_plan_ids:
                invoice_plan_base_amount = invoice_plan_base_amount + invoice.price_subtotal
            record.invoice_plan_base_amount = invoice_plan_base_amount
            
            invoice_supplier_base_amount = 0.0
            for invoice in record.invoice_supplier_ids:
                invoice_supplier_base_amount = invoice_supplier_base_amount + invoice.price_subtotal
            record.invoice_supplier_base_amount = invoice_supplier_base_amount


class project_invoice_plan(models.Model):
    _name = 'project.invoice.plan'

    project_id = fields.Many2one('project.project', string="Proyecto", required=True)
    product_id = fields.Many2one('product.template', string="Producto", required=True)
    name = fields.Char(string="Descripción", required=True)
    uom_id = fields.Many2one('uom.uom', string='Unidad de medida')
    quantity = fields.Float(digits=(6, 2), string='Cantidad', required=True, default=1.0)
    price_unit = fields.Float(digits=(6, 2), string='Precio ud. (con IVA)', required=True)
    tax = fields.Float(digits=(6, 2), string='% IVA', compute='_get_default_tax')
    price_unit_base = fields.Float(digits=(6, 2), string='Precio ud. (sin IVA)')
    price_subtotal = fields.Float(compute='_compute_subtotal', string='Subtotal')
    date_invoice = fields.Date(string='Fecha factura', compute='_get_fechas_plan')
    date_forecast = fields.Date(string='Fecha cobro', compute='_get_fechas_plan')
    date_invoice_manual = fields.Date(string='Fecha factura')
    date_forecast_manual = fields.Date(string='Fecha cobro')

    invoice_id = fields.Many2one('account.invoice', string="Factura")
    forecast_id = fields.Many2one('account.bank.statement.line', string="Previsión cobro", readonly=True)
    
    permite_crear_forecast = fields.Boolean(string='Permite crear forecast', compute='_get_permites', store=True)
    permite_borrar_forecast = fields.Boolean(string='Permite borrar forecast', compute='_get_permites', store=True)
    
    @api.multi
    def _get_default_tax(self): 
        for record in self:
    
            tax = 0.0
            if record.project_id:
                if record.project_id.partner_id:
                    if record.project_id.partner_id.country_id:
                        if record.project_id.partner_id.country_id.name == "España":
                            tax = 21.0
            record.tax = tax

        
    @api.onchange('price_unit_base')
    def _onchange_price_unit_base(self):
        if self.price_unit_base >= 0.0:
            self.price_unit = self.price_unit_base + self.price_unit_base*(self.tax/100)
            
    @api.onchange('price_unit')
    def _onchange_price_unit(self):
        if self.price_unit >= 0.0:
            self.price_unit_base = self.price_unit / (1+ self.tax/100)
            
                        
    
    
    @api.multi
    def create_invoice_line(self): 
        for record in self:
            record.delete_forecast_bank_line()
            if not record.invoice_id:
            
                #COMPROBAMOS
                if not record.project_id.partner_id:
                    raise ValidationError("Error: El proyecto no tiene un cliente asociado")
                if not record.project_id.analytic_account_id.id:
                    raise ValidationError("Error: El proyecto no tiene una cuenta analítica asociada")
                
                fiscal_position = None
                if record.project_id.partner_id.property_account_position_id:
                    fiscal_position = record.project_id.partner_id.property_account_position_id
                if fiscal_position == None:
                    fiscal_position = self.env['account.fiscal.position'].search([('company_id', '=', record.project_id.company_id.id),('name', 'like', 'Régimen Nacional')])[0]
                
                product_id = record.product_id.product_variant_id
                
                payment_term_id = False
                
                #creamos cabecera de factura
                
                account_id = fiscal_position.map_account(record.product_id.property_account_income_id or record.product_id.categ_id.property_account_income_categ_id).id
                if not account_id:
                    inc_acc = ir_property_obj.get('property_account_income_categ_id', 'product.category')
                    account_id = fiscal_position.map_account(inc_acc).id if inc_acc else False
                    
                taxes = record.product_id.taxes_id.filtered(lambda r: not record.project_id.company_id or r.company_id == record.project_id.company_id)
                if fiscal_position and taxes:
                    tax_ids = fiscal_position.map_tax(taxes, record.product_id, record.project_id.partner_id).ids
                else:
                    tax_ids = taxes.ids
                    
                payment_mode_id = None
                if record.project_id.partner_id.customer_payment_mode_id:
                    payment_mode_id = record.project_id.partner_id.customer_payment_mode_id.id
                    
                payment_term_id = None
                if record.project_id.partner_id.property_payment_term_id:
                    payment_term_id = record.project_id.partner_id.property_payment_term_id.id
                    
                    
                price_unit = record.price_unit
                if record.price_unit_base > 0.0:
                    price_unit = record.price_unit_base
                
                invoice = self.env['account.invoice'].create({
                    'type': 'out_invoice',
                    'reference': False,
                    'name': record.project_id.num_oferta,
                    'oc_cliente': record.project_id.oc_cliente,
                    'account_id': record.project_id.partner_id.property_account_receivable_id.id,
                    'partner_id': record.project_id.partner_id.id,
                    'invoice_line_ids': [(0, 0, {
                        'name': record.name,
                        'account_id': account_id,
                        'price_unit': price_unit,
                        'quantity': record.quantity,
                        'discount': 0.0,
                        'uom_id': record.product_id.uom_id.id,
                        'product_id': product_id.id,
                        'invoice_line_tax_ids': [(6, 0, tax_ids)],
                        'account_analytic_id': record.project_id.analytic_account_id.id,
                    })],
                    #'currency_id': order.pricelist_id.currency_id.id,
                    'payment_term_id': payment_term_id,
                    'payment_mode_id': payment_mode_id,
                    'fiscal_position_id': fiscal_position.id,
                    'company_id': record.project_id.company_id.id,
                })
                invoice.compute_taxes()
                record.invoice_id = invoice.id
                
                
            
            
    
    @api.depends('invoice_id', 'forecast_id')
    def _get_permites(self):
        for record in self:
        
            permite_crear_forecast = True
            permite_borrar_forecast = False
            
            if record.invoice_id or record.forecast_id:
                permite_crear_forecast = False
                
            if record.forecast_id:
                permite_borrar_forecast = True
            
            record.permite_crear_forecast = permite_crear_forecast
            record.permite_borrar_forecast = permite_borrar_forecast
    
    
    @api.multi
    def create_forecast_bank_line(self): 
        for record in self:
            if not record.forecast_id and not record.invoice_id:
                journal_id = None
                for journal in self.env['account.journal'].search([('treasury_planning', '=', True),('company_id','=',record.project_id.company_id.id)]):
                    journal_id = journal
                if journal_id:
                    bank_id = None
                    for bank in self.env['account.bank.statement'].search([('journal_id', '=', journal_id.id),('state', '=', 'open'),('company_id','=',record.project_id.company_id.id)]):
                        bank_id = bank
                    
                    partner_id = None
                    if record.project_id.partner_id:
                        partner_id = record.project_id.partner_id.id
                        
                    account_analytic_id = None
                    if record.project_id.analytic_account_id:
                        account_analytic_id = record.project_id.analytic_account_id.id
                        
                    if bank_id:
                        line_id = self.env['account.bank.statement.line'].create({'date': record.date_forecast, 
                                                                                  'name': record.project_id.name + ' - ' + record.name, 
                                                                                  'statement_id': bank_id.id, 
                                                                                  'amount': record.price_subtotal,
                                                                                  'amount_currency': record.price_subtotal,
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
                    
                
    
    
    
    
    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for record in self:
            record.price_subtotal = record.quantity * record.price_unit

    
    
    
    @api.depends('date_invoice_manual', 
                 'date_forecast_manual', 
                 'invoice_id', 
                 'forecast_id')
    def _get_fechas_plan(self):
        for record in self:
            date_invoice = None
            date_forecast = None

            
            if record.invoice_id:
                date_invoice = record.invoice_id.date_invoice 
            else:
                date_invoice = record.date_invoice_manual
                    

            date_forecast = record.date_forecast_manual

            record.date_invoice = date_invoice
            record.date_forecast = date_forecast
    
    


    

class project_invoice_supplier(models.Model):
    _name = 'project.invoice.supplier'

    project_id = fields.Many2one('project.project', string="Proyecto", required=True)
    partner_id = fields.Many2one('res.partner', string="Proveedor")
    name = fields.Char(string="Descripción", required=True)
    price_subtotal = fields.Float(string='Subtotal')
    date_invoice = fields.Date(string='Fecha factura')
    date_forecast = fields.Date(string='Fecha pago')

    invoice_id = fields.Many2one('account.invoice', string="Factura")
    forecast_id = fields.Many2one('account.bank.statement.line', string="Previsión pago", readonly=True)
    
    permite_crear_forecast = fields.Boolean(string='Permite crear forecast', compute='_get_permites', store=True)
    permite_borrar_forecast = fields.Boolean(string='Permite borrar forecast', compute='_get_permites', store=True)
    
    
    @api.depends('invoice_id', 'forecast_id')
    def _get_permites(self):
        for record in self:
        
            permite_crear_forecast = True
            permite_borrar_forecast = False
            
            if record.invoice_id or record.forecast_id:
                permite_crear_forecast = False
                
            if record.forecast_id:
                permite_borrar_forecast = True
            
            record.permite_crear_forecast = permite_crear_forecast
            record.permite_borrar_forecast = permite_borrar_forecast
    
    
    @api.multi
    def create_forecast_bank_line(self): 
        for record in self:
            if not record.forecast_id and not record.invoice_id:
                journal_id = None
                for journal in self.env['account.journal'].search([('treasury_planning', '=', True),('company_id','=',record.project_id.company_id.id)]):
                    journal_id = journal
                if journal_id:
                    bank_id = None
                    for bank in self.env['account.bank.statement'].search([('journal_id', '=', journal_id.id),('state', '=', 'open'),('company_id','=',record.project_id.company_id.id)]):
                        bank_id = bank
                    
                    partner_id = None
                    if record.partner_id:
                        partner_id = record.partner_id.id
                        
                    account_analytic_id = None
                    if record.project_id.analytic_account_id:
                        account_analytic_id = record.project_id.analytic_account_id.id
                        
                    if bank_id:
                        line_id = self.env['account.bank.statement.line'].create({'date': record.date_forecast, 
                                                                                  'name': record.project_id.name + ' - ' + record.name, 
                                                                                  'statement_id': bank_id.id, 
                                                                                  'amount': record.price_subtotal * (-1),
                                                                                  'amount_currency': record.price_subtotal * (-1),
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

