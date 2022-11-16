# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Planificación de facturación en proyectos",
    "summary": "Planificación de facturas y cobros en proyectos",
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
        "mis_builder",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/project.xml",
    ],

}
