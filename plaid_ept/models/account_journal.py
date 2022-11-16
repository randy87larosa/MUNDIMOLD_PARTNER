# -*- coding: utf-8 -*-
# Copyright (c) 2017 Emipro Technologies Pvt Ltd (www.emiprotechnologies.com). All rights reserved.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero, DEFAULT_SERVER_DATE_FORMAT
import datetime
import logging

_logger = logging.getLogger(__name__)

class AccountJournal(models.Model):
    _inherit = "account.journal"

    # Add Plaid Synchronization selection to base field.
    def __get_bank_statements_available_sources(self):
        return [('undefined', _('Undefined Yet')),("plaid_sync", "Plaid Synchronization"),("file_import", "Importar fichero"),("manual", "Manual")]

    plaid_account_id = fields.Many2one('plaid.bank.account', string='Plaid Bank Account', copy=False)
    next_synchronization_cron = fields.Datetime(string="Next synchronization", related='plaid_account_id.next_synchronization')
    last_sync_date = fields.Date(string='Last Sync Date', related='plaid_account_id.last_sync_date')

    @api.constrains('plaid_account_id')
    def _check_plaid_account_id(self):
        if self.plaid_account_id:
            journals = self.search([('plaid_account_id','=',self.plaid_account_id.id)])
            if len(journals) > 1:
                raise ValidationError(_("Error! You can't mapped same Plaid account in multiple Journals."))

    @api.multi
    def plaid_configure(self):
        """we need this method to call Account Plaid wizard from Journal."""
        form = self.env.ref('plaid_ept.view_account_plaid_wizard_form')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Plaid Configuration',
            'res_model': 'account.plaid.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': form and form.id,
            'target': 'new',
            'context': {}
        }

    @api.multi
    def manual_sync_from_dashboard(self):
        return self.plaid_account_id.manual_sync()


