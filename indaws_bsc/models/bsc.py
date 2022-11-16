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


from odoo import models, fields, api
from datetime import datetime
import time


class bsc_config(models.Model):
    _name = 'bsc.config'
    
    name = fields.Char(string="Nombre")
    actual = fields.Many2one('bsc.period', string="Periodo actual")
    verde = fields.Float(string="Verde")
    amarillo = fields.Float(string="Amarillo")
    min_date = fields.Date(string="Fecha actual")
    year = fields.Integer(string="Año")
    
    show_complete_year = fields.Boolean(string="Mostrar año completo")

    

bsc_config()


class bsc_categ(models.Model):
    _name = 'bsc.categ'
    _order = 'name'
    
    name = fields.Char(string="Nombre", required=True)

bsc_categ()


class bsc_uom(models.Model):
    _name = 'bsc.uom'
    _order = 'name'
    
    name = fields.Char(string="Nombre", required=True)
    
    @api.multi
    def test_func(self):
        return 4.2

bsc_uom()


class bsc_period(models.Model):
    _name = 'bsc.period'
    _order = 'date_ini'

    name = fields.Char(string="Nombre", required=True)
    date_ini = fields.Date(string="Desde", required=True)
    date_fin = fields.Date(string="Hasta", required=True)
    previous = fields.Many2one('bsc.period', string="Previo")
    year = fields.Integer(string="Año")
    date_ini_year = fields.Date(string="Fecha inicio año", required=True)

    line_ids = fields.One2many('bsc.kpi.line', 'period_id', string="Líneas")


    def num_days_inicio(self):
        dif = datetime.strptime(self.date_fin, '%Y-%m-%d') - datetime.strptime(self.date_ini_year, '%Y-%m-%d')
        return dif.days

bsc_period()


