# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime, timedelta

class HrAttendance(models.Model):
    _inherit = "hr.attendance"
    _description = "Attendance"

    extra_time_hour = fields.Datetime("Hora de salida ajustada")
    overtime = fields.Float(string='Horas extras')

    @api.model
    def action_compute_overtime(self):
        attendances = self.env['hr.attendance'].search([('id','in',self._context.get('active_ids'))])
        for attendance in attendances:
            total_time = attendance.check_out - attendance.check_in
            if float(total_time.seconds/(60*60)) > attendance.employee_id.attendance_max_length:
                attendance.extra_time_hour = attendance.check_out
                attendance.overtime = (float(total_time.seconds/(60*60)) - attendance.employee_id.attendance_max_length)
                attendance.check_out = attendance.check_out - timedelta(hours=attendance.overtime)
