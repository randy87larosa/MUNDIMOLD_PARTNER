from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ChecklistActivityStages(models.Model):
    _name = 'checklist.activity.stages'
    _description = 'Checklist Activity Stages'
    _order = "sequence, name, id"

    name = fields.Char()
    sequence = fields.Integer(help='Sequence must be between 2 to 20\nsome sequences are reserved like\n'
                                   '1 for TODO\n21 for Completed\n22for Canceled', default=1, required=True)
    default_stage = fields.Selection([('TODO', 'TODO'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], readonly=0)

    _sql_constraints = [
        ('sequence_uniq', 'unique(sequence)', 'Stage with same sequence is already available!'),
        ('default_stage_uniq', 'unique(default_stage)', 'Stage with same default stage is already available!'),
        ('sequence_check', 'check(sequence >= 1 and sequence <= 22)', 'Sequence should be greater than onr and less than 21 !'),
    ]

    @api.onchange('default_stage')
    def onchange_next_activity_id(self):
        if self.default_stage == 'TODO':
            self.sequence = 1
        elif self.default_stage == 'Completed':
            self.sequence = 21
        elif self.default_stage == 'Canceled':
            self.sequence = 22


class ChecklistActivities(models.Model):
    _inherit = 'mail.thread'
    _name = 'checklist.activities'
    _description = 'Checklist Activities'

    def _default_stage_id(self):
        stage_id = self.env['checklist.activity.stages'].search([('default_stage', '=', 'TODO')], limit=1)
        return stage_id.id if stage_id.id else None

    name = fields.Char(track_visibility='onchange')
    sequence = fields.Integer(default=1)
    description = fields.Char(track_visibility='onchange')
    completed = fields.Boolean()
    canceled = fields.Boolean()
    progress = fields.Boolean()
    task_id = fields.Many2one('project.task', string='Task')
    project_id = fields.Many2one('project.project', string='Project', related='task_id.project_id', store=True)
    activity_stage_id = fields.Many2one('checklist.activity.stages', string='Stage', track_visibility='onchange',
                                        index=True, default=lambda self: self._default_stage_id())
    default_stage = fields.Selection(related='activity_stage_id.default_stage', string='Default Stage', readonly=True)
    approve_user_id = fields.Many2one('res.users', string='Approve User', track_visibility='onchange',
                                      default=lambda self: self.env.user.id)
    can_reset_after_completed = fields.Boolean(compute='_compute_check_reset_after_completed', multi='checklist_setting')
    can_reset_after_canceled = fields.Boolean(compute='_compute_check_reset_after_completed', multi='checklist_setting')

    def _compute_check_reset_after_completed(self):
        Param = self.env['ir.config_parameter']
        for obj in self:
            obj.can_reset_after_completed = Param.sudo().get_param('task_subtask_checklist.checklist_allow_reset_after_completed')
            obj.can_reset_after_canceled = Param.sudo().get_param('task_subtask_checklist.checklist_allow_reset_after_canceled')

    @api.multi
    def approve_and_next_stage(self):
        for obj in self:
            if self.env.user == obj.approve_user_id:
                current_sequence = obj.activity_stage_id.sequence
                completed_id = self.env['checklist.activity.stages'].search([('default_stage', '=', 'Completed')], limit=1)
                next_id = self.env['checklist.activity.stages'].search([('sequence', '>', current_sequence)], order='sequence', limit=1)
                obj.write({
                    'completed': False if completed_id != next_id else True,
                    'canceled': False,
                    'progress': True if completed_id != next_id else False,
                    'activity_stage_id': next_id.id,
                })
            else:
                raise ValidationError(_('Only "%s" Can Approve This Record' % str(obj.approve_user_id.name)))

    @api.multi
    def mark_completed(self):
        for obj in self:
            if self.env.user == obj.approve_user_id:
                completed_stage = self.env['checklist.activity.stages'].search([('default_stage', '=', 'Completed')], limit=1)
                obj.write({
                    'completed': True,
                    'canceled': False,
                    'progress': False,
                    'activity_stage_id': completed_stage and completed_stage.id or None,
                })
            else:
                raise ValidationError(_('Only "%s" Can Approve This Record' % str(obj.approve_user_id.name)))

    @api.multi
    def mark_canceled(self):
        for obj in self:
            if self.env.user == obj.approve_user_id:
                canceled_stage = self.env['checklist.activity.stages'].search([('default_stage', '=', 'Canceled')], limit=1)
                obj.write({
                    'completed': False,
                    'canceled': True,
                    'progress': False,
                    'activity_stage_id': canceled_stage and canceled_stage.id or None,
                })
            else:
                raise ValidationError(_('Only "%s" Can Cancel This Record' % str(obj.approve_user_id.name)))

    @api.multi
    def reset_todo(self):
        for obj in self:
            if self.env.user == obj.approve_user_id:
                reset_stage = self.env['checklist.activity.stages'].search([('default_stage', '=', 'TODO')], limit=1)
                obj.write({
                    'completed': False,
                    'canceled': False,
                    'progress': False,
                    'activity_stage_id': reset_stage and reset_stage.id or None,
                })
            else:
                raise ValidationError(_('Only "%s" Can Reset This Record' % str(obj.approve_user_id.name)))


class ChecklistItem(models.Model):
    _name = 'checklist.item'
    _description = 'Checklist Item'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    description = fields.Char()
    checklist_id = fields.Many2one('task.checklist')


class TaskChecklist(models.Model):
    _name = 'task.checklist'
    _description = 'Task Checklist'

    name = fields.Char(required=True)
    description = fields.Char()
    project_id = fields.Many2one('project.project', string='Project',
                                 help='Select Project to use this checklist for project specific else its global')
    item_ids = fields.One2many('checklist.item', 'checklist_id', string='CheckList Items', required=True)


class Task(models.Model):
    _inherit = 'project.task'

    checklist_id = fields.Many2one('task.checklist', string='Checklist')
    checklist_activity_ids = fields.One2many('checklist.activities', 'task_id', string='Activity')
    activity_progress = fields.Float(compute='_compute_activity_progress', digits=(16, 2), string='Checklist Progress')

    @api.multi
    def _compute_activity_progress(self):
        for obj in self:
            total_completed = 0
            for activity in obj.checklist_activity_ids:
                if activity.activity_stage_id.default_stage in ['Canceled', 'Completed']:
                    total_completed += 1
            if total_completed:
                obj.activity_progress = float(total_completed) / len(obj.checklist_activity_ids) * 100
            else:
                obj.activity_progress = 0.0

    @api.onchange('checklist_id')
    def onchange_checklist_id(self):
        checklist_activity_ids = []
        for obj in self:
            for activity in obj.checklist_activity_ids:
                checklist_activity_ids.append((2, activity.id))
            default_stage_id = self.env['checklist.activity.stages'].search([('default_stage', '=', 'TODO')], limit=1)
            if obj.checklist_id:
                for activity in obj.checklist_id.item_ids:
                    checklist_activity_ids.append((0, 0, {
                        'sequence': activity.sequence,
                        'name': activity.name,
                        'description': activity.description,
                        'activity_stage_id': default_stage_id[0],
                        'approve_user_id': self.env.user,
                    }))
            obj.update({'checklist_activity_ids': checklist_activity_ids})
            if self._origin.checklist_id:
                return {'warning': {
                    'title': _('Warning!'),
                    'message': _('On Change Of Checklist ALl Old Activities Of This Task Will Replace By New One'),
                }}

    def check_restriction_setting(self, new_stage):
        if new_stage.checklist_task_progress_restriction:
            if self.env.user.has_group('task_subtask_checklist.group_checklist_task_progress_restriction'):
                return True
        return False

    @api.multi
    def write(self, vals):
        # Restrict stage change till all activity are either completed or cancelled
        if 'stage_id' in vals:
            for obj in self:
                new_stage = self.env['project.task.type'].browse(vals.get('stage_id'))
                if self.check_restriction_setting(new_stage):
                    activity_pending_list = []
                    for activity in obj.checklist_activity_ids:
                        if activity.completed or activity.canceled:
                            continue
                        else:
                            activity_pending_list.append(activity.name)
                    if activity_pending_list:
                        msg = "You Can Not change stage from %s to %s because following activities are not completed or not canceled for the task%s" % \
                              (obj.stage_id.name, new_stage.name, obj.name)
                        for pending in activity_pending_list:
                            msg += "\n" + pending
                        raise ValidationError(_(msg))

        return super(Task, self).write(vals)


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'
    checklist_task_progress_restriction = fields.Boolean('Checklist Task Progress Restriction')


class Project(models.Model):
    _inherit = 'project.project'
    activity_count = fields.Integer(compute='_compute_activity_count')

    @api.multi
    def _compute_activity_count(self):
        for obj in self:
            count = 0
            if self._context:
                ctx = self._context.copy()
            else:
                ctx = {}
            ctx['active_test'] = False
            for activity in self.env['checklist.activities'].with_context(ctx).search([('project_id', '=', obj.id)]):
                count += 1
            obj.activity_count = count
