
from odoo import fields, models, api




class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    oc_cliente = fields.Char(string="OC cliente")
    notas_internas = fields.Char(string="Notas internas")
    
    #packing list
    num_bultos = fields.Integer(string="Num bultos")
    peso_bruto = fields.Char(string="Peso bruto")
    comentario_contenido = fields.Text(string="Comentario contenido")
    partida_arancelaria = fields.Char(string="Partida arancelaria")
    medidas_caja = fields.Text(string="Medidas caja")