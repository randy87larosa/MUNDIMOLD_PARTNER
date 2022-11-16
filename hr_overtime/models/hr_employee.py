# -*- coding: utf-8 -*-

from odoo import api, fields, models

class HrEmployee(models.Model):
    _inherit = "hr.employee"
    _description = "Employee"

    attendance_max_length = fields.Float(string='Duración máxima jornada')
