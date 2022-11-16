# -*- coding: utf-8 -*-
# © 2009 NetAndCo (<http://www.netandco.net>).
# © 2011 Akretion Benoît Guillot <benoit.guillot@akretion.com>
# © 2014 prisnet.ch Seraphine Lantible <s.lantible@gmail.com>
# © 2016 Serpent Consulting Services Pvt. Ltd.
# © 2018 Daniel Campos <danielcampos@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo.exceptions import UserError, ValidationError

        
class account_bank_statement(models.Model):
    _name = 'account.bank.statement'
    _inherit = 'account.bank.statement'

   
    @api.multi
    def update_forecast_lines(self):
        for record in self:
            
            if record.journal_id.treasury_planning == True:
                #Actualizamos invoice plan
                for line in self.env['project.invoice.plan'].search([('permite_crear_forecast', '=', True),('date_forecast_manual', '>=', datetime.now().strftime("%Y-%m-%d")), ('project_id.company_id','=',record.company_id.id)]):
                    line.create_forecast_bank_line()
                    
                    
                #Actualizamos invoice suppliers
                for line in self.env['project.invoice.supplier'].search([('permite_crear_forecast', '=', True),('date_forecast', '>=', datetime.now().strftime("%Y-%m-%d")), ('project_id.company_id','=',record.company_id.id)]):
                    line.create_forecast_bank_line()
                
                #Actualizamos escandallo
                for line in self.env['project.escandallo'].search([('forecast_id', '=', False),('fecha_pago_manual', '>=', datetime.now().strftime("%Y-%m-%d")),('project_id.company_id','=',record.company_id.id)]):
                    line.create_forecast_bank_line()
                
                #Actualizamos subcontratistas
                for line in self.env['project.escandallo.subcontratista'].search([('forecast_id', '=', False),('fecha_pago_manual', '>=', datetime.now().strftime("%Y-%m-%d")),('project_id.company_id','=',record.company_id.id)]):
                    line.create_forecast_bank_line()


    

class account_bank_statement(models.Model):
    _name = 'account.bank.statement.line'
    _inherit = 'account.bank.statement.line'
    
    account_analytic_id = fields.Many2one('account.analytic.account', string="Proyecto")

