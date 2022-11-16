# Copyright 2019 Patrick Wilson <patrickraymondwilson@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProjectTemplate(models.Model):
    _inherit = 'project.project'

    def create_project_from_template(self):
        res = super().create_project_from_template()
        new_project = self.env['project.project'].browse(res['res_id'])
        old_project = self.env['project.project'].search([('name', '=', new_project.name.replace("(COPY)", "(TEMPLATE)"))])[0]
        
        
        for new_task_record in new_project.task_ids:
            for old_task_record in old_project.task_ids:
                if new_task_record.name == old_task_record.name:
                    for resource in old_task_record.task_resource_ids:
                        new_res_id = self.env['project.task.resource.link'].create({'task_id': new_task_record.id, 
                                               'resource_id': resource.resource_id.id,
                                               'load_factor': resource.load_factor,
                                               'load_control': resource.load_control,
                                             })
                                             
                    for pred in old_task_record.predecessor_ids:
                    
                        parent_task = self.env['project.task'].search([('name', '=', pred.parent_task_id.name), ('project_id', '=', new_project.id)])[0]
                        new_pred_id = self.env['project.task.predecessor'].create({'task_id': new_task_record.id, 
                                               'parent_task_id': parent_task.id,
                                               'type': pred.type,
                                               'lag_qty': pred.lag_qty,
                                               'lag_type': pred.lag_type,
                                             })
        
        return res
