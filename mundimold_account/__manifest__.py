# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Ampliaciones Contabilidad Mundimold",
    "summary": "Ampliaciones Contabilidad Mundimold",
    'version': '11.0.1.0.0',
    "category": "Account",
    "website": "www.indaws.es",
    "author": "INDAWS",

    "license": "AGPL-3",
    'application': False,
    'installable': True,
    'auto_install': False,
    "depends": [
        "account",
        "account_due_list"
    ],
    "data": [

        "views/account.xml",
        "views/invoice.xml",


    ],

}
