# -*- coding: utf-8 -*-
# © 2009 NetAndCo (<http://www.netandco.net>).
# © 2011 Akretion Benoît Guillot <benoit.guillot@akretion.com>
# © 2014 prisnet.ch Seraphine Lantible <s.lantible@gmail.com>
# © 2016 Serpent Consulting Services Pvt. Ltd.
# © 2018 Daniel Campos <danielcampos@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date
from odoo.exceptions import UserError, ValidationError
import calendar

        
class report_tesoreria_mundimold(models.Model):
    _name = 'report.tesoreria.mundimold'
    
    
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)
    
    date_ini = fields.Date(string="Fecha inicio", required=True)
    date_fin = fields.Date(string="Fecha fin", required=True)
    
    
    customer_account_id = fields.Many2one('account.account', string="Cuentas de clientes", required=True)
    customer_pagares_account_id = fields.Many2one('account.account', string="Cuentas de pagarés de clientes", required=False)
    supplier_account_id = fields.Many2one('account.account', string="Cuentas de proveedores", required=False)
    supplier_pagares_account_id = fields.Many2one('account.account', string="Cuentas de pagarés de proveedores", required=True)
    
    line_ids = fields.One2many('report.tesoreria.mundimold.line', 'report_id', string="Planificación facturación", readonly=True)
    pagares_ids = fields.One2many('report.tesoreria.mundimold.pagares', 'report_id', string="Dto pagarés", readonly=True)
    saldos_ids = fields.One2many('report.tesoreria.mundimold.saldos', 'report_id', string="Saldos iniciales")
    saldos_acumulados_ids = fields.One2many('report.tesoreria.mundimold.saldos.acumulados', 'report_id', string="Saldos acumulados")
    financiacion_ids = fields.One2many('report.tesoreria.mundimold.financiacion', 'report_id', string="Financiación")
    resumen_ids = fields.One2many('report.tesoreria.mundimold.resumen', 'report_id', string="Resumen financiación")
    
    incluir_vencidos_cliente = fields.Boolean(string="Incuir saldos vencidos clientes")
    incluir_vencidos_proveedor = fields.Boolean(string="Incuir saldos vencidos proveedores")
    incluir_vencidos_financiacion = fields.Boolean(string="Incuir saldos vencidos financ.")
    
    
    
    #ACCESOS
    bank_statement_id = fields.Many2one('account.bank.statement', string="Extracto tesorería")
    forecast_template_id = fields.Many2one('treasury.forecast.template', string="Platilla previsión mensual")
    forecast_1_id = fields.Many2one('treasury.forecast', string="Planificación mes 1")
    forecast_2_id = fields.Many2one('treasury.forecast', string="Planificación mes 2")
    forecast_3_id = fields.Many2one('treasury.forecast', string="Planificación mes 3")
    forecast_4_id = fields.Many2one('treasury.forecast', string="Planificación mes 4")
    
    
    #RESUMEN
    cobros_sin_asignar = fields.Float(string="Cobros sin asignar", readonly=True)
    pagos_sin_asignar = fields.Float(string="Pagos sin asignar", readonly=True)
    
    
    saldo_inicial = fields.Float(string="Saldo inicial", readonly=True)
    cobros = fields.Float(string="Cobros", readonly=True)
    pagos = fields.Float(string="Pagos", readonly=True)
    saldo_final = fields.Float(string="Saldo final", readonly=True)
    
    
            

            
    @api.multi
    def update_saldos_diarios(self):
        for record in self:
        
            self.env['report.tesoreria.mundimold.saldos.acumulados'].search([('report_id', '=', record.id)]).unlink()
            
            start_date = record.date_ini
            while start_date <= record.date_fin:
                
                
                semana = False
                mes = False
                if start_date == record.date_fin:
                    semana = True
                    mes = True
                    
                last_day_of_month = calendar.monthrange(start_date.year, start_date.month)[1]
                if start_date == date(start_date.year, start_date.month, last_day_of_month):
                    mes = True
                    
                if start_date.weekday() == 6:
                    semana = True
                
                for journal in self.env['report.tesoreria.mundimold.saldos'].search([('report_id', '=', record.id)]):
                
                    saldo_id = self.env['report.tesoreria.mundimold.saldos.acumulados'].create({'report_id': record.id, 
                                                                               'journal_id': journal.journal_id.id,
                                                                               'amount': 0.0,
                                                                               'date': start_date,
                                                                               'semana': semana,
                                                                               'mes': mes,
                                                                             })
                saldo_id = self.env['report.tesoreria.mundimold.saldos.acumulados'].create({'report_id': record.id, 
                                                                               'journal_id': None,
                                                                               'amount': 0.0,
                                                                               'date': start_date,
                                                                               'semana': semana,
                                                                               'mes': mes,
                                                                             })
                                                                             
                start_date += timedelta(days=1)
        
            for line in record.line_ids:
                journal_id = None
                if line.journal_id:
                    journal_id = line.journal_id.id
                elem = self.env['report.tesoreria.mundimold.saldos.acumulados'].search([('date', '=', line.date), ('journal_id', '=', journal_id)])
                if len(elem) > 0:
                    elem[0].amount = elem[0].amount + line.amount
                else:
                    elem = self.env['report.tesoreria.mundimold.saldos.acumulados'].search([('date', '=', line.date), ('journal_id', '=', None)])
                    if len(elem) > 0:
                        elem[0].amount = elem[0].amount + line.amount
                        
                        
            for journal in self.env['report.tesoreria.mundimold.saldos'].search([('report_id', '=', record.id)]):
            
                acumulado = 0.0
                for elem in self.env['report.tesoreria.mundimold.saldos.acumulados'].search([('report_id', '=', record.id), ('journal_id', '=', journal.journal_id.id)]):
                    acumulado = acumulado + elem.amount
                    elem.acumulado = acumulado
                    
            acumulado = 0.0
            for elem in self.env['report.tesoreria.mundimold.saldos.acumulados'].search([('report_id', '=', record.id), ('journal_id', '=', None)]):
                acumulado = acumulado + elem.amount
                elem.acumulado = acumulado
                    
                
            
    @api.multi
    def update_financiacion(self):
        for record in self:
            
            #LINEAS
            for financiacion in record.financiacion_ids:
                saldo_calculado = 0.0
                for line in self.env['report.tesoreria.mundimold.line'].search([('report_id', '=', record.id),('name', '=', financiacion.name)]):
                    saldo_calculado = saldo_calculado + line.amount
                for line in self.env['report.tesoreria.mundimold.pagares'].search([('report_id', '=', record.id),('name', '=', financiacion.name)]):
                    saldo_calculado = saldo_calculado + line.amount
                financiacion.saldo_calculado = saldo_calculado * (-1)
                financiacion.diferencia = financiacion.amount - financiacion.saldo_calculado
                
            #LINEAS
            for resumen in record.resumen_ids:
                saldo_calculado = 0.0
                amount = 0.0
                for line in self.env['report.tesoreria.mundimold.financiacion'].search([('report_id', '=', record.id),('name', 'like', resumen.name)]):
                    saldo_calculado = saldo_calculado + line.saldo_calculado
                    amount = amount + line.amount
                resumen.saldo_calculado = saldo_calculado
                resumen.amount = amount
                resumen.diferencia = resumen.amount - resumen.saldo_calculado
            
            
   
    @api.multi
    def update_banks(self):
        for record in self:
        
            for saldo in record.saldos_ids:
                saldo.cobros = 0.0
                saldo.pagos = 0.0
            record.cobros_sin_asignar = 0.0
            record.pagos_sin_asignar = 0.0
            
            #LINEAS
            for line in record.line_ids:
                if 'SALDO' not in line.type:
                    encontrado = False
                    for saldo in record.saldos_ids:
                        if saldo.journal_id.id == line.journal_id.id:
                            if line.amount > 0.0:
                                saldo.cobros = saldo.cobros + line.amount
                            if line.amount < 0.0:
                                saldo.pagos = saldo.pagos + line.amount
                            encontrado = True
                            break
                    if encontrado == False:
                        if line.amount > 0.0:
                            record.cobros_sin_asignar = record.cobros_sin_asignar + line.amount
                        if line.amount < 0.0:
                            record.pagos_sin_asignar = record.pagos_sin_asignar + line.amount
                            
            #TOTALES
            saldo_inicial = 0.0
            cobros = 0.0
            pagos = 0.0
            for saldo in record.saldos_ids:
                saldo_inicial = saldo_inicial + saldo.amount
                cobros = cobros + saldo.cobros
                pagos = pagos + saldo.pagos
                saldo.saldo_final = saldo.amount + saldo.cobros + saldo.pagos
                
            record.saldo_inicial = saldo_inicial
            record.cobros = cobros + record.cobros_sin_asignar
            record.pagos = pagos + record.pagos_sin_asignar
            record.saldo_final = record.saldo_inicial + record.cobros + record.pagos
   
   
    @api.multi
    def update_report(self):
        for record in self:
            
            self.env['wizard.tesoreria.asignar.banco'].search([]).unlink()
            self.env['wizard.tesoreria.asignar.fecha'].search([]).unlink()
            self.env['wizard.tesoreria.eliminar.prevision'].search([]).unlink()
            self.env['report.tesoreria.mundimold.line'].search([('report_id', '=', record.id)]).unlink()
            self.env['report.tesoreria.mundimold.pagares'].search([('report_id', '=', record.id)]).unlink()
            
            if record.bank_statement_id:
                record.bank_statement_id.update_forecast_lines()
            
            
            #SALDOS INICIALES
            for saldo in record.saldos_ids:
                saldo_id = self.env['report.tesoreria.mundimold.line'].create({'report_id': record.id, 
                                                                               'name': 'SALDO INICIAL ' + saldo.journal_id.name, 
                                                                               'journal_id': saldo.journal_id.id,
                                                                               'amount': saldo.amount,
                                                                               'date': record.date_ini,
                                                                               'type': '12_SALDOS',
                                                                               'main_type': '02_SALDOS',
                                                                             })
        
            
            #BUSCAMOS PREVISIONES
            journal_id = None
            for journal in self.env['account.journal'].search([('treasury_planning', '=', True), ('company_id', '=', record.company_id.id)]):
                journal_id = journal
            if journal_id:
                bank_id = None
                for bank in self.env['account.bank.statement'].search([('journal_id', '=', journal_id.id),('state', '=', 'open')]):
                
                    for line in self.env['account.bank.statement.line'].search([('statement_id', '=', bank.id),
                                                                                #('date', '>=', record.date_ini),
                                                                                ('date', '<=', record.date_fin),
                                                                                #('cf_forecast', '=', True),
                                                                                ]):
                        partner_id = None
                        if line.partner_id:
                            partner_id = line.partner_id.id
                            
                        journal_payment_id = journal_id.id
                        if line.journal_payment_id:
                            journal_payment_id = line.journal_payment_id.id
                            
                        account_analytic_id = None
                        if line.account_analytic_id:
                            account_analytic_id = line.account_analytic_id.id
                            
                        type = '06_PREV_PAGO'
                        main_type = '01_PAGOS'
                        if line.amount > 0.0:
                            type = '01_PREV_COBRO'
                            main_type = '00_COBROS'
                            
                            if '[PRESTAMO]' in line.name:
                                type = '09_PRESTAMOS'
                            
                        else:
                            if '[IMPUESTOS]' in line.name:
                                type = '10_IMPUESTOS'
                            if '[PAGOS FIJOS]' in line.name:
                                type = '07_PAGOS_FIJOS'
                            if '[PERSONAL]' in line.name:
                                type = '08_PERSONAL'
                            if '[PRESTAMO]' in line.name:
                                type = '09_PRESTAMOS'
                            if '[LEASING]' in line.name:
                                type = '10_LEASING'
                            

                        date_rep = line.date
                        name = line.name
                        if not line.name or line.name == '' or line.name == False:
                            name = '-'
                        if line.date < record.date_ini:
                            date_rep = record.date_ini
                            name = name + ' (VENCIDO)'
                        
                        
                        #if line.cf_forecast == True:
                        line_id = self.env['report.tesoreria.mundimold.line'].create({'report_id': record.id, 
                                                                                  'name': name, 
                                                                                  'partner_id': partner_id, 
                                                                                  'journal_id': journal_payment_id,
                                                                                  'amount': line.amount,
                                                                                  'date': date_rep,
                                                                                  'type': type,
                                                                                  'account_analytic_id': account_analytic_id,
                                                                                  'bank_line_id': line.id,
                                                                                  'main_type': main_type,
                                                                                 })
            #BUSCAMOS APUNTES CLIENTES
            for line in self.env['account.move.line'].search([('account_id', '=', record.customer_account_id.id),
                                                            ('date_maturity', '>=', record.date_ini),
                                                            ('date_maturity', '<=', record.date_fin),
                                                            ('reconciled', '=', False),
                                                            ('debit', '>', 0.0),
                                                            ('company_id', '=', record.company_id.id),
                                                            ]):
                partner_id = None
                if line.partner_id:
                    partner_id = line.partner_id.id
                    
                journal_payment_id = None
                if line.journal_payment_id:
                    journal_payment_id = line.journal_payment_id.id
                else:
                    if line.payment_mode_id:
                        if len(line.payment_mode_id.variable_journal_ids) <= 1:
                            for bk in line.payment_mode_id.variable_journal_ids:
                                journal_payment_id = bk.id
                
                name = line.name
                if line.invoice_id:
                    name = line.invoice_id.number
                    
                account_analytic_id = None
                for apunte in line.move_id.line_ids:
                    if apunte.analytic_account_id:
                        account_analytic_id = apunte.analytic_account_id.id
                        break
                
                line_id = self.env['report.tesoreria.mundimold.line'].create({'report_id': record.id, 
                                                                              'name': name, 
                                                                              'partner_id': partner_id, 
                                                                              'journal_id': journal_payment_id,
                                                                              'amount': line.amount_residual,
                                                                              'date': line.date_maturity,
                                                                              'type': '00_FRA_COBRO',
                                                                              'main_type': '00_COBROS',
                                                                              'account_analytic_id': account_analytic_id,
                                                                              'move_line_id': line.id,
                                                                             })
                                                                             
            
            
            #BUSCAMOS APUNTES CLIENTES FACTURAS VENCIDAS
            if record.incluir_vencidos_cliente == True:
                for line in self.env['account.move.line'].search([('account_id', '=', record.customer_account_id.id),
                                                                ('date_maturity', '<', record.date_ini),
                                                                ('invoice_id', '!=', False),
                                                                ('reconciled', '=', False),
                                                                ('debit', '>', 0.0),
                                                                ('company_id', '=', record.company_id.id),
                                                                ]):
                    partner_id = None
                    if line.partner_id:
                        partner_id = line.partner_id.id
                        
                    journal_payment_id = None
                    if line.journal_payment_id:
                        journal_payment_id = line.journal_payment_id.id
                    else:
                        if line.payment_mode_id:
                            if len(line.payment_mode_id.variable_journal_ids) <= 1:
                                for bk in line.payment_mode_id.variable_journal_ids:
                                    journal_payment_id = bk.id
                    
                    name = line.name
                    if not line.name or line.name == '' or line.name == False:
                        name = '-'
                    if line.invoice_id:
                        name = line.invoice_id.number + ' (VENCIDA)'
                        
                    account_analytic_id = None
                    for apunte in line.move_id.line_ids:
                        if apunte.analytic_account_id:
                            account_analytic_id = apunte.analytic_account_id.id
                            break
                    
                    line_id = self.env['report.tesoreria.mundimold.line'].create({'report_id': record.id, 
                                                                                  'name': name, 
                                                                                  'partner_id': partner_id, 
                                                                                  'journal_id': journal_payment_id,
                                                                                  'amount': line.amount_residual,
                                                                                  'date': record.date_ini,
                                                                                  'type': '00_FRA_COBRO',
                                                                                  'main_type': '00_COBROS',
                                                                                  'account_analytic_id': account_analytic_id,
                                                                                  'move_line_id': line.id,
                                                                                 })
            
            
            #BUSCAMOS APUNTES CLIENTES PAGARES
            
            lista_lines = []
            if record.customer_pagares_account_id.id:
                lista_lines = self.env['account.move.line'].search([('account_id', '=', record.customer_pagares_account_id.id),
                                                            ('date_maturity', '>=', record.date_ini),
                                                            ('date_maturity', '<=', record.date_fin),
                                                            ('reconciled', '=', False),
                                                            ('debit', '>', 0.0),
                                                            ('exclude_mis', '=', False),
                                                            ('company_id', '=', record.company_id.id),
                                                            ])
            else:
                lista_lines = self.env['account.move.line'].search([('account_id', 'like', '431%'),
                                                            ('date_maturity', '>=', record.date_ini),
                                                            ('date_maturity', '<=', record.date_fin),
                                                            ('reconciled', '=', False),
                                                            ('debit', '>', 0.0),
                                                            ('exclude_mis', '=', False),
                                                            ('company_id', '=', record.company_id.id),
                                                            ])
            
            for line in lista_lines:
                                                            
                
                partner_id = None
                if line.partner_id:
                    partner_id = line.partner_id.id
                    
                journal_payment_id = None
                if line.journal_payment_id:
                    journal_payment_id = line.journal_payment_id.id
                    
                name = line.name
                if not line.name or line.name == '' or line.name == False:
                    name = '-'
                    
                line_id = self.env['report.tesoreria.mundimold.line'].create({'report_id': record.id, 
                                                                              'name': name, 
                                                                              'partner_id': partner_id, 
                                                                              'journal_id': journal_payment_id,
                                                                              'amount': line.debit,
                                                                              'date': line.date_maturity,
                                                                              'type': '02_PAG_COBRO',
                                                                              'main_type': '00_COBROS',
                                                                              'move_line_id': line.id,
                                                                             })

                                                                             
            #BUSCAMOS APUNTES PROVEEDORES
            for line in self.env['account.move.line'].search([('account_id', '=', record.supplier_account_id.id),
                                                            ('date_maturity', '>=', record.date_ini),
                                                            ('date_maturity', '<=', record.date_fin),
                                                            ('reconciled', '=', False),
                                                            ('credit', '>', 0.0),
                                                            ('company_id', '=', record.company_id.id),
                
                                            ]):
                
                type = '04_FRA_PAGO_INTERNACIONAL'
                partner_id = None
                if line.partner_id:
                    partner_id = line.partner_id.id
                    if line.partner_id.country_id:
                        if line.partner_id.country_id.name == 'España':
                            type = '03_FRA_PAGO_NACIONAL'
                    
                journal_payment_id = None
                if line.journal_payment_id:
                    journal_payment_id = line.journal_payment_id.id
                else:
                    if line.payment_mode_id:
                        if len(line.payment_mode_id.variable_journal_ids) <= 1:
                            for bk in line.payment_mode_id.variable_journal_ids:
                                journal_payment_id = bk.id
                
                name = line.name
                if line.invoice_id:
                    name = line.invoice_id.number
                    if line.invoice_id.reference:
                        name = name + ' - ' + line.invoice_id.reference
                        
                
                account_analytic_id = None
                for apunte in line.move_id.line_ids:
                    if apunte.analytic_account_id:
                        account_analytic_id = apunte.analytic_account_id.id
                        break
                    

                
                
                line_id = self.env['report.tesoreria.mundimold.line'].create({'report_id': record.id, 
                                                                              'name': name, 
                                                                              'partner_id': partner_id, 
                                                                              'journal_id': journal_payment_id,
                                                                              'amount': line.amount_residual,
                                                                              'date': line.date_maturity,
                                                                              'type': type,
                                                                              'main_type': '01_PAGOS',
                                                                              'account_analytic_id': account_analytic_id,
                                                                              'move_line_id': line.id,
                                                                             })
                                                                             
            #BUSCAMOS APUNTES PROVEEDORES FACTURAS VENCIDAS
            if record.incluir_vencidos_proveedor == True:
                for line in self.env['account.move.line'].search([('account_id', '=', record.supplier_account_id.id),
                                                            ('date_maturity', '<', record.date_ini),
                                                            ('invoice_id', '!=', False),
                                                            ('reconciled', '=', False),
                                                            ('credit', '>', 0.0),
                                                            ('company_id', '=', record.company_id.id),
                                            ]):
                
                    type = '04_FRA_PAGO_INTERNACIONAL'
                    partner_id = None
                    if line.partner_id:
                        partner_id = line.partner_id.id
                        if line.partner_id.country_id:
                            if line.partner_id.country_id.name == 'España':
                                type = '03_FRA_PAGO_NACIONAL'
                        
                    journal_payment_id = None
                    if line.journal_payment_id:
                        journal_payment_id = line.journal_payment_id.id
                    else:
                        if line.payment_mode_id:
                            if len(line.payment_mode_id.variable_journal_ids) <= 1:
                                for bk in line.payment_mode_id.variable_journal_ids:
                                    journal_payment_id = bk.id
                    
                    name = line.name
                    if line.invoice_id:
                        name = line.invoice_id.number
                        if line.invoice_id.reference:
                            name = name + ' - ' + line.invoice_id.reference + ' (VENCIDA)'
                    if not line.name or line.name == '' or line.name == False:
                        name = '-'
                            
                    
                    account_analytic_id = None
                    for apunte in line.move_id.line_ids:
                        if apunte.analytic_account_id:
                            account_analytic_id = apunte.analytic_account_id.id
                            break
                        

                    
                    
                    line_id = self.env['report.tesoreria.mundimold.line'].create({'report_id': record.id, 
                                                                                  'name': name, 
                                                                                  'partner_id': partner_id, 
                                                                                  'journal_id': journal_payment_id,
                                                                                  'amount': line.amount_residual,
                                                                                  'date': record.date_ini,
                                                                                  'type': type,
                                                                                  'main_type': '01_PAGOS',
                                                                                  'account_analytic_id': account_analytic_id,
                                                                                  'move_line_id': line.id,
                                                                                 })


            
            #BUSCAMOS APUNTES PAGARES PROVEEDORES
            
            lista_lines = []
            if record.supplier_pagares_account_id.id:
                lista_lines = self.env['account.move.line'].search([('account_id', '=', record.supplier_pagares_account_id.id),
                                                            #('date_maturity', '>=', record.date_ini),
                                                            ('date_maturity', '<=', record.date_fin),
                                                            ('reconciled', '=', False),
                                                            ('credit', '>', 0.0),
                                                            ('exclude_mis', '=', False),
                                                            ('company_id', '=', record.company_id.id),
                                                            ])
            else:
                lista_lines = self.env['account.move.line'].search([('account_id', '=', record.supplier_pagares_account_id.id),
                                                            #('date_maturity', '>=', record.date_ini),
                                                            ('date_maturity', '<=', record.date_fin),
                                                            ('reconciled', '=', False),
                                                            ('credit', '>', 0.0),
                                                            ('exclude_mis', '=', False),
                                                            ('company_id', '=', record.company_id.id),
                                                            ])
            
            
            
            
            
            
            for line in lista_lines:
            
                partner_id = None
                if line.partner_id:
                    partner_id = line.partner_id.id
                    
                journal_payment_id = None
                if line.journal_payment_id:
                    journal_payment_id = line.journal_payment_id.id
                
                name = line.name
                if not line.name or line.name == '' or line.name == False:
                    name = '-'
                #if line.invoice_id:
                #    name = line.invoice_id.number
                    
                date_rep = line.date_maturity
                if line.date_maturity < record.date_ini:
                    date_rep = record.date_ini
                    name = name + ' (VENCIDO)'
                
                line_id = self.env['report.tesoreria.mundimold.line'].create({'report_id': record.id, 
                                                                              'name': name, 
                                                                              'partner_id': partner_id, 
                                                                              'journal_id': journal_payment_id,
                                                                              'amount': line.credit * (-1),
                                                                              'date': date_rep,
                                                                              'type': '05_PAG_PAGO',
                                                                              'main_type': '01_PAGOS',
                                                                              'move_line_id': line.id,
                                                                              
                                                                             })
                                                                             
                                                                             
            #BUSCAMOS APUNTES FINANCIACION
            for line in self.env['account.move.line'].search([('account_id.code', 'ilike', '5208%'),
                                                            #('date_maturity', '>=', record.date_ini),
                                                            ('date_maturity', '<=', record.date_fin),
                                                            ('reconciled', '=', False),
                                                            ('credit', '>', 0.0),
                                                            ('company_id', '=', record.company_id.id),
                                                            ]):
                partner_id = None
                if line.partner_id:
                    partner_id = line.partner_id.id
                    
                journal_payment_id = None
                if line.journal_payment_id:
                    journal_payment_id = line.journal_payment_id
                else:
                    journal_payment_id = line.move_id.journal_id
                    
                if journal_payment_id:
                    if journal_payment_id.id == 63:
                        journal_payment_id = self.env['account.journal'].search([('id', '=', '51')])[0]
                    
                    
                is_pagares = False
                name = '[FINANCIACION]'
                if 'Import' in line.account_id.name:
                    name = '[FINANCIACION] - LINEA IMPORT'
                elif 'Pagar' in line.account_id.name:
                    name = '[FINANCIACION] - DTO PAGARES'
                    is_pagares = True
                        
                else:
                    name = '[FINANCIACION] - CONFIRMING'
                    
                if journal_payment_id:
                    name = name + ' ' + journal_payment_id.name
                    
                date_rep = line.date_maturity
                
                incluido = True
                if line.date_maturity < record.date_ini:
                    date_rep = record.date_ini
                    #name = name + ' (VENCIDO)'
                    
                    if record.incluir_vencidos_financiacion == False:
                        incluido = False
                    
                
                if incluido == True:
                    if is_pagares == True:
                        line_id = self.env['report.tesoreria.mundimold.pagares'].create({'report_id': record.id, 
                                                                                      'name': name, 
                                                                                      'partner_id': partner_id, 
                                                                                      'journal_id': journal_payment_id.id,
                                                                                      'amount': line.credit * (-1),
                                                                                      'date': date_rep,
                                                                                      'move_line_id': line.id,
                                                                                     })
                    
                    else:
                        line_id = self.env['report.tesoreria.mundimold.line'].create({'report_id': record.id, 
                                                                                      'name': name, 
                                                                                      'partner_id': partner_id, 
                                                                                      'journal_id': journal_payment_id.id,
                                                                                      'amount': line.credit * (-1),
                                                                                      'date': date_rep,
                                                                                      'type': '11_FINANCIACION',
                                                                                      'main_type': '01_PAGOS',
                                                                                      'move_line_id': line.id,
                                                                                     })
            record.update_banks()
            record.update_saldos_diarios()
            record.update_financiacion()
                    

                    
