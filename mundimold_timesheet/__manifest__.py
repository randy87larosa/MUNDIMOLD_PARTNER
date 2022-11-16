# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Registro de horas Mundimold",
    "summary": "Registro de horas Mundimold",
    'version': '12.0.1.0.0',
    "category": "Project",
    "website": "www.indaws.es",
    "author": "INDAWS",

    "license": "AGPL-3",
    'application': False,
    'installable': True,
    'auto_install': False,
    "depends": [
        "hr_timesheet",
        "mrp",
        "project",
        "mundimold_no_conformidades",
        "mundimold_hr",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_timesheet.xml",
    ],

}
