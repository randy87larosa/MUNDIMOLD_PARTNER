from odoo import api, fields, models


class LeaveBulkApprove(models.TransientModel):
    _name = 'checklist.activities.approve.reject'
    skip_complete_cancel = fields.Boolean(string='Skip Records In Complete And Cancel State')

    @api.multi
    def approve_activity(self):
        if self._context.get('active_model') == 'checklist.activities' and self._context.get('active_ids'):
            activity_obj = self.env['checklist.activities']
            completed_stage = self.env['checklist.activity.stages'].search([('default_stage', '=', 'Completed')], limit=1)
            for obj in self:
                activities = activity_obj.browse(self._context.get('active_ids'))
                if obj.skip_complete_cancel:
                    for activity in activities:
                        if activity.activity_stage_id.default_stage in ['Completed', 'Canceled']:
                            continue
                        else:
                            activity.write({
                                'completed': True,
                                'canceled': False,
                                'progress': False,
                                'activity_stage_id': completed_stage and completed_stage.id or None
                            })
                else:
                    activities.write({
                        'completed': True,
                        'canceled': False,
                        'progress': False,
                        'activity_stage_id': completed_stage and completed_stage.id or None
                    })
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def refuse_activity(self):
        if self._context.get('active_model') == 'checklist.activities' and self._context.get('active_ids'):
            activity_obj = self.env['checklist.activities']
            canceled_stage = self.env['checklist.activity.stages'].search([('default_stage', '=', 'Canceled')], limit=1)
            for obj in self:
                activities = activity_obj.browse(self._context.get('active_ids'))
                if obj.skip_complete_cancel:
                    for activity in activities:
                        if activity.activity_stage_id.default_stage in ['Completed', 'Canceled']:
                            continue
                        else:
                            activity.write({
                                'completed': False,
                                'canceled': True,
                                'progress': False,
                                'activity_stage_id': canceled_stage and canceled_stage.id or None,
                            })
                else:
                    activities.write({
                        'completed': False,
                        'canceled': True,
                        'progress': False,
                        'activity_stage_id': canceled_stage and canceled_stage.id or None,
                    })
        return {'type': 'ir.actions.act_window_close'}
