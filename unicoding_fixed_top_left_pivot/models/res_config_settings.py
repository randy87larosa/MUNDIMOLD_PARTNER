# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    
    stickify_pivot_shadow = fields.Boolean(string='Shadow')
    stickify_pivot_stack = fields.Selection([('shift', 'Shift'), ('overlay', 'Overlay')], required=True, default='shift')



            
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        xml_o = self.env['ir.model.data'].sudo().xmlid_to_object
        res.update(
            stickify_pivot_shadow= xml_o('unicoding_fixed_top_left_pivot.sticky_th_shadow', True).active,
            stickify_pivot_stack = 'overlay' if xml_o('unicoding_fixed_top_left_pivot.sticky_th_overlay', True).active else 'shift',
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        xml_o = self.env['ir.model.data'].sudo().xmlid_to_object
        xml_o('unicoding_fixed_top_left_pivot.sticky_th_shadow', True).active = self.stickify_pivot_shadow
        xml_o('unicoding_fixed_top_left_pivot.sticky_th_overlay', True).active = self.stickify_pivot_stack == 'overlay'
        xml_o('unicoding_fixed_top_left_pivot.sticky_th_shift', True).active = self.stickify_pivot_stack == 'shift'

        