class bsc_kpi(models.Model):
    _name = 'bsc.kpi'
    _order = 'name'

    name = fields.Char(string="Nombre", required=True)
    color = fields.Integer(string="Color")
    categ_id = fields.Many2one('bsc.categ', string="Categoría", required=True)
    uom_id = fields.Many2one('bsc.uom', string="Unidad de medida", required=True)
    responsible_id = fields.Many2one('res.users', string="Responsable", required=True)
    description = fields.Text(string="Descripción")
    manual = fields.Boolean(string="Entrada de datos manual", default=False)
    is_acumulado = fields.Boolean(string="Indicador acumulado", default=False)
    type = fields.Selection([('I', 'Incremento'),('R', 'Reducción'),], string="Tipo", required=True)

    line_ids = fields.One2many('bsc.kpi.line', 'kpi_id', string="Líneas")




    difference_real_obj = fields.Float(digits=(6, 2), string="Dif (REAL - OBJ)", compute='_get_datos_kpi_line')
    percentage_real_obj = fields.Float(digits=(6, 0), string="Ptje (REAL - OBJ)", compute='_get_datos_kpi_line')

    difference_real_obj_acum = fields.Float(digits=(6, 2), string="Dif Acum (REAL - OBJ)", compute='_get_datos_kpi_line')
    percentage_real_obj_acum = fields.Float(digits=(6, 0), string="Ptje Acum (REAL - OBJ)", compute='_get_datos_kpi_line')

    difference_real_ant = fields.Float(digits=(6, 2), string="Dif (REAL - ANT)", compute='_get_datos_kpi_line')
    percentage_real_ant = fields.Float(digits=(6, 0), string="Ptje (REAL - ANT)", compute='_get_datos_kpi_line')

    difference_real_ant_acum = fields.Float(digits=(6, 2), string="Dif Acum (REAL - ANT)", compute='_get_datos_kpi_line')
    percentage_real_ant_acum = fields.Float(digits=(6, 0), string="Ptje Acum (REAL - ANT)", compute='_get_datos_kpi_line')


    #Mostrar
    show_difference_real_obj = fields.Boolean(string="Mostrar Dif (REAL - OBJ)", default=True)
    show_percentage_real_obj = fields.Boolean(string="Mostrar Ptje (REAL - OBJ)", default=True)

    show_difference_real_obj_acum = fields.Boolean(string="Mostrar Dif Acum (REAL - OBJ)", default=True)
    show_percentage_real_obj_acum = fields.Boolean(string="Mostrar Ptje Acum (REAL - OBJ)", default=True)

    show_difference_real_ant = fields.Boolean(string="Mostrar Dif (REAL - ANT)", default=True)
    show_percentage_real_ant = fields.Boolean(string="Mostrar Ptje (REAL - ANT)", default=True)

    show_difference_real_ant_acum = fields.Boolean(string="Mostrar Dif Acum (REAL - ANT)", default=True)
    show_percentage_real_ant_acum = fields.Boolean(string="Mostrar Ptje Acum (REAL - ANT)", default=True)


    #CALCULO VALORES
    sql = fields.Text(string="SQL")
    action_id = fields.Many2one('ir.actions.server', string="Acción")

    #OTROS
    period_id = fields.Many2one('bsc.period', string="Periodo", compute='_get_datos_periodo')


    @api.depends('line_ids')
    def _get_datos_periodo(self):
        for record in self:
            for elem in self.env['bsc.config'].search([]):
                if elem.actual:
                    period_id = elem.actual.id

                    record.period_id = period_id


    @api.depends('line_ids')
    def _get_datos_kpi_line(self):
        for record in self:

            difference_real_obj = 0.0
            percentage_real_obj = 0.0

            difference_real_obj_acum = 0.0
            percentage_real_obj_acum = 0.0
            difference_real_ant = 0.0
            percentage_real_ant = 0.0
            difference_real_ant_acum = 0.0
            percentage_real_ant_acum = 0.0
            period_id = None

            for elem in self.env['bsc.config'].search([]):
                if elem.actual:
                    period_id = elem.actual.id

            if period_id:
                for elem in self.env['bsc.kpi.line'].search([('kpi_id', '=', record.id), ('period_id', '=', period_id)]):
                    difference_real_obj = elem.difference_real_obj
                    percentage_real_obj = elem.percentage_real_obj

                    difference_real_obj_acum = elem.difference_real_obj_acum
                    percentage_real_obj_acum = elem.percentage_real_obj_acum
                    difference_real_ant = elem.difference_real_ant
                    percentage_real_ant = elem.percentage_real_ant
                    difference_real_ant_acum = elem.difference_real_ant_acum
                    percentage_real_ant_acum = elem.percentage_real_ant_acum

            record.difference_real_obj = difference_real_obj
            record.percentage_real_obj = percentage_real_obj

            record.difference_real_obj_acum = difference_real_obj_acum
            record.percentage_real_obj_acum = percentage_real_obj_acum
            record.difference_real_ant = difference_real_ant
            record.percentage_real_ant = percentage_real_ant
            record.difference_real_ant_acum = difference_real_ant_acum
            record.percentage_real_ant_acum = percentage_real_ant_acum

    @api.multi
    def create_lines_kpi(self):
        idp = []
        for p in self.line_ids:
            idp.append(p.period_id.id)

        for elem in self.env['bsc.period'].search([]):
            if not elem.id in idp:
                self.env['bsc.kpi.line'].create({'kpi_id':self.id, 'period_id':elem.id, 'target':0.0, 'real':0.0})


bsc_kpi()


