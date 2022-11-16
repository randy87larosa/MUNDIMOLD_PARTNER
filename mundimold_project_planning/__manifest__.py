# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Ampliaciones planificación de proyectos",
    "summary": "Ampliaciones planificación de proyectos",
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
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/project.xml",
        "views/res_partner.xml",
        "views/resource.xml",
    ],

}
