# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

{
    "name": "Mundimold Partner Adapt",
    "version": "1.0.0",
    "author": "Antonio Hermosilla <ahermosilla@visiion.net>",
    "license": "AGPL-3",
    "category": 'Partner',
    'website': 'www.visiion.net',
    'depends': [
        'base',
        'contacts',
    ],
    'external_dependencies': {
        # 'python': ['unidecode'],
    },
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'views/res_partner.xml',
    ],
    'qweb': [],
    'demo': [],
    'test': [],
    # 'post_init_hook': '_init_function',
    'installable': True,
    'auto_install': False,
}
