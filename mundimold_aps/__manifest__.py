# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Presupuestos Consultoría APS",
    "summary": "Presupuestos Consultoría APS",
    'version': '12.0.1.0.0',
    "category": "Sale",
    "website": "www.indaws.es",
    "author": "INDAWS",

    "license": "AGPL-3",
    'application': False,
    'installable': True,
    'auto_install': False,
    "depends": [
        "sale",
        "product",
        "crm",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_aps.xml",
    ],

}
