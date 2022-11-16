# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Ampliaciones Mundimold ficha del producto",
    "summary": "Ampliaciones para Mundimold",
    'version': '12.0.1.0.0',
    "category": "Product",
    "website": "www.visiion.net",
    "author": "VISIION",

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
        "views/product.xml",
        "views/moldrent.xml",
        "views/layout_hrader.xml"
    ],

}