class bsc_kpi_line(models.Model):
    _name = 'bsc.kpi.line'
    _order = 'date'

    kpi_id = fields.Many2one('bsc.kpi', string="Indicador", required=True)
    period_id = fields.Many2one('bsc.period', string="Periodo", required=True)
    date = fields.Date(string="Fecha", related="period_id.date_ini", store=True)
    manual = fields.Boolean(string="Entrada de datos manual", related="kpi_id.manual", store=True)


    target = fields.Float(string="Objetivo")
    real = fields.Float(string="Real")

    target_acum = fields.Float(digits=(6, 2), string="Objetivo acum", compute='_calc_datos_acum')
    real_acum = fields.Float(digits=(6, 2), string="Real acum", compute='_calc_datos_acum')

    real_ant = fields.Float(digits=(6, 2), string="Real ant", compute='_calc_datos_ant')
    real_ant_acum = fields.Float(digits=(6, 2), string="Real ant acum", compute='_calc_datos_ant')


    difference_real_obj = fields.Float(digits=(6, 2), string="Dif (REAL - OBJ)", compute='_calc_datos_kpi')
    percentage_real_obj = fields.Float(digits=(6, 0), string="Ptje (REAL - OBJ)", compute='_calc_datos_kpi')

    difference_real_obj_acum = fields.Float(digits=(6, 2), string="Dif Acum (REAL - OBJ)", compute='_calc_datos_kpi')
    percentage_real_obj_acum = fields.Float(digits=(6, 0), string="Ptje Acum (REAL - OBJ)", compute='_calc_datos_kpi')

    difference_real_ant = fields.Float(digits=(6, 2), string="Dif (REAL - ANT)", compute='_calc_datos_kpi')
    percentage_real_ant = fields.Float(digits=(6, 0), string="Ptje (REAL - ANT)", compute='_calc_datos_kpi')

    difference_real_ant_acum = fields.Float(digits=(6, 2), string="Dif Acum (REAL - ANT)", compute='_calc_datos_kpi')
    percentage_real_ant_acum = fields.Float(digits=(6, 0), string="Ptje Acum (REAL - ANT)", compute='_calc_datos_kpi')

    color_real_obj = fields.Char(string="Color", compute='_calc_datos_kpi')
    color_real_obj_acum = fields.Char(string="Color", compute='_calc_datos_kpi')
    color_real_ant = fields.Char(string="Color", compute='_calc_datos_kpi')
    color_real_ant_acum = fields.Char(string="Color", compute='_calc_datos_kpi')



    is_actual = fields.Boolean(string="Año actual", compute='_get_fechas_actual')



    def get_color(self, value):
        verde = 100.0
        amarillo = 66.0
        for elem in self.env['bsc.config'].search([]):
            verde = elem.verde
            amarillo = elem.amarillo
        if value >= verde:
            return 'green'
        if value < amarillo:
            return 'red'
        return 'orange'



    @api.depends('target', 'real')
    def _calc_datos_kpi(self):
        for record in self:

            #OBJETIVO
            record.difference_real_obj = record.real - record.target
            if record.kpi_id.type == 'R':
                record.difference_real_obj = record.target - record.real
            percentage_real_obj = 100.0

            if record.kpi_id.type == 'R':
                if record.real != 0.0:
                    percentage_real_obj = (record.target / record.real) * 100
            else:
                if record.target != 0.0:
                    percentage_real_obj = (record.real / record.target) * 100
            record.percentage_real_obj = percentage_real_obj
            record.color_real_obj = record.get_color(percentage_real_obj)

            #OBJETIVO ACUMULADO
            if record.kpi_id.is_acumulado == True:
                record.difference_real_obj_acum = record.difference_real_obj
                record.percentage_real_obj_acum = record.percentage_real_obj
                record.color_real_obj_acum = record.color_real_obj
            else:
                record.difference_real_obj_acum = record.real_acum - record.target_acum
                if record.kpi_id.type == 'R':
                    record.difference_real_obj_acum = record.target_acum - record.real_acum

                percentage_real_obj_acum = 100.0
                if record.kpi_id.type == 'R':
                    if record.real_acum != 0.0:
                        percentage_real_obj_acum = (record.target_acum / record.real_acum) * 100
                else:
                    if record.target_acum != 0.0:
                        percentage_real_obj_acum = (record.real_acum / record.target_acum) * 100

                record.percentage_real_obj_acum = percentage_real_obj_acum
                record.color_real_obj_acum = record.get_color(percentage_real_obj_acum)


            #ANTERIOR
            difference_real_ant = 0.0
            percentage_real_ant = 0.0
            ant = record._get_line_anterior()
            if ant:
                record.difference_real_ant = record.real - ant.real
                if record.kpi_id.type == 'R':
                    record.difference_real_ant = ant.real - record.real

                percentage_real_ant = 100.0
                if record.kpi_id.type == 'R':
                    if record.real != 0.0:
                        percentage_real_ant = (ant.real / record.real) * 100
                else:
                    if ant.real != 0.0:
                        percentage_real_ant = (record.real / ant.real) * 100

                record.percentage_real_ant = percentage_real_ant
            record.color_real_ant = record.get_color(percentage_real_ant)


            #ANTERIOR ACUMULADO
            difference_real_ant_acum = 0.0
            percentage_real_ant_acum = 0.0
            ant = record._get_line_anterior()

            if record.kpi_id.is_acumulado == True:
                difference_real_ant_acum = record.difference_real_ant
                percentage_real_ant_acum = record.percentage_real_ant
            else:
                if ant:
                    if record.kpi_id.type == 'R':
                        record.difference_real_ant = ant.real_acum - record.real_acum
                    record.difference_real_ant_acum = record.real_acum - ant.real_acum

                    percentage_real_ant_acum = 100.0
                    if record.kpi_id.type == 'R':
                        if record.real_acum != 0.0:
                            percentage_real_ant_acum = (ant.real_acum / record.real_acum) * 100
                    else:
                        if ant.real_acum != 0.0:
                            percentage_real_ant_acum = (record.real_acum / ant.real_acum) * 100

                    record.percentage_real_ant_acum = percentage_real_ant_acum
            record.color_real_ant_acum = record.get_color(percentage_real_ant_acum)




    @api.depends('target', 'real')
    def _calc_datos_acum(self):
        for record in self:

            target_acum = 0.0
            real_acum = 0.0

            if record.kpi_id.is_acumulado == True:
                target_acum = record.target
                real_acum = record.real

            else:
                for elem in self.env['bsc.kpi.line'].search([('kpi_id', '=', record.kpi_id.id), ('period_id.date_ini', '<=', record.period_id.date_ini), ('period_id.year', '=', record.period_id.year)]):
                        target_acum = target_acum + elem.target
                        real_acum = real_acum + elem.real


            record.target_acum = target_acum
            record.real_acum = real_acum


    @api.depends('period_id')
    def _get_line_anterior(self):
        for record in self:

            if record.period_id.previous:
                for elem in self.env['bsc.kpi.line'].search([('kpi_id', '=', record.kpi_id.id), ('period_id', '=', record.period_id.previous.id)]):
                    return elem

            return None


    @api.depends('period_id', 'real')
    def _calc_datos_ant(self):
        for record in self:
            ant = record._get_line_anterior()
            real_ant = 0.0
            real_ant_acum = 0.0
            if ant:
                real_ant = ant.real
                real_ant_acum = ant.real_acum
            record.real_ant = real_ant
            record.real_ant_acum = real_ant_acum

    @api.depends('period_id', 'date')
    def _get_fechas_actual(self):
        for record in self:
            fecha = None
            fecha_max = None
            is_actual = True
            show_complete_year = True

            for elem in self.env['bsc.config'].search([]):
                if elem.actual:
                    fecha = elem.actual.date_ini_year
                    fecha_max = elem.actual.date_ini
                    show_complete_year = elem.show_complete_year

            if fecha:
                if record.period_id.date_ini >= fecha:
                    is_actual = True
                else:
                    is_actual = False

                if show_complete_year == False:
                    if record.period_id.date_ini > fecha_max:
                        is_actual = False

            record.is_actual = is_actual

bsc_kpi_line()




class account_account(models.Model):
    _name = 'account.account'
    _inherit = 'account.account'


    @api.multi
    def _get_balance_account(self, code, start_date, end_date, debitcredit):

        result = 0.0

        sql = "SELECT SUM(l.debit) AS debit, SUM(l.credit) AS credit "
        sql += "FROM account_account a "
        sql += "INNER JOIN account_move_line l ON a.id=l.account_id "
        sql += "WHERE a.code LIKE '" + code + "' "

        if start_date:
            sql += "and l.date >= '" + str(start_date) + "' "

        if end_date:
            sql += "and l.date <= '" + str(end_date) + "' "

        self.env.cr.execute(sql)
        for att in self.env.cr.dictfetchall():
            if att["debit"] or att["credit"]:
                if debitcredit:
                    result = att["debit"] - att["credit"]
                else:
                    result = att["credit"] - att["debit"]
        return result


account_account()






# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: