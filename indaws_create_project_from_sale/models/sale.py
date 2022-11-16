
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError





class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_name = fields.Char(string="Nombre proyecto")
    sale_project_id = fields.Many2one('project.project', string='Proyecto')
    
    
    @api.onchange('summary_sale')
    def _onchange_summary_sale(self):
        for record in self:
            if not record.project_name or record.project_name == "":
                record.project_name = record.summary_sale
        
    
    @api.onchange('analytic_account_id')
    def _onchange_analytic_account_id(self):
        for record in self:
            project_id = None
            if record.analytic_account_id:
                for project in self.env['project.project'].search([('analytic_account_id', '=', record.analytic_account_id.id)]):
                    record.sale_project_id = project.id
                
                
    

                
    @api.multi
    def action_project_create(self):
        for record in self:
        
            if not record.project_name or record.project_name == '':
                raise ValidationError("Error: Hay que indicar un nombre par el proyecto")
        
        
            if not record.sale_project_id:
            

                project_id = self.env['project.project'].create({
                    'name': record.project_name,
                    'partner_id': record.partner_id.id
                    })
                record.sale_project_id = project_id.id
                record.analytic_account_id = project_id.analytic_account_id.id
   


        
                    
                    
                    