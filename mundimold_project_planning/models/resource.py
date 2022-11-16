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

import logging
#Get the logger
_logger = logging.getLogger(__name__)
from datetime import datetime




        
class resource_resource(models.Model):
    _name = 'resource.resource'
    _inherit = 'resource.resource'
    
    is_departamento = fields.Boolean(string='¿Recurso departamento?')
    num_recursos = fields.Integer(string='Num recursos', default=1)
    nombre_departamento = fields.Char(string='Nombre departamento')
    
    


