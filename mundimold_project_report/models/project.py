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

        
        
        
class res_company(models.Model):
    _name = 'res.company'
    _inherit = 'res.company'
    
    coste_hora = fields.Float(string='Coste hora fábrica', default=40)
        
        
class account_analytic_line(models.Model):
    _name = 'account.analytic.line'
    _inherit = 'account.analytic.line'        
    
    
    num_factura = fields.Char(compute='_compute_num_factura', string='Num factura')
    
    @api.depends('move_id')
    def _compute_num_factura(self):
        for record in self:

            num_factura = ''
            if record.move_id:
                if record.move_id.invoice_id:
                    num_factura = record.move_id.invoice_id.number
            record.num_factura = num_factura
        
        
    @api.multi
    def action_view_invoice_line(self):
        view = self.env.ref('account.invoice_form')
        list_ids = []
        id_factura = None
        if self.move_id:
            if self.move_id.invoice_id:
                id_factura = self.move_id.invoice_id.id

        

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'res_id': id_factura,
            'context': self.env.context,
        }
        
    
        
        
        
        
        
class project_project(models.Model):
    _name = 'project.project'
    _inherit = 'project.project'

    partner_name = fields.Char(compute='_compute_analytic_projects', string='Cliente')

    coste_materiales = fields.Float(compute='_compute_analytic_projects', string='Coste materiales')
    coste_subco = fields.Float(compute='_compute_analytic_projects', string='Coste subcontratación')
    coste_transporte = fields.Float(compute='_compute_analytic_projects', string='Coste transporte')
    coste_stock = fields.Float(compute='_compute_analytic_projects', string='Coste stock')
    precio_proyecto_estimado = fields.Float(compute='_compute_analytic_projects', string='Precio')
    precio_reparacion = fields.Float(string='Precio reparación')
    facturado_proyecto = fields.Float(compute='_compute_analytic_projects', string='Facturado')
    beneficio_proyecto = fields.Float(compute='_compute_analytic_projects', string='Beneficio')
    beneficio_proyecto_ptje = fields.Float(compute='_compute_analytic_projects', string='% Beneficio')
    
    horas_presenciales = fields.Float(compute='_compute_analytic_projects', string='Horas presenciales')
    horas_diseno = fields.Float(compute='_compute_analytic_projects', string='Horas diseño')
    horas_nopresenciales = fields.Float(compute='_compute_analytic_projects', string='Horas no presenciales')
    horas_totales = fields.Float(compute='_compute_analytic_projects', string='Horas totales')
    coste_produccion = fields.Float(compute='_compute_analytic_projects', string='Coste producción')
    coste_produccion_estimado = fields.Float(compute='_compute_analytic_projects', string='Coste producción estimado')
    coste_total = fields.Float(compute='_compute_analytic_projects', string='Coste total')
    
    no_conformidad = fields.Float(compute='_compute_analytic_projects', string='No conformidad')
    
    horas_diseno_estimadas = fields.Float(string='Horas diseño estimadas')
    horas_totales_estimadas = fields.Float(string='Horas teóricas producción', compute='_compute_horas_teoricas')
    
    b0 = fields.Float(string='B (%)')
    beneficio_teorico = fields.Float(string='B teórico', compute='_compute_horas_teoricas')
    beneficio_real = fields.Float(string='B real', compute='_compute_horas_teoricas')
    beneficio_real_ptje = fields.Float(string='B real (%)', compute='_compute_horas_teoricas')
    
    #informe estimacion
    coste_total_teorico = fields.Float(compute='_compute_horas_teoricas', string='Coste total teórico')
    coste_total_real = fields.Float(compute='_compute_horas_teoricas', string='Coste total real')
    desviacion_coste_total = fields.Float(compute='_compute_horas_teoricas', string='Desviación coste total')
    
    desviacion_horas_diseno = fields.Float(compute='_compute_analytic_projects', string='Desviación horas diseño')
    desviacion_horas = fields.Float(compute='_compute_analytic_projects', string='Desviación horas')
    desviacion_escandallo = fields.Float(compute='_compute_analytic_projects', string='Desviación escandallo')
    desviacion_subcontratacion = fields.Float(compute='_compute_analytic_projects', string='Desviación subcontratación')
    desviacion_produccion = fields.Float(compute='_compute_analytic_projects', string='Desviación producción')
    
    
    @api.depends('precio_proyecto_estimado', 'coste_estimado_escandallo', 'coste_estimado_subcontratista')
    def _compute_horas_teoricas(self):
        
        for record in self:
            horas_totales_estimadas= 0.0
            beneficio_teorico = (record.precio_proyecto_estimado * (1+(record.b0 / 100))) - record.precio_proyecto_estimado
            coste_hora = record.company_id.coste_hora
            if coste_hora > 0:
                horas_totales_estimadas = (record.precio_proyecto_estimado - record.coste_estimado_escandallo - record.coste_estimado_subcontratista - beneficio_teorico)/coste_hora
            
            record.beneficio_teorico = beneficio_teorico
            record.horas_totales_estimadas = horas_totales_estimadas
            
            record.coste_total_teorico = record.precio_proyecto_estimado - record.beneficio_teorico
            record.coste_total_real = record.coste_escandallo + record.coste_subcontratista + (record.horas_totales * coste_hora)
            record.desviacion_coste_total = record.coste_total_teorico - record.coste_total_real
            record.beneficio_real = record.precio_proyecto_estimado - record.coste_total_real
            beneficio_real_ptje = 0.0
            if record.precio_proyecto_estimado>0.0:
                beneficio_real_ptje = (record.beneficio_real/record.precio_proyecto_estimado) * 100
            record.beneficio_real_ptje = beneficio_real_ptje
    
    @api.depends('analytic_account_id', 'partner_id')
    def _compute_analytic_projects(self):
        for record in self:
        
            partner_name = ''
            if record.partner_id:
                if record.partner_id.comercial and record.partner_id.comercial != '':
                    partner_name = record.partner_id.comercial
                else:
                    partner_name = record.partner_id.name
            record.partner_name = partner_name

            coste_materiales = 0.0
            for line in self.env['account.analytic.line'].search([('general_account_id.code', 'ilike', '601%'),('account_id', '=', record.analytic_account_id.id)]):
                coste_materiales = coste_materiales + line.amount
                
            coste_subco = 0.0
            for line in self.env['account.analytic.line'].search([('general_account_id.code', 'ilike', '607%'),('account_id', '=', record.analytic_account_id.id)]):
                coste_subco = coste_subco + line.amount
                
            coste_transporte = 0.0
            for line in self.env['account.analytic.line'].search([('general_account_id.code', 'ilike', '624%'),('account_id', '=', record.analytic_account_id.id)]):
                coste_transporte = coste_transporte + line.amount
                
            facturado_proyecto = 0.0
            for line in self.env['account.analytic.line'].search([('general_account_id.code', '=like', '7%'),('account_id', '=', record.analytic_account_id.id)]):
                facturado_proyecto = facturado_proyecto + line.amount
                
            precio_proyecto_estimado = 0.0
            for line in record.invoice_plan_ids:
                
                if line.price_unit_base <= 0:
                    precio_proyecto_estimado = precio_proyecto_estimado + line.price_unit
                else:
                    precio_proyecto_estimado = precio_proyecto_estimado + line.price_unit_base
                    
            if record.precio_reparacion > 0.0:
                precio_proyecto_estimado = record.precio_reparacion
                    
            no_conformidad = 0
            for line in self.env['project.noconformidad'].search([('project_id', '=', record.id),]):
                no_conformidad = no_conformidad + line.coste_materiales + line.coste_subcontratacion
                
            coste_stock = 0.0
            for line in self.env['project.escandallo'].search([('project_id', '=', record.id),('stock', '=', True)]):
                coste_stock = coste_stock + (line.coste_calculado * (-1))
                
                    
            horas_presenciales = 0
            horas_nopresenciales = 0
            horas_diseno = 0
            
            for line in self.env['hr.timesheet.employee'].search([('project_id', '=', record.id),]):
            
                if line.fase_id.type_timesheet == "DIS":
                    horas_diseno = horas_diseno + line.horas_presenciales + line.horas_no_presenciales
                else:
                    horas_presenciales = horas_presenciales + line.horas_presenciales
                    horas_nopresenciales = horas_nopresenciales + line.horas_no_presenciales
            
            
            coste_hora = record.company_id.coste_hora
            coste_hora = coste_hora * (-1)
            coste_produccion = (horas_presenciales + horas_nopresenciales) * coste_hora
            
            coste_produccion_estimado = record.horas_totales_estimadas * coste_hora
            
            coste_total = coste_materiales + coste_subco + coste_transporte + coste_stock + coste_produccion
                    
            
            record.coste_materiales = coste_materiales
            record.coste_subco = coste_subco
            record.coste_transporte = coste_transporte
            record.coste_stock = coste_stock
            record.precio_proyecto_estimado = precio_proyecto_estimado
            record.facturado_proyecto = facturado_proyecto
            
            record.horas_presenciales = horas_presenciales
            record.horas_nopresenciales = horas_nopresenciales
            record.horas_diseno = horas_diseno
            record.horas_totales = horas_presenciales + horas_nopresenciales
            record.no_conformidad = no_conformidad
            record.coste_produccion = coste_produccion
            record.coste_produccion_estimado = coste_produccion_estimado
            record.coste_total = coste_total
            
            record.beneficio_proyecto = precio_proyecto_estimado + coste_total
            
            beneficio_proyecto_ptje = 0.0
            if precio_proyecto_estimado > 0.0:
                beneficio_proyecto_ptje = (record.beneficio_proyecto / precio_proyecto_estimado) * 100
            record.beneficio_proyecto_ptje = beneficio_proyecto_ptje
            
            record.desviacion_horas_diseno = record.horas_diseno_estimadas - record.horas_diseno
            record.desviacion_horas = record.horas_totales_estimadas - record.horas_totales
            record.desviacion_escandallo = record.coste_estimado_escandallo - record.coste_escandallo
            record.desviacion_subcontratacion = record.coste_estimado_subcontratista - record.coste_subcontratista
            record.desviacion_produccion = record.coste_produccion_estimado - record.coste_produccion
            

    @api.multi
    def action_view_list_analytic_lines(self):
        view = self.env.ref('mundimold_project_report.view_account_analytic_line_rentabilidad_tree')
        list_ids = []
        for line in self.analytic_account_id.line_ids:
            list_ids.append(line.id)
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Apuntes analíticos',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.analytic.line',
            'context': 'account.analytic.line',
            'views': [(view.id, 'tree')],
            'view_id': view.id,
            'domain': [('id', 'in', list_ids)],
            'context': {},
        }
        
    @api.multi
    def action_view_list_601(self):
        view = self.env.ref('mundimold_project_report.view_account_analytic_line_rentabilidad_tree')
        list_ids = []
        for line in self.env['account.analytic.line'].search([('general_account_id.code', 'ilike', '601%'),('account_id', '=', self.analytic_account_id.id)]):
            list_ids.append(line.id)
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Apuntes analíticos',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.analytic.line',
            'context': 'account.analytic.line',
            'views': [(view.id, 'tree')],
            'view_id': view.id,
            'domain': [('id', 'in', list_ids)],
            'context': {},
        }
        
    @api.multi
    def action_view_list_607(self):
        view = self.env.ref('mundimold_project_report.view_account_analytic_line_rentabilidad_tree')
        list_ids = []
        for line in self.env['account.analytic.line'].search([('general_account_id.code', 'ilike', '607%'),('account_id', '=', self.analytic_account_id.id)]):
            list_ids.append(line.id)
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Apuntes analíticos',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.analytic.line',
            'context': 'account.analytic.line',
            'views': [(view.id, 'tree')],
            'view_id': view.id,
            'domain': [('id', 'in', list_ids)],
            'context': {},
        }
        
    @api.multi
    def action_view_list_624(self):
        view = self.env.ref('mundimold_project_report.view_account_analytic_line_rentabilidad_tree')
        list_ids = []
        for line in self.env['account.analytic.line'].search([('general_account_id.code', 'ilike', '624%'),('account_id', '=', self.analytic_account_id.id)]):
            list_ids.append(line.id)
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Apuntes analíticos',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.analytic.line',
            'context': 'account.analytic.line',
            'views': [(view.id, 'tree')],
            'view_id': view.id,
            'domain': [('id', 'in', list_ids)],
            'context': {},
        }
        
        
    @api.multi
    def action_view_list_7(self):
        view = self.env.ref('mundimold_project_report.view_account_analytic_line_rentabilidad_tree')
        list_ids = []
        for line in self.env['account.analytic.line'].search([('general_account_id.code', '=like', '7%'),('account_id', '=', self.analytic_account_id.id)]):
            list_ids.append(line.id)
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Apuntes analíticos',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.analytic.line',
            'context': 'account.analytic.line',
            'views': [(view.id, 'tree')],
            'view_id': view.id,
            'domain': [('id', 'in', list_ids)],
            'context': {},
        }
        
        
    @api.multi
    def action_view_list_conformidad(self):
        view = self.env.ref('mundimold_no_conformidades.view_project_noconformidad_tree')
        list_ids = []
        for line in self.env['project.noconformidad'].search([('project_id', '=', self.id),]):
            list_ids.append(line.id)
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'No conformidades',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'project.noconformidad',
            'context': 'project.noconformidad',
            #'views': [(view.id, 'tree')],
            #'view_id': view.id,
            'domain': [('id', 'in', list_ids)],
            'context': {},
        }
        
        
    @api.multi
    def action_view_list_timesheet(self):
        view = self.env.ref('mundimold_timesheet.view_hr_timesheet_employee_tree')
        list_ids = []
        for line in self.env['hr.timesheet.employee'].search([('project_id', '=', self.id),]):
            list_ids.append(line.id)
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Partes fábrica',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'hr.timesheet.employee',
            'context': 'hr.timesheet.employee',
            #'views': [(view.id, 'tree')],
            #'view_id': view.id,
            'domain': [('id', 'in', list_ids)],
            'context': {},
        }


    @api.multi
    def action_view_form_project_project(self):
        view = self.env.ref('project.edit_project')

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'project.project',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'res_id': self.id,
            'context': self.env.context,
        }








