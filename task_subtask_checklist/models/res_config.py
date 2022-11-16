from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    checklist_allow_reset_after_completed = fields.Boolean("Allow Reset Activity After Completed", help="User can reset activity from Done To TODO")
    checklist_allow_reset_after_canceled = fields.Boolean("Allow Reset Activity After Canceled", help="User can reset activity from Canceled To TODO")
    group_checklist_task_progress_restriction = fields.Selection([
        (0, 'No Restriction To Task Progress'),
        (1, 'Restrict Task Progress Before All Checklist Completion')
    ], "Task Progress Restriction", implied_group='task_subtask_checklist.group_checklist_task_progress_restriction',
        help="Restrict Task Progress Before All Checklist Either Canceled Or Completed.")

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        Param = self.env['ir.config_parameter'].sudo()
        Param.set_param("task_subtask_checklist.checklist_allow_reset_after_completed", (self.checklist_allow_reset_after_completed or False))
        Param.set_param("task_subtask_checklist.checklist_allow_reset_after_canceled", (self.checklist_allow_reset_after_canceled or False))

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            checklist_allow_reset_after_completed=params.get_param('task_subtask_checklist.checklist_allow_reset_after_completed', default=False),
            checklist_allow_reset_after_canceled=params.get_param('task_subtask_checklist.checklist_allow_reset_after_canceled', default=False),
        )
        return res
