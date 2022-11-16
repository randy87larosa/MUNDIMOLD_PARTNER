# -*- coding: utf-8 -*-
{
    'name': "Calculate Employee Overtime",

    'summary': """
        calculate employee overtime""",

    'description': """
        This module compute extra time worked by an employee in different lists. 
        and each employee has a maximum amount of time that they work (eg 8 hours per day), 
        and if they work more than that time, it is counted as overtime.
    """,
    'author': "inDAWS",
    'website': "http://www.indaws.es",
    'category': 'hr',
    'version': '12.0.1.0.0',
    'sequence': 1,
    'installable': True,
    'application': False,
    'auto_install': False,
    'depends': ['hr_attendance','hr_timesheet'],
    'data': [
        'views/hr_employee_views.xml',
        'views/hr_attendance_views.xml',
        'data/overtime_data.xml',
    ],
}