class WizardProjectReparacion(models.TransientModel):
    _name = 'wizard.project.reparacion'
    

    def _default_project(self):
        return self.env['project.project'].browse(self._context.get('active_id'))


    project_id = fields.Many2one('project.project', string='Proyecto', default=_default_project, required=True)
    
    coste_escandallo = fields.Float(string='Coste escandallo', related='project_id.coste_escandallo')
    coste_subcontratista = fields.Float(string='Coste subcontratistas', related='project_id.coste_subcontratista')
    coste_produccion = fields.Float(string='Coste producción', compute='_compute_coste_produccion')
    
    porcentaje_aplicado = fields.Float(string='% beneficio deseado')
    precio_venta = fields.Float(string='Precio de venta', compute='_compute_precio_venta')
    
    
    @api.depends('project_id', 'project_id.coste_produccion')
    def _compute_coste_produccion(self):
        for record in self:
            if record.project_id:
                record.coste_produccion = record.project_id.coste_produccion * (-1)

    @api.depends('porcentaje_aplicado', 'coste_escandallo', 'coste_subcontratista', 'coste_produccion')
    def _compute_precio_venta(self):
        for record in self:
            total_coste = record.coste_escandallo + record.coste_subcontratista + record.coste_produccion
            record.precio_venta = total_coste + (total_coste * (record.porcentaje_aplicado)/100)






    @api.multi
    def actualizar_precio_reparacion(self): 
        for record in self:
            record.project_id.precio_reparacion = record.precio_venta