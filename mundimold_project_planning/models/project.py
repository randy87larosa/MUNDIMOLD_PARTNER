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
import dateutil.relativedelta
from odoo.osv import expression

import logging
#Get the logger
_logger = logging.getLogger(__name__)
from datetime import datetime


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    project_id = fields.Many2one('project.project', string="Proyecto")
    escandallo_project_id = fields.Many2one('account.analytic.account', string="Proyecto escandallo", related="purchase_id.project_id")
    albaran_proveedor = fields.Char("Num albarán proveedor")


class project_project(models.Model):
    _name = 'project.project'
    _inherit = 'project.project'
    
    sequence_name = fields.Char("Cod proyecto", readonly=False, default=lambda self: "/")
    
    project_original_id = fields.Many2one('project.project', string="Proyecto original")

        
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sequence_name', '/') == '/':
                vals['sequence_name'] = self.env['ir.sequence'].next_by_code(
                    'project.project'
                )
        return super().create(vals_list)
        
        
    @api.multi
    def name_get(self):
        # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
        self.browse(self.ids).read(['name', 'sequence_name'])
        return [(template.id, '%s%s' % (template.sequence_name and '[%s] ' % template.sequence_name or '', template.name))
                for template in self]
                
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        """Include sequence_name name in direct name search."""
        args = expression.normalize_domain(args)
        for arg in args:
            if isinstance(arg, (list, tuple)):
                if arg[0] == 'name' or arg[0] == 'sequence_name':
                    index = args.index(arg)
                    args = (
                        args[:index] + ['|', ('sequence_name', arg[1], arg[2])] +
                        args[index:]
                    )
                    break
        return super(project_project, self).search(
            args, offset=offset, limit=limit, order=order, count=count,
        )
                

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        arg = args or []
        domain = []
        if name:
            #domain = ['|', ('name', operator, name), ('sequence_name', operator, name)]
            project_ids = self._search(['|', ('name', operator, name), ('sequence_name', operator, name)] + args, limit=limit, access_rights_uid=name_get_uid)
        else:
            project_ids = self._search(args, limit=limit, access_rights_uid=name_get_uid)
        return self.browse(project_ids).name_get()
    
    
    en_planificacion = fields.Boolean(string='En planificación', default=False)
    
    #cargar plantilla
    date_t1 = fields.Datetime(string='Fecha T1')
    date_inicio = fields.Date(string='Fecha de inicio proyecto')
    date_entrega = fields.Date(string='Fecha recepción molde')
    load_project_id = fields.Many2one('project.project', string='Copiar tareas de')
    
    @api.multi
    def cargar_plantilla_tareas(self): 
        for record in self:
        
            if len(record.task_ids) > 0:
                raise UserError("Error: El proyecto tiene tareas asociadas. Es necesario borrar las tareas existentes antes")
            elif not record.load_project_id:
                raise UserError("Error: No se ha seleccionado un proyecto para copiar las tareas")
                
            else:
            
                #copiamos las tareas
                for old_task_record in record.load_project_id.task_ids:
                    new_task_record = old_task_record.copy()
                    new_task_record.project_id = record.id
                    new_task_record.name = old_task_record.name
                    
                    if "PRUEBA DE MOLDE T1" in old_task_record.name:
                        new_task_record.constrain_type = 'mfo'
                        new_task_record.constrain_date = record.date_t1
                        
                        
                for old_task_record in record.load_project_id.task_ids:
                    new_task_record = self.env['project.task'].search([('project_id', '=', record.id), ('name', '=', old_task_record.name)])[0]
                    for resource in old_task_record.task_resource_ids:
                        new_res_id = self.env['project.task.resource.link'].create({'task_id': new_task_record.id, 
                                               'resource_id': resource.resource_id.id,
                                               'load_factor': resource.load_factor,
                                               'load_control': resource.load_control,
                                             })
                                             
                    #buscamos parent
                    if old_task_record.parent_id:
                        if len(self.env['project.task'].search([('project_id', '=', record.id), ('name', '=', old_task_record.parent_id.name)])) > 0:
                            new_parent = self.env['project.task'].search([('project_id', '=', record.id), ('name', '=', old_task_record.parent_id.name)])[0]
                            new_task_record.parent_id = new_parent.id
                                             
                    for pred in old_task_record.predecessor_ids:
                    
                        if len(self.env['project.task'].search([('name', '=', pred.parent_task_id.name), ('project_id', '=', record.id)])) > 0:
                            parent_task = self.env['project.task'].search([('name', '=', pred.parent_task_id.name), ('project_id', '=', record.id)])[0]
                            new_pred_id = self.env['project.task.predecessor'].create({'task_id': new_task_record.id, 
                                                   'parent_task_id': parent_task.id,
                                                   'type': pred.type,
                                                   'lag_qty': pred.lag_qty,
                                                   'lag_type': pred.lag_type,
                                                 })
                                             
                
                #ejecutamos scheduler
                _logger.error("FORWARD")
                record.scheduling_type = 'forward'
                record.date_start = record.date_t1 - dateutil.relativedelta.relativedelta(months=1)
                record.date_end = None
                record.task_ids[0]._scheduler_plan_start_calc(record)
                
                _logger.error("BACKWARD")
                record.scheduling_type = 'backward'
                record.date_start = None
                record.date_end = record.date_t1 + dateutil.relativedelta.relativedelta(days=7)
                record.task_ids[0]._scheduler_plan_start_calc(record)
                    


        
