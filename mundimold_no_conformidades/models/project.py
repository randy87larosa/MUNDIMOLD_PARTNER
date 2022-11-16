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



class project_noconformidad_type(models.Model):
    _name = 'project.noconformidad.type'

    name = fields.Char(string="Tipo", required=True)
    
    
    
class project_noconformidad_causa(models.Model):
    _name = 'project.noconformidad.causa'

    name = fields.Char(string="Causa", required=True)
    
    
    
        
class project_noconformidad(models.Model):
    _name = 'project.noconformidad'
    _inherit = ['mail.thread']
    
    sequence_name = fields.Char("Número", readonly=True, default=lambda self: "/")
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sequence_name', '/') == '/':
                vals['sequence_name'] = self.env['ir.sequence'].next_by_code(
                    'project.noconformidad'
                )
        return super().create(vals_list)
        
    @api.multi
    def name_get(self):
        # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
        self.browse(self.ids).read(['name', 'sequence_name'])
        return [(template.id, '%s%s' % (template.sequence_name and '[%s] ' % template.sequence_name or '', template.name))
                for template in self]
    
    
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)
    
    name = fields.Char(string="Título", required=True)
    type_id = fields.Many2one('project.noconformidad.type', string="Tipo", required=True)
    causa_id = fields.Many2one('project.noconformidad.causa', string="Causa", required=False)
    user_id = fields.Many2one('res.users', string="Abierta por", default=lambda self: self.env.user, required=True)
    product_id = fields.Many2one('product.template', string="Pieza")
    date_open = fields.Date(string="Fecha apertura", default=fields.Date.today(), required=True)
    PRIORIDADES = [('0','Baja'),   
                     ('1','Media'),
                     ('2','Alta'),
                     ('3','Muy Alta'),
                     ]
    priority = fields.Selection(selection=PRIORIDADES, string='Prioridad')
    ESTADOS = [('0','En espera'),   
                 ('1','En ejecución'),
                 ('2','Resuelto'),
                 ('3','Cancelado'),
                 ]
    state = fields.Selection(selection=ESTADOS, string='Estado', default='0')
    project_id = fields.Many2one('project.project', string="Proyecto")
    escandallo_id = fields.Many2one('project.escandallo', string="Pieza escandallo", domain = "[('project_id','=',project_id)]")
    task_id = fields.Many2one('project.task', string="Tarea")
    assigned_id = fields.Many2one('res.users', string="Asignado a (Usuario)")
    assigned_partner_id = fields.Many2one('res.partner', string="Asignado a")
    date_close = fields.Date(string="Fecha cierre")
    
    coste_materiales = fields.Float(string="Coste materiales")
    coste_subcontratacion = fields.Float(string="Coste subcontratación")
    num_horas = fields.Float(compute='_compute_coste_horas', string="Num de horas")
    coste_horas = fields.Float(compute='_compute_coste_horas', string='Coste horas')
    
    description = fields.Html(string="Descripción de la NC")
    causas = fields.Text(string="Causas de la NC")

    accion_correctiva = fields.Html(string="Acciones correctivas")
    date_accion_correctiva = fields.Date(string="Fecha acciones correctivas")
    responsable_accion_correctiva = fields.Many2one('res.users', string="Responsable acciones correctivas (usuario)")
    responsable_accion_correctiva_partner = fields.Many2one('res.partner', string="Responsable acciones correctivas")
    
    accion_preventiva = fields.Html(string="Acciones preventivas")
    date_accion_preventiva = fields.Date(string="Fecha acciones preventivas")
    responsable_accion_preventiva = fields.Many2one('res.users', string="Responsable acciones preventivas (Usuario)")
    responsable_accion_preventiva_partner = fields.Many2one('res.partner', string="Responsable acciones preventivas")
    
    coste_total = fields.Float(compute='_compute_coste_total', string='Coste total')
    
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_noconformidad_attach_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Adjuntos")
    
    @api.depends('coste_materiales', 'coste_subcontratacion', 'num_horas')
    def _compute_coste_total(self):
        for record in self:
            record.coste_total = record.coste_materiales + record.coste_subcontratacion + record.coste_horas
            
    @api.depends('name')
    def _compute_coste_horas(self):
        for record in self:

            coste_hora = record.company_id.coste_hora
            num_horas = 0.0
            
            for elem in self.env['hr.timesheet.employee'].search([('noconformidad_id', '=', record.id)]):
                num_horas = num_horas + elem.horas_presenciales + elem.horas_no_presenciales
                
            record.num_horas = num_horas
            record.coste_horas = num_horas * coste_hora
    
    
    
    