class report_tesoreria_mundimold_saldos_acumulados(models.Model):
    _name = 'report.tesoreria.mundimold.saldos.acumulados'
    _order = 'date'
    
    report_id = fields.Many2one('report.tesoreria.mundimold', string="Tesorería", readonly=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)
    date = fields.Date(string="Fecha", readonly=True)
    journal_id = fields.Many2one('account.journal', string="Banco", readonly=True)
    amount = fields.Float(string="Importe", readonly=True)
    acumulado = fields.Float(string="Saldo final", readonly=True)
    semana = fields.Boolean(string="Semana", readonly=True)
    mes = fields.Boolean(string="Mes", readonly=True)
                    
                    
class report_tesoreria_mundimold_saldos(models.Model):
    _name = 'report.tesoreria.mundimold.saldos'
    
    report_id = fields.Many2one('report.tesoreria.mundimold', string="Tesorería", required=True)
    
    journal_id = fields.Many2one('account.journal', string="Banco", required=True)
    amount = fields.Float(string="Saldo inicial", required=True)
    
    cobros = fields.Float(string="Cobros", readonly=True)
    pagos = fields.Float(string="Pagos", readonly=True)
    saldo_final = fields.Float(string="Saldo final", readonly=True)
    
    
    
class report_tesoreria_mundimold_financiacion(models.Model):
    _name = 'report.tesoreria.mundimold.financiacion'
    
    report_id = fields.Many2one('report.tesoreria.mundimold', string="Tesorería", required=True)
    name = fields.Char(string="Concepto", required=True)
    amount = fields.Float(string="Límite", required=True)
    saldo_calculado = fields.Float(string="Consumido", readonly=True)
    diferencia = fields.Float(string="Disponible", readonly=True, compute="_get_valores")
    
    @api.depends('amount',)
    def _get_valores(self):
    
        for record in self:
            record.diferencia = record.amount - record.saldo_calculado
            
            