class project_task(models.Model):
    _name = 'project.task'
    _inherit = 'project.task'
    
    duartion_convert = fields.Float(string='Duración (conv)')
    
    duration_calc = fields.Float(string='Duración días (calculada)', compute='_compute_duracion',)
    
    @api.depends('duartion_convert', 'plan_duration')
    def _compute_duracion(self):
        for record in self:
            record.duration_calc = record.plan_duration / (60*60)

    
    @api.onchange('duartion_convert')
    def on_change_duartion_convert(self):
        
        if self.duartion_convert >= 0.0:
            self.plan_duration = int(self.duartion_convert * (60*60))

    
    @api.multi
    def action_subcontratar(self):
        
        view = self.env.ref('mundimold_project_planning.wizard_subcontratar_tarea_form_view')
        wiz = self.env['wizard.subcontratar.tarea'].create({'task_id': self.id})
        # TDE FIXME: a return in a loop, what a good idea. Really.
        return {
            'name': 'Subcontratar tareas',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.subcontratar.tarea',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': wiz.id,
            'context': self.env.context,
        }




class WizardSubcontratarTarea(models.TransientModel):
    _name = 'wizard.subcontratar.tarea'
    

    def _default_task(self):
        return self.env['project.task'].browse(self._context.get('active_id'))


    task_id = fields.Many2one('project.task', string='Tarea', default=_default_task, required=True, readonly=True)
    partner_id = fields.Many2one('res.partner', string='Proveedor', required=True)


    
    @api.multi
    def subcontratar_tareas(self): 
        for record in self:
        
            if not record.partner_id.resource_subco_id or record.partner_id.resource_subco_id == None:
                raise UserError("Error: El proveedor no tiene ningún recurso asociado")
        
            for resource in record.task_id.task_resource_ids:
                resource.resource_id = record.partner_id.resource_subco_id.id
                resource.load_control = 'no'
                
            for subtask in record.task_id.child_ids:
                for resource in subtask.task_resource_ids:
                    resource.resource_id = record.partner_id.resource_subco_id.id
                    resource.load_control = 'no'
                
        



