# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Crear proyecto desde pedido",
    "summary": "Ampliaciones de pedidos y proyectos",
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
        "project",
        "account",
        "mundimold_mundimold"
    ],
    "data": [
        "views/sale.xml",
    ],

}