class AccountBankStatement(models.Model):
    _inherit = "account.bank.statement"

    @api.model
    def plaid_sync_bank_statement(self, transactions, journal):
        """
         build a bank statement from a list of transaction and post messages is also post in the online_account of the journal.
         :param transactions: A list of transactions that will be created in the new bank statement.
             The format is : [{
                 'id': online id,                  (unique ID for the transaction)
                 'date': transaction date,         (The date of the transaction)
                 'description': transaction description,  (The description)
                 'amount': transaction amount,     (The amount of the transaction. Negative for debit, positive for credit)
                 'end_amount': total amount on the account
                 'location': optional field used to find the partner (see _find_partner for more info)
             }, ...]
         :param journal: The journal (account.journal) of the new bank statement

         Return: The number of imported transaction for the journal
        """
        # Since the synchronization succeeded, set it as the bank_statements_source of the journal
        journal.bank_statements_source = 'plaid_sync'

        all_lines = self.env['account.bank.statement.line'].search([('journal_id', '=', journal.id),
                                                                    ('date', '>=',journal.plaid_account_id.last_sync_date)])

        total = 0
        lines = []
        last_date = journal.plaid_account_id.last_sync_date
        end_amount = 0
        for transaction in transactions:
            if all_lines.search_count([('plaid_transaction_id', '=', transaction['id'])]) > 0 or transaction['amount'] == 0.0:
                continue
            line = {
                'date': transaction['date'],
                'name': transaction['description'],
                'amount': transaction['amount'],
                'plaid_transaction_id': transaction['id'],
            }
            total += transaction['amount']
            end_amount = transaction['end_amount']
            # Partner from address
            if 'location' in transaction:
                line['partner_id'] = self._find_partner(transaction['location']) and self._find_partner(transaction['location']).id or ''
            # Get the last date
            if not last_date or transaction['date'] > last_date:
                last_date = transaction['date']
            lines.append((0, 0, line))

        # Search for previous transaction end amount
        previous_statement = self.search([('journal_id', '=', journal.id)], order="date desc, id desc", limit=1)
        # For first synchronization, an opening bank statement line is created to fill the missing bank statements
        all_statement = self.search_count([('journal_id', '=', journal.id)])
        digits_rounding_precision = journal.currency_id.rounding
        if all_statement == 0 and not float_is_zero(end_amount - total, precision_rounding=digits_rounding_precision):
            lines.append((0, 0, {
                'date': transactions and (transactions[0]['date']) or datetime.datetime.now(),
                'name': _("Opening statement: first synchronization"),
                'amount': end_amount - total,
            }))
            total = end_amount

        # If there is no new transaction, the bank statement is not created
        if lines:
            to_create = []
            # create a new bank statement or add lines to existing bank statement
            previous_amount_to_report = 0
            for line in lines:
                create = False
                if not previous_statement or previous_statement.state == 'confirm':
                    to_create = lines
                    break

                line_date = datetime.datetime.strptime(str(line[2]['date']), DEFAULT_SERVER_DATE_FORMAT)
                p_stmt = datetime.datetime.strptime(str(previous_statement.date), DEFAULT_SERVER_DATE_FORMAT)
                if line_date.isocalendar()[1] != p_stmt.isocalendar()[1]:
                    create = True

                if create:
                    to_create.append(line)
                else:
                    previous_amount_to_report += line[2]['amount']
                    line[2].update({'statement_id': previous_statement.id})
                    self.env['account.bank.statement.line'].create(line[2])

            if not float_is_zero(previous_amount_to_report, precision_rounding=journal.currency_id.rounding):
                previous_statement.write(
                    {'balance_end_real': previous_statement.balance_end_real + previous_amount_to_report})

            if to_create:
                sorted_by_date = sorted(to_create, key=lambda l: l[2].get('date'))
                name = '{} To {} ({})'.format(sorted_by_date[0][2].get('date', ''), sorted_by_date[len(sorted_by_date) - 1][2].get('date', ''),journal.name)
                balance_start = None
                if previous_statement:
                    balance_start = previous_statement.balance_end_real
                sum_lines = sum([l[2]['amount'] for l in to_create])
                self.create({'name': name or _('Plaid sync'),
                                # 'name': _('Plaid sync'),
                             'journal_id': journal.id,
                             'line_ids': to_create,
                             'balance_end_real': end_amount if balance_start is None else balance_start + sum_lines,
                             'balance_start': (end_amount - total) if balance_start is None else balance_start
                             })
            _logger.info('to_create value of plaid_sync_bank_statement method: {}'.format(to_create))

        if self._context.get('pending',False) and self._context.get('pending_date',''):
            last_date = datetime.datetime.strptime(self._context.get('pending_date'),"%Y-%m-%d") - datetime.timedelta(days=1)
            journal.plaid_account_id.last_sync_date = last_date.date()
        else:
            journal.plaid_account_id.last_sync_date = last_date

        return {
            'effect': {
                'fadeout': 'slow',
                'message': "Yeah! Manual Sync Successfully.",
                'img_url': '/web/static/src/img/smile.svg',
                'type': 'rainbow_man',
            }
        }

    @api.model
    def _find_partner(self, location):
        """
        :param location: a dictionary of type:
                   {'state': x, 'address': y, 'city': z, 'zip': w}
                   state and zip are optional
        :return: Return a recordset of partner if the address of the transaction exactly match the address of a partner
        """
        partners = self.env['res.partner']
        domain = []
        if 'address' in location and 'city' in location:
            domain.append(('street', '=', location['address']))
            domain.append(('city', '=', location['city']))
            if 'state' in location:
                domain.append(('state_id.name', '=', location['state']))
            if 'zip' in location:
                domain.append(('zip', '=', location['zip']))
            return partners.search(domain, limit=1)
        return None
        return partners

class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    plaid_transaction_id = fields.Char("Plaid Transaction Id")