#INFORME DE RECURSOS            
class project_resource_report(models.Model):
    _name = 'project.resource.report'
    
    
    resource_ids = fields.Many2many('resource.resource', string='Recursos')
    
    date_from = fields.Date(string='Desde')
    date_to = fields.Date(string='Hasta')
    mostrar = fields.Selection([('R', 'Real'),('T', 'Teórico'),('D', 'Diferencia'),], string="Tipo", required=True)
    departamentos = fields.Boolean(string='Mostrar departamentos')
    
    line_ids = fields.One2many('project.resource.report.line', 'report_id', string="Líneas informe", readonly=True)
    
    
    html_semanal = fields.Html(string='Informe semanal', compute='_compute_table',)
    html_mensual = fields.Html(string='Informe mensual', compute='_compute_table',)
    
    @api.depends('line_ids', 'mostrar', 'departamentos')
    def _compute_table(self):
        for record in self:
        
            record.html_semanal = record.tabla_informe('S')
            record.html_mensual = record.tabla_informe('M')
        
        
    def tabla_informe(self, type):
    
        html = ''
    
        html = html + '<table class="table">'
        html = html + '<thead>'
        html = html + '<tr>'
        
        html = html + '<th>'
        html = html + '<strong>Recurso</strong>'
        html = html + '</th>'
        
        ids_dates = []
        for line in self.env['project.resource.report.dates'].search([('type', '=', type),('date_from', '>=', self.date_from),('date_to', '<=', self.date_to)]):
            html = html + '<th>' + line.name + '</th>'
            ids_dates.append(line)
            
        html = html + '</tr>'
        html = html + '</thead>'
        html = html + '<tbody>'
        
        if self.departamentos == False:
            for resource in self.resource_ids:
            
                html = html + '<tr>'
                html = html + '<td>'
                html = html + '<strong>' + resource.name + '</strong>'
                html = html + '</td>'
                
                
                for dt in ids_dates:
                    style = ''
                    num = 0
                    
                    encontrado = False
                    for line in self.env['project.resource.report.line'].search([('report_id', '=', self.id),('resource_id', '=', resource.id),('date_id', '=', dt.id)]):
                    
                        encontrado = True
                    
                        if self.mostrar == "T":
                            num = line.teorico
                        elif self.mostrar == "R":
                            num = line.real
                        else:
                            num = line.diferencia

                        
                        style = ''
                        if line.diferencia < 0:
                            style = "style='background-color:#fa5555'"
                        if line.diferencia == 0:
                            style = "style='background-color:#f3f77c'"
                        break
                    
                    if encontrado == False:
                        teorico = resource.calendar_id.get_work_hours_count(datetime.combine(dt.date_from, datetime.min.time()), 
                                                                            datetime.combine(dt.date_to, datetime.min.time()), True)
                        teorico = teorico * resource.num_recursos
                        if self.mostrar != "R":
                            num = teorico
                        
                    html = html + '<td ' + style + '>'
                    if num!=0:
                        html = html + '<strong>' + str(round(num,1)) + '</strong>'
                    html = html + '</td>'

                html = html + '</tr>'
            
            
        else:
            for resource in self.resource_ids:
                if resource.is_departamento == True:
            
                    html = html + '<tr>'
                    html = html + '<td>'
                    html = html + '<strong>' + resource.name + '</strong>'
                    html = html + '</td>'
                    
                    
                    for dt in ids_dates:
                        style = ''
                        num = 0
                        encontrado = False
                        for line in self.env['project.resource.report.line'].search([('report_id', '=', self.id),
                                                                                    ('resource_id.nombre_departamento', '=', resource.nombre_departamento),
                                                                                    ('date_id', '=', dt.id)]):
                        
                            if self.mostrar == "T":
                                num = num + line.teorico
                            elif self.mostrar == "R":
                                num = num + line.real
                            else:
                                num = num + line.diferencia

                            encontrado = True
                            
                            style = ''
                            if line.diferencia < 0:
                                style = "style='background-color:#fa5555'"
                            if line.diferencia == 0:
                                style = "style='background-color:#f3f77c'"
 
                        
                        
                        if encontrado == False:
                            teorico = resource.calendar_id.get_work_hours_count(datetime.combine(dt.date_from, datetime.min.time()), 
                                                                            datetime.combine(dt.date_to, datetime.min.time()), True)
                            teorico = teorico * resource.num_recursos
                            if self.mostrar != "R":
                                num = teorico
                        
                            
                        html = html + '<td ' + style + '>'
                        if num!=0:
                            html = html + '<strong>' + str(round(num,1)) + '</strong>'
                        html = html + '</td>'

                    html = html + '</tr>'
            
        
        html = html + '</tbody>'
        html = html + '</table>'
        
        
        
        
        return html
    
    
    
    @api.multi
    def update_report(self):
        for record in self:
        
            self.env['project.resource.report.line'].search([('report_id', '=', record.id)]).unlink()
            _logger.warning("EMPEZANDO METODO")

            
            for detail in self.env['project.resource.report.dates'].search([]):
            
                _logger.warning("BUSCANDO POR FECHA")
                                                                       
                                                                       
                domain = [('data_from', '>=', detail.date_from),
                           ('data_to', '<=', detail.date_to),
                           ('task_id.active', '=', True)]
                           
                task_data = self.env['project.task.detail.plan'].read_group(
                    domain=domain, 
                    fields=['duration', 'resource_id'], 
                    groupby='resource_id')
                    
                for tk in task_data:

                    if tk["resource_id"]:
                        idrecurso = tk["resource_id"][0]
                        if idrecurso > 0:
                        
                            resource = self.env['resource.resource'].browse(idrecurso)
                            teorico = resource.calendar_id.get_work_hours_count(datetime.combine(detail.date_from, datetime.min.time()), 
                                                                                datetime.combine(detail.date_to, datetime.min.time()), True)
                            teorico = teorico * resource.num_recursos
                            real = tk["duration"] / (60*60)
                            self.env['project.resource.report.line'].create({'report_id': record.id,
                                                                             'date_id': detail.id,
                                                                             'teorico': round(teorico,1),
                                                                             'real': round(real,1),
                                                                             'diferencia': round(teorico - real,1),
                                                                             'resource_id': resource.id,
                                                                             
                                                                             })

                    
                

                #mapped_data = dict([(data['project_id'], data['project_id_count']) for data in task_data])
                #for data in mapped_data.values():
                #    tasks_count += data
                    
    
    


class project_resource_report_line(models.Model):
    _name = 'project.resource.report.line'
    
    report_id = fields.Many2one('project.resource.report', string='Informe')
    date_id = fields.Many2one('project.resource.dates', string='Fecha')
    resource_id = fields.Many2one('resource.resource', string='Recurso')
    
    teorico = fields.Float(string='Teórico')
    real = fields.Float(string='Real')
    diferencia = fields.Float(string='Diferencia')

   
    
#INFORME DE RECURSOS            
class project_resource_report_dates(models.Model):
    _name = 'project.resource.report.dates'
    
    name = fields.Char(string='Nombre')
    date_from = fields.Date(string='Desde')
    date_to = fields.Date(string='Hasta')
    type = fields.Selection([('S', 'Semana'),('M', 'Mes'),], string="Tipo", )
