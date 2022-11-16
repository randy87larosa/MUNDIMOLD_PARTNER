# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Escandallo de compras Mundimold",
    "summary": "Escandallo de compras en proyectos",
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
        "mundimold_project_planning"

    ],
    "data": [
        "security/ir.model.access.csv",
        "views/project.xml",
        "views/purchase.xml",
        "views/product.xml",
        "views/picking.xml",
        "reports/qweb/report_escandallo.xml",
        "reports/mundimold_report.xml",
    ],

}