class report_tesoreria_mundimold_resumen(models.Model):
    _name = 'report.tesoreria.mundimold.resumen'
    
    report_id = fields.Many2one('report.tesoreria.mundimold', string="Tesorería", required=True)
    name = fields.Char(string="Concepto", required=True)
    amount = fields.Float(string="Límite", required=True)
    saldo_calculado = fields.Float(string="Consumido", readonly=True)
    diferencia = fields.Float(string="Disponible", readonly=True, compute="_get_valores")
    
    @api.depends('amount',)
    def _get_valores(self):
    
        for record in self:
            record.diferencia = record.amount - record.saldo_calculado



class report_tesoreria_mundimold_pagares(models.Model):
    _name = 'report.tesoreria.mundimold.pagares'
    _order = 'date'
    
    report_id = fields.Many2one('report.tesoreria.mundimold', string="Tesorería", required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)
    name = fields.Char(string="Concepto", required=True)
    partner_id = fields.Many2one('res.partner', string="Empresa")
    journal_id = fields.Many2one('account.journal', string="Diario de pago")
    amount = fields.Float(string="Importe", required=True)
    date = fields.Date(string="Fecha", required=True)
    move_line_id = fields.Many2one('account.move.line', ondelete="cascade", string="Línea banco")
            
            

class report_tesoreria_mundimold_line(models.Model):
    _name = 'report.tesoreria.mundimold.line'
    _order = 'date'
    
    report_id = fields.Many2one('report.tesoreria.mundimold', string="Tesorería", required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)
    name = fields.Char(string="Concepto", required=True)
    partner_id = fields.Many2one('res.partner', string="Empresa")
    journal_id = fields.Many2one('account.journal', string="Diario de pago")
    amount = fields.Float(string="Importe", required=True)
    account_analytic_id = fields.Many2one('account.analytic.account', string="Proyecto")
    account_id = fields.Many2one('account.account', string="Cuenta contable")
    date = fields.Date(string="Fecha", required=True)
    
    bank_line_id = fields.Many2one('account.bank.statement.line', ondelete="cascade", string="Línea banco")
    move_line_id = fields.Many2one('account.move.line', ondelete="cascade", string="Línea banco")
    
    TIPOS = [('06_PREV_PAGO','Previsión de pago'),   
             ('01_PREV_COBRO','Previsión de cobro'),
             ('03_FRA_PAGO_NACIONAL','Pago factura nacional'),
             ('04_FRA_PAGO_INTERNACIONAL','Pago factura intern.'),
             ('00_FRA_COBRO','Cobro de factura'),
             ('02_PAG_COBRO','Pagarés clientes'),
             ('05_PAG_PAGO','Pagarés proveedores'),
             ('12_SALDOS','Saldos iniciales'),
             ('11_FINANCIACION','Financiación'),
             ('10_IMPUESTOS','Impuestos'),
             ('07_PAGOS_FIJOS','Pagos fijos'),
             ('08_PERSONAL','Personal'),
             ('09_PRESTAMOS','Préstamos'),
             ('10_LEASING','Leasing'),
             ]
    type = fields.Selection(selection=TIPOS, string='Tipo')
    
    
    MAINT = [('00_COBROS','Cobros de clientes'),   
             ('01_PAGOS','Pagos de proveedores'),
             ('02_SALDOS','Saldos'),
             ]
    main_type = fields.Selection(selection=MAINT, string='Tipo principal')
    
    
    

    


