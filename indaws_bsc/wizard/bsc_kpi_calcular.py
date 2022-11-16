# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2012 Avanzosc <http://www.avanzosc.com>
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
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import date


class bsc_kpi_wizard_calc(models.TransientModel):
    _name = 'bsc.kpi.wizard.calc'
    _description = 'Calcular valores indicadores'
    
    def _default_kpi(self):
        return self.env['bsc.kpi'].browse(self._context.get('active_ids'))
        

    kpi_ids = fields.Many2many('bsc.kpi', string="Indicadores", default=_default_kpi)
    period_id = fields.Many2one('bsc.period', string="Periodo")
    period_ids = fields.Many2many('bsc.period', string="Periodos")
    
    
    @api.multi
    def calcular_valores_kpi(self):
    
        for kpi in self.kpi_ids:
            if self.period_id:
                self.calcular_valor_periodo(self.period_id, kpi)
            else:
                for period in self.period_ids:
                    self.calcular_valor_periodo(period, kpi)
            
        return {}
        
        
    def calcular_valor_periodo(self, period, kpi):
        if kpi.manual == False:
            result = 0.0
            
            if kpi.sql != False and kpi.sql != "":
                query = kpi.sql
                query = query.replace("DATEINICIAL", str(period.date_ini))
                query = query.replace("DATEFIN", str(period.date_fin))
                self.env.cr.execute(query)
                for att in self.env.cr.dictfetchall():
                    result = att["result"]
                if result != 0.0:
                    #comprobamos que no esta el kpi creado
                    lines = self.env['bsc.kpi.line'].search([('kpi_id', '=', kpi.id), ('period_id', '=', period.id)])
                    if len(lines) > 0:
                        lines[0].real = result
                    else:
                        self.env['bsc.kpi.line'].create({'kpi_id':kpi.id, 'period_id':period.id, 'target':0.0, 'real':result})
                        
            elif kpi.action_id:
                
                
                lines = self.env['bsc.kpi.line'].search([('kpi_id', '=', kpi.id), ('period_id', '=', period.id)])
                id_line = 0
                if len(lines) == 0:
                    newobj = self.env['bsc.kpi.line'].create({'kpi_id':kpi.id, 'period_id':period.id, 'target':0.0, 'real':0.0})
                    id_line = newobj.id
                else:
                    id_line = lines[0].id
                    
                ctx = dict(self.env.context or {})
                ctx.update({'active_id': id_line,})
                kpi.action_id.with_context(ctx).run()
    
    
bsc_kpi_wizard_calc()
    
    
