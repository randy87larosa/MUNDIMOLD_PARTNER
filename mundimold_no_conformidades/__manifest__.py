# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "No conformidades Mundimold",
    "summary": "Registro de no conformidades",
    'version': '12.0.1.0.0',
    "category": "Project",
    "website": "www.indaws.es",
    "author": "INDAWS",

    "license": "AGPL-3",
    'application': False,
    'installable': True,
    'auto_install': False,
    "depends": [
        "sale",
        "product",
        "project",
        "mundimold_escandallo",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/view.xml",
        "reports/qweb/report_noconformidad.xml",
        "reports/mundimold_report.xml",
    ],

}
