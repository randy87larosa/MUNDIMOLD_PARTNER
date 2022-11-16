# -*- coding: utf-8 -*-
# © 2009 NetAndCo (<http://www.netandco.net>).
# © 2011 Akretion Benoît Guillot <benoit.guillot@akretion.com>
# © 2014 prisnet.ch Seraphine Lantible <s.lantible@gmail.com>
# © 2016 Serpent Consulting Services Pvt. Ltd.
# © 2018 Daniel Campos <danielcampos@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date
from odoo.exceptions import UserError, ValidationError
import calendar





class MrRouting(models.Model):
    _name = 'mrp.routing'
    _inherit = 'mrp.routing'
    
    maquina_ids = fields.Many2many('mrp.workcenter', string="Máquinas posibles")
    
    MAINT = [('PROD','Productiva'),   
             ('NOPR','No productiva'),
             ('DIS','Diseño'),
             ]
    type_timesheet = fields.Selection(selection=MAINT, string='Tipo hora')




class HrTimesheetEmployee(models.Model):
    _name = 'hr.timesheet.employee'
    
    
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)
    
    #campos
    date = fields.Date(string="Fecha", required=True, default=fields.Date.today())
    user_id = fields.Many2one('res.users','Usuario', default=lambda self: self.env.user)
    employee_id = fields.Many2one('hr.employee', string="Empleado", required=True)
    project_id = fields.Many2one('project.project', string="Proyecto", required=False)
    task_id = fields.Many2one('project.task', string="Tarea", domain = "[('project_id','=',project_id)]")
    maquina_id = fields.Many2one('mrp.workcenter', string="Máquina")
    noconformidad_id = fields.Many2one('project.noconformidad', string="No conformidad", domain = "[('project_id','=',project_id)]")
    fase_id = fields.Many2one('mrp.routing', string="Subfase", domain = "['|',('maquina_ids','in',maquina_id),('maquina_ids','=',False)]")
    escandallo_id = fields.Many2one('project.escandallo', string="Pieza escandallo", domain = "[('project_id','=',project_id)]")
    num_pieza = fields.Char(string="Num pieza")
    horas_presenciales = fields.Float(string="Horas presenciales")
    horas_no_presenciales = fields.Float(string="Horas no presenciales")
    horas_totales = fields.Float(string="Horas totales", readonly=True, compute='_compute_horas_totales', store=True )
    comentario = fields.Char(string="Comentario")
    interno = fields.Char(string="Interno")
    
    MAINT = [('PROD','Productiva'),   
             ('NOPR','No productiva'),
             ('DIS','Diseño'),
             ]
    type_timesheet = fields.Selection(selection=MAINT, string='Tipo hora', store=True, related='fase_id.type_timesheet')
    
    
    @api.depends('horas_presenciales', 'horas_no_presenciales')
    def _compute_horas_totales(self):
        for record in self:
            record.horas_totales = record.horas_presenciales + record.horas_no_presenciales
    
    
    @api.model
    def default_get(self, field_list):
        result = super(HrTimesheetEmployee, self).default_get(field_list)
        if not self.env.context.get('default_employee_id') and 'employee_id' in field_list and result.get('user_id'):
            result['employee_id'] = self.env['hr.employee'].search([('user_id', '=', result['user_id'])], limit=1).id
        return result

    
    @api.model
    def create(self, vals_list):
        res = super(HrTimesheetEmployee, self).create(vals_list)
        
        if vals_list["fase_id"]:
            fase_id = None
            for elem in self.env['mrp.routing'].search([('id', '=', vals_list["fase_id"])]):
                fase_id = elem
                break
            if 'Ausencias' in fase_id.name or 'Personal' in fase_id.name:
                if vals_list["project_id"]:
                    raise UserError("Error: No se puede poner Proyecto en fases de Personal o Ausencias")
                if vals_list["maquina_id"]:
                    raise UserError("Error: No se puede poner Máquina en fases de Personal o Ausencias")
            elif 'General' in fase_id.name:
                if vals_list["project_id"]:
                    raise UserError("Error: No se puede poner Proyecto en fases de General")
            else:
                if not vals_list["project_id"]:
                    raise UserError("Error: Es obligatorio indicar un proyecto")
                if not vals_list["maquina_id"]:
                    raise UserError("Error: Es obligatorio indicar una máquina")
                    
            if '181' in fase_id.name or '182' in fase_id.name or '183' in fase_id.name:
                if not vals_list["noconformidad_id"]:
                    raise UserError("Error: Se debe indicar la no conformidad")
        return res
    
    
    @api.onchange('employee_id')
    def calc_price_cost(self):
        if self.employee_id:
            if self.employee_id.maquina_id:
                self.maquina_id = self.employee_id.maquina_id.id
    

