# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Ampliaciones Mundimold",
    "summary": "Ampliaciones de Mundimold",
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
        "account",
        "account_asset_management"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/company.xml",
        "views/invoice.xml",
        "views/account.xml",
        "views/sale.xml",
        "views/report_mundimold_invoice.xml",
        "views/report_mundimold_invoice_document.xml",
        "views/report_mundimold_sale.xml",
        "views/report_mundimold_sale_document.xml",
        "views/report_mundimold_request.xml",
        "views/report_mundimold_request_document.xml",
        "views/report_mundimold_purchase.xml",
        "views/report_mundimold_purchase_document.xml",
        "reports/qweb/report_account_invoice_packing_list.xml",
        "reports/qweb/report_account_invoice_albaran.xml",
        "reports/mundimold_report.xml",
    ],

}
