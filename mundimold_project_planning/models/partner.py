from odoo import fields,models,api



class ResPartner(models.Model):
    _inherit='res.partner'

    resource_subco_id = fields.Many2one('resource.resource', string="Recurso")