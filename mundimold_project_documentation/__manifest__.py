# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Documentación de proyectos",
    "summary": "Gestión documental en proyectos",
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
        "crm",
        "project",
        "product",
        "mundimold_moldrent",
        "mundimold_partner_adapt"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/project.xml",
        "views/sale_order.xml",
        "views/crm_lead.xml",
    ],

}
