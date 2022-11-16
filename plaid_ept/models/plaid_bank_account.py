# -*- coding: utf-8 -*-
# Copyright (c) 2017 Emipro Technologies Pvt Ltd (www.emiprotechnologies.com). All rights reserved.

from odoo import api, fields, models, _
from .. import plaid
import datetime
from odoo.exceptions import ValidationError, UserError
import math
import logging
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

_logger = logging.getLogger(__name__)
MAX_TRANSACTIONS_PER_PAGE = 500


class PlaidBankAccount(models.Model):
    _name = 'plaid.bank.account'
    _description = 'Plaid for online synchronization'
    _inherit = ['mail.thread']

    name = fields.Char(string='Bank Name', help='Name of the Bank')
    official_name = fields.Char(string='Official Name')
    number = fields.Char(string='Account Number', help='Account Number of this Bank')
    account_id = fields.Char(string='Provider Account', help='ID used to identify provider account in plaid',
                             readonly=True)
    institute_name = fields.Char(string="Institute Name", readonly=True)
    institute_id = fields.Char(string='Provider Institute ID',
                               help='ID of the banking institution in plaid server used for debugging purpose',
                               readonly=True)
    balance = fields.Char(string='Balance')
    last_sync_date = fields.Date(string='Last Sync Date', help='Last Import/sync Date of Plaid Bank Account Statements')
    next_synchronization = fields.Datetime("Next synchronization", compute='_compute_next_synchronization',
                                           help='next execution time of Manual Sync Cron')
    access_token = fields.Char(string='Access Token',
                               help='A rotatable token unique to a single Item used to access data for that Item')
    company_id = fields.Many2one('res.company', required=True, readonly=True,
                                 default=lambda self: self.env.user.company_id)

    update_credentials_required = fields.Boolean('Update Credentials Required', default=False)

    ##get next execution time from Plaid Sync cron
    @api.one
    def _compute_next_synchronization(self):
        self.next_synchronization = self.env['ir.cron'].sudo().search(
            [('id', '=', self.env.ref('plaid_ept.plaid_sync_cron').id)], limit=1).nextcall

    def _get_plaid_client_obj(self):
        try:
            ICP_obj = self.env['ir.config_parameter'].sudo()
            PLAID_CLIENT_ID = ICP_obj.get_param('plaid_client_id') or ''
            PLAID_SECRET = ICP_obj.get_param('plaid_secret') or ''
            PLAID_PUBLIC_KEY = ICP_obj.get_param('plaid_public_key') or ''
            PLAID_ENV = ICP_obj.get_param('plaid_env') or ''
            client = plaid.Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET,
                                  public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV)
            _logger.info(client)
            return client
        except plaid.errors.PlaidError as e:
            _logger.error('an error occured from _get_plaid_client_obj method : {}'.format(e.code, str(e)))
            raise ValidationError(_('{} , {}'.format(e.code, str(e))))

    @api.multi
    def create_or_update_plaid_account(self, values):
        try:
            client = self._get_plaid_client_obj()
            # Getting the information from the response
            # Note: we may multiple accounts if they have customized the plaid link. So, Just taking only one of them
            account_id = values.get('accounts[0][id]')
            institute_id = values.get('institution[institution_id]')

            # Searching for existing linked account.
            plaid_account_id = self.search([('account_id', '=', account_id), ('institute_id', '=', institute_id),
                                            ('company_id', '=', self.env.user.company_id.id)], limit=1)

            # if account is already existing then skip otherwise creating new one.
            if plaid_account_id:
                plaid_account_id.write({'update_credentials_required': False})
                return True
            else:
                public_token = values.get('public_token')
                institute_name = values.get('institution[name]')
                name = values.get('accounts[0][name]')
                exchange_token_response = client.Item.public_token.exchange(public_token)
                access_token = exchange_token_response['access_token']
                Response = client.Accounts.get(access_token, account_ids=[account_id])
                for account in Response.get('accounts', False):
                    _logger.info('Account Response: {}'.format(account))
                    end_amount = account['balances']['current']
                    name = account['name']
                    official_name = account['official_name']
                    if account.get('mask', ''):
                        number = '****' + account['mask']
                    else:
                        number = '****{}'.format(name)
                vals = {'name': name + ' (' + institute_name + ')' or 'Plaid Account',
                        'institute_name': institute_name,
                        'access_token': access_token,
                        'account_id': account_id,
                        'institute_id': institute_id,
                        'balance': end_amount,
                        'number': number,
                        'official_name': official_name,
                        }
                self.create(vals)
            _logger.info('values of create_or_update_plaid_account method is: {}'.format(values))
            return True
        except plaid.errors.PlaidError as e:
            _logger.error('an error occured from create_or_update_plaid_account method : {}'.format(e.code, str(e)))
            raise ValidationError(_('{} , {}'.format(e.code, str(e))))

    @api.multi
    def manual_sync(self):
        try:
            journal_id = self.env['account.journal'].search([('plaid_account_id', '=', self.id)])
            if self.update_credentials_required:
                return self.update_credentials()

            client = self._get_plaid_client_obj()
            access_token = self.access_token or ''

            if self.last_sync_date:
                start_date = self.last_sync_date
            else:
                start_date = "{:%Y-%m-%d}".format(datetime.datetime.now() + datetime.timedelta(-30))
            end_date = "{:%Y-%m-%d}".format(datetime.datetime.now())
            # existing_lines = self.env['account.bank.statement.line'].search([('journal_id', '=', journal_id.id),
            #                                                                  ('date', '>', start_date)], order='date')
            # if existing_lines:
            #     raise UserError(
            #         _("Warning, You can't able to Sync because after %s Bank Statements already Exist.") % (start_date))
            Response = client.Transactions.get(access_token, str(start_date), str(end_date), account_ids=[self.account_id])
            # Update the balance
            end_amount = self.balance
            for account in Response.get('accounts', False):
                end_amount = account['balances']['current']
            ##update Plaid Bank Account Balance
            self.balance = end_amount

            num_available_transactions = Response['total_transactions']
            num_pages = math.ceil(num_available_transactions / MAX_TRANSACTIONS_PER_PAGE)
            bank_transactions = []
            for page_num in range(num_pages):
                bank_transactions += \
                    client.Transactions.get(access_token, str(start_date), str(end_date), account_ids=[self.account_id],
                                            offset=page_num * MAX_TRANSACTIONS_PER_PAGE,
                                            count=MAX_TRANSACTIONS_PER_PAGE)['transactions']

            # Prepare the transaction
            transactions = []
            pending_trans_date = ''
            is_any_pending_trans = False
            for trans in bank_transactions:
                ## skip pending transactions.
                pending_trans = trans.get('pending',False)
                if pending_trans:
                    is_any_pending_trans = True
                    if not pending_trans_date:
                        pending_trans_date = trans['date']
                    elif pending_trans_date < trans['date']:
                        pending_trans_date = trans['date']
                    continue
                else:
                    transactions.append({
                        'id': trans['transaction_id'],
                        'date': datetime.datetime.strptime(trans['date'], DEFAULT_SERVER_DATE_FORMAT).date(),
                        'description': trans['name'],
                        'amount': -1 * trans['amount'],
                        'end_amount': end_amount,
                        # 'location': {'address': '69 rue de Namur', 'city': 'Wavre', 'state': 'Gujarat', 'zip': '1300'},
                        'location': trans['location'],
                    })
            _logger.info('Response of Manual Sync: {}'.format(Response))
            return self.env['account.bank.statement'].with_context({'pending':is_any_pending_trans,'pending_date':pending_trans_date}).plaid_sync_bank_statement(transactions, journal_id)
        except plaid.errors.PlaidError as e:
            _logger.error('an error from manual_sync: {}'.format(e.code, str(e)))
            if e.code == 'ITEM_LOGIN_REQUIRED':
                self.write({'update_credentials_required': True})
            else:
                raise ValidationError(_('{} , {}'.format(e.code, str(e))))

    @api.multi
    def update_credentials(self):
        return {'type': 'ir.actions.act_url',
                'name': "Update Credentials",
                'target': 'new',
                'url': '/plaid/reauthentication?plaid_acc=%s' % (self.id),
                }

    @api.model
    def cron_fetch_plaid_transactions(self):
        for account in self.search([]):
            _logger.info('Cron for Plaid Bank Account: {}'.format(account.name))
            journal_id = self.env['account.journal'].search([('plaid_account_id', '=', account.id)])
            if not journal_id:
                continue

            if account.update_credentials_required:
                account.message_post(
                    'Unable to sync, the provided credentials were not correct. Please try again or click on update credentials')
                continue

            if self.last_sync_date:
                start_date = self.last_sync_date
            else:
                start_date = "{:%Y-%m-%d}".format(datetime.datetime.now() + datetime.timedelta(-30))
            existing_lines = self.env['account.bank.statement.line'].search([('journal_id', '=', journal_id.id),
                                                                             ('date', '>=', start_date)], order='date')
            if existing_lines:
                continue
            account.manual_sync()
