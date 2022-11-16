# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Ampliaciones tesorería Mundimold",
    "summary": "Planificación de tesorería avanzada",
    'version': '12.0.1.0.0',
    "category": "Project",
    "website": "www.visiion.net",
    "author": "VISIION",

    "license": "AGPL-3",
    'application': False,
    'installable': True,
    'auto_install': False,
    "depends": [
        "sale",
        "product",
        "mundimold_project_invoicing",
        "mundimold_escandallo",
        "treasury_forecast"
    ],
    "data": [
        "security/tesoreria_security.xml",
        "security/ir.model.access.csv",
        "views/bank_statement.xml",
        "views/report_tesoreria.xml",
    ],

}
