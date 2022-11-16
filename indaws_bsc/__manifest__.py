# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'BSC - Sistema de indicadores',
    'version': '12.0.1.0.0',
    'author': 'inDAWS',
    'category': 'Tools',
    'depends': [ 'base', 'account' ],
    'demo': [],
    'data': [
            'security/bsc_security.xml',
            'security/ir.model.access.csv',
            'wizard/bsc_kpi_calcular_view.xml',
            'views/bsc_view.xml',
            'reports/qweb/report_bsc_kpi.xml',
            'reports/qweb/report_bsc_period.xml',
            'reports/bsc_report.xml',
              ],
    'installable': True,
    'sequence': 1,
    'application': True,
    'auto_install': False,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
