# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Cotizaciones Mundimold",
    "summary": "Generar ofertas de moldes",
    'version': '12.0.1.0.0',
    "category": "Sale",
    "website": "www.visiion.net",
    "author": "VISIION",

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
        "views/sale_cotizacion.xml",
        "views/res_partner.xml",
        "reports/qweb/report_sale_cotizacion.xml",
        "reports/mundimold_report.xml",
    ],

}