class WizardTesoreriaAsignarBanco(models.TransientModel):
    _name = 'wizard.tesoreria.asignar.banco'
    

    def _default_line(self):
        return self.env['report.tesoreria.mundimold.line'].browse(self._context.get('active_id'))


    line_id = fields.Many2one('report.tesoreria.mundimold.line', string="Línea", default=_default_line, readonly=True)
    journal_id = fields.Many2one('account.journal', string="Diario de banco", required=True)
    
    
    
    @api.multi
    def assign_journal(self): 
        for record in self:
        
            if record.line_id.bank_line_id:
                record.line_id.bank_line_id.journal_payment_id = record.journal_id.id
                
            if record.line_id.move_line_id:
                record.line_id.move_line_id.journal_payment_id = record.journal_id.id
                
            record.line_id.journal_id = record.journal_id.id




class WizardTesoreriaAsignarFecha(models.TransientModel):
    _name = 'wizard.tesoreria.asignar.fecha'
    

    def _default_line(self):
        return self.env['report.tesoreria.mundimold.line'].browse(self._context.get('active_id'))


    line_id = fields.Many2one('report.tesoreria.mundimold.line', string="Línea", default=_default_line, readonly=True)
    date = fields.Date(string="Nueva fecha", required=False)
    ocultar = fields.Boolean(string="¿Ocultar línea?")
    
    
    
    @api.multi
    def assign_date(self): 
        for record in self:
        
            if record.date:
        
                if record.line_id.bank_line_id:
                    record.line_id.bank_line_id.date = record.date
                    
                if record.line_id.move_line_id:
                    record.line_id.move_line_id.date_maturity = record.date
                    
                record.line_id.date = record.date
                
            if record.ocultar == True:
                if record.line_id.move_line_id:
                    #if record.line_id.type == '02_PAG_COBRO' or record.line_id.type == '05_PAG_PAGO':
                    record.line_id.move_line_id.exclude_mis = True
                    self.env['report.tesoreria.mundimold.line'].search([('id', '=', record.line_id.id)]).unlink()
            
            
class WizardTesoreriaEliminarPrevision(models.TransientModel):
    _name = 'wizard.tesoreria.eliminar.prevision'
    

    def _default_line(self):
        return self.env['report.tesoreria.mundimold.line'].browse(self._context.get('active_id'))

    line_id = fields.Many2one('report.tesoreria.mundimold.line', string="Línea", default=_default_line, readonly=True)
    
    @api.multi
    def eliminar_prevision(self): 
        for record in self:
        
            if record.line_id.bank_line_id:
                
                
                idlin = record.line_id.id
                idbanklin = record.line_id.bank_line_id.id
                self.env['wizard.tesoreria.eliminar.prevision'].search([]).unlink()
                self.env['account.bank.statement.line'].search([('id', '=', idbanklin)]).unlink()
                self.env['report.tesoreria.mundimold.line'].search([('id', '=', idlin)]).unlink()
            
            