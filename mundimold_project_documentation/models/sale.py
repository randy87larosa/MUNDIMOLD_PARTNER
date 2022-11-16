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

        
class sale_order(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    
    #pieza
    category_moldrent_id = fields.Many2one('product.moldrent.category', string="Categoría Moldrent",)
    subcategory_moldrent_id = fields.Many2one('product.moldrent.category', string="Subcategoría Moldrent",)
    denominacion_pieza = fields.Char(string="Denominación Pieza", )
    uso_especifico = fields.Char(string="Uso especifico", )
    dimensiones_nominales = fields.Char(string="Dimensiones nominales", )
    dimensiones_x = fields.Float(string="Dimensiones X", )
    dimensiones_y = fields.Float(string="Dimensiones Y", )
    dimensiones_z = fields.Float(string="Dimensiones Z", )
    altura_apilamiento = fields.Float(string="Altura de apilamiento", )
    peso_nominal = fields.Float(string="Peso nominal", )
    material1_pieza_ids = fields.Many2many('product.mundimold.material', string="Material 1 (NO)", )
    material1_pieza = fields.Selection([('PP', 'PP'),('HDPE', 'HDPE')], string="Material 1 (NO)", )
    material1_pieza_id = fields.Many2one('product.template', string="Material 1")
    otro_material_pieza_ids = fields.Many2many('product.mundimold.material', string="Otro material (NO)", )
    otro_material_pieza = fields.Selection([('PP', 'PP'),('HDPE', 'HDPE')], string="Otro material (NO)", )
    otro_material_pieza_id = fields.Many2one('product.template', string="Otro material")
    peso_otro_material = fields.Float(string="Peso otro material", )
    material_reciclado = fields.Boolean(string="Se puede usar material reciclado", )
    compatibles_otras = fields.Boolean(string="Compatibles con otras del mercado", )
    carga_estatica = fields.Float(string="Carga estática", )
    carga_dinamica = fields.Float(string="Carga dinámica", )
    detalles_funcionales = fields.Char(string="Detalles funcionales", )
    limitaciones_funcionales = fields.Char(string="Limitaciones funcionales", )
    volumen_interno_contenido = fields.Float(string="Volume interno / Contenido:", )
    producto_contener = fields.Char(string="Producto a contener", )
    otro_pieza = fields.Text(string="Otro", )
    analisis_moldflow = fields.Boolean(string="Análisis moldflow", )
    analisis_estructural = fields.Boolean(string="Análisis estructural", )
    
    #molde general
    contraccion_material = fields.Char(string="Contracción del material", )
    tipo_molde_id = fields.Many2one('product.mundimold.molde.tipo', string="Tipo de molde",)
    clase_molde_id = fields.Many2one('product.mundimold.molde.clase', string="Clase de molde",)
    tecnologia_aplicada_id = fields.Many2one('product.mundimold.molde.tecnologia', string="Tecnología aplicada",)
    num_cavidades = fields.Float(string="Num cavidades",)
    plazo_molde = fields.Date(string="Plazo entrega molde (T1)",)
    ciclo_produccion = fields.Float('Ciclo de producción', digits = (8,2))
    colectores = fields.Float('Colectores', digits = (8,2))
    tonelaje_recomendado_maquina = fields.Float(string="Tonelaje recomendado máquina", digits = (8,2))
    
    #materiales
    fija_material_piezas_figura_ids = fields.Many2many('product.mundimold.material', string="Fija Material piezas de figura", )
    fija_material_base_fija_ids = fields.Many2many('product.mundimold.material', string="Fija Material base fija del molde", )
    fija_material_piezas_moviles_ids = fields.Many2many('product.mundimold.material', string="Fija Material Piezas móviles", )
    fija_aleacines_ids = fields.Many2many('product.mundimold.aleacion', string="Fija Aleaciones especiales", )
    
    #tratamientos
    tratamientos_piezas_figura_ids = fields.Many2many('product.mundimold.tratamiento', string="Tratamiento piezas de figura", )
    tratamientos_piezas_especificas_ids = fields.Many2many('product.mundimold.tratamiento', string="Tratamiento piezas específicas", )
    tratamientos_piezas_moviles_ids = fields.Many2many('product.mundimold.tratamiento', string="Tratamiento piezas móviles", )
    
    #sistema de inyeccion
    numero_puntos_inyeccion = fields.Float('Nº de puntos de inyección')
    tipo_inyeccion_ids = fields.Many2many('res.partner.tipo.inyeccion', string="Tipo")
    valvula_gate_obt_ids = fields.Many2many('res.partner.valvula.obturacion', string="Valve gate. Obturación")
    pro_diff_inyec_ids = fields.Many2many('res.partner.prov.diff', string="Proveedor diferente")
    filtro_en_camara = fields.Boolean(string="Filtro en cámara")
    comments_sistema_inyeccion = fields.Text(string="Comentarios sistema inyección")
    
    #acabados
    acabados_macho_ids = fields.Many2many('product.mundimold.acabado', string="Acabados parte macho", )
    acabados_hembra_ids = fields.Many2many('product.mundimold.acabado', string="Acabados parte hembra", )
    
    #textura
    tipo_textura = fields.Char(string="Tipo de textura", )
    proveedor_textura = fields.Char(string="Proveedor de textura", )
    attachment_texturas = fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_textura_crm_attach_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Adjuntos texturas")
    
    #expulsion
    tipo_expulsion_ids = fields.Many2many('res.partner.tipo.expulsion', string="Tipo")
    expulsion_piezas_ids = fields.Many2many('res.partner.expulsion.pieza', string="Expulsión pieza")
    expulsion_acontecimientos_ids = fields.Many2many('res.partner.expulsion.acontecimientos', string="Accionamientos de expulsión")
    comments_expulsion = fields.Text(string="Comentarios")
    barras_expulsion_maquina = fields.Float('Barras expulsión máquina')
    
    #elementos especiales
    elementos_date_codes = fields.Float('Fechador', digits = (8,2))
    elementos_shift_codes = fields.Float('Código transporte', digits = (8,2))
    elementos_material = fields.Float('Material ID', digits = (8,2))
    elementos_floating_plates = fields.Float('Placas del cliente', digits = (8,2))
    elementos_transducers = fields.Float('Sensores', digits = (8,2))
    elementos_switches = fields.Float('Enchufes', digits = (8,2))
    elementos_engraving = fields.Float('Grabados', digits = (8,2))
    elementos_qmc_plates = fields.Float('QMC Placas', digits = (8,2))
    elementos_cycle_counter = fields.Float('Contador ciclos', digits = (8,2))
    elementos_mold_samples = fields.Float('Muestras molde', digits = (8,2))
    elementos_repuestos = fields.Boolean('Repuestos')
    elementos_otros = fields.Char('Otros elementos')
    
    #otros accionamientos
    accionamientos_correderas_mecanicas = fields.Char(string="Correderas mecánicas", )
    accionamientos_correderas_hidraulicas = fields.Char(string="Correderas hidráulicas", )
    accionamientos_cilindros_hidraulicas = fields.Char(string="Cilindros hidráulicos", )
    accionamientos_cilindros_aire = fields.Char(string="Cilindros aire", )
    accionamientos_muelles = fields.Char(string="Muelles", )
    accionamientos_cilindros_gas = fields.Char(string="Cilindros de gas", )
    accionamientos_telescopicos = fields.Char(string="Telescópicos", )
    accionamientos_otros = fields.Char(string="Otros", )
    
    #parque maquinaria
    parque_maquinaria_ids = fields.One2many(
        comodel_name='parque.maquinaria.sale',
        inverse_name='sale_id'
    )
    
    
    
    @api.multi
    def cargar_datos_oportunidad(self):
        for record in self:
            if record.opportunity_id:
            
                sale = record.opportunity_id
            
            
                record.category_moldrent_id = sale.category_moldrent_id
                record.subcategory_moldrent_id = sale.subcategory_moldrent_id
                record.denominacion_pieza = sale.denominacion_pieza
                record.uso_especifico = sale.uso_especifico
                record.dimensiones_nominales = sale.dimensiones_nominales
                record.dimensiones_x = sale.dimensiones_x
                record.dimensiones_y = sale.dimensiones_y
                record.dimensiones_z = sale.dimensiones_z
                record.altura_apilamiento = sale.altura_apilamiento
                record.peso_nominal = sale.peso_nominal
                record.material1_pieza_ids = sale.material1_pieza_ids
                record.material1_pieza_id = sale.material1_pieza_id
                record.otro_material_pieza_ids = sale.otro_material_pieza_ids
                record.otro_material_pieza_id = sale.otro_material_pieza_id
                record.peso_otro_material = sale.peso_otro_material
                record.material_reciclado = sale.material_reciclado
                record.compatibles_otras = sale.compatibles_otras
                record.compatibles_otras = sale.compatibles_otras
                record.carga_estatica = sale.carga_estatica
                record.carga_dinamica = sale.carga_dinamica
                record.detalles_funcionales = sale.detalles_funcionales
                record.limitaciones_funcionales = sale.limitaciones_funcionales
                record.volumen_interno_contenido = sale.volumen_interno_contenido
                record.producto_contener = sale.producto_contener
                record.otro_pieza = sale.otro_pieza
                record.analisis_moldflow = sale.analisis_moldflow
                record.analisis_estructural = sale.analisis_estructural
                
                
                #molde general
                record.contraccion_material = sale.contraccion_material
                record.tipo_molde_id = sale.tipo_molde_id
                record.clase_molde_id = sale.clase_molde_id
                record.tecnologia_aplicada_id = sale.tecnologia_aplicada_id
                record.num_cavidades = sale.num_cavidades
                record.plazo_molde = sale.plazo_molde
                record.ciclo_produccion = sale.ciclo_produccion
                record.colectores = sale.colectores
                record.tonelaje_recomendado_maquina = sale.tonelaje_recomendado_maquina
                
                
                #materiales
                record.fija_material_piezas_figura_ids = sale.fija_material_piezas_figura_ids
                record.fija_material_base_fija_ids = sale.fija_material_base_fija_ids
                record.fija_material_piezas_moviles_ids = sale.fija_material_piezas_moviles_ids
                record.fija_aleacines_ids = sale.fija_aleacines_ids
                
                record.tratamientos_piezas_figura_ids = sale.tratamientos_piezas_figura_ids
                record.tratamientos_piezas_especificas_ids = sale.tratamientos_piezas_especificas_ids
                record.tratamientos_piezas_moviles_ids= sale.tratamientos_piezas_moviles_ids
                
                #sistema de inyeccion
                record.numero_puntos_inyeccion = sale.numero_puntos_inyeccion
                record.tipo_inyeccion_ids = sale.tipo_inyeccion_ids
                record.valvula_gate_obt_ids = sale.valvula_gate_obt_ids
                record.pro_diff_inyec_ids = sale.pro_diff_inyec_ids
                record.filtro_en_camara = sale.filtro_en_camara
                record.comments_sistema_inyeccion = sale.comments_sistema_inyeccion
                
                
                record.acabados_macho_ids = sale.acabados_macho_ids
                record.acabados_hembra_ids = sale.acabados_hembra_ids
                
                record.tipo_textura = sale.tipo_textura
                record.proveedor_textura = sale.proveedor_textura
                record.attachment_texturas = sale.attachment_texturas
                
                #expulsion
                record.tipo_expulsion_ids = sale.tipo_expulsion_ids
                record.expulsion_piezas_ids = sale.expulsion_piezas_ids
                record.expulsion_acontecimientos_ids = sale.expulsion_acontecimientos_ids
                record.comments_expulsion = sale.comments_expulsion
                record.barras_expulsion_maquina = sale.barras_expulsion_maquina
    
    
                #elementos especiales
                record.elementos_date_codes = sale.elementos_date_codes
                record.elementos_shift_codes = sale.elementos_shift_codes
                record.elementos_material = sale.elementos_material
                record.elementos_floating_plates = sale.elementos_floating_plates
                record.elementos_transducers = sale.elementos_transducers
                record.elementos_switches = sale.elementos_switches
                record.elementos_engraving = sale.elementos_engraving
                record.elementos_qmc_plates = sale.elementos_qmc_plates
                record.elementos_cycle_counter = sale.elementos_cycle_counter
                record.elementos_mold_samples = sale.elementos_mold_samples
                record.elementos_repuestos = sale.elementos_repuestos
                record.elementos_otros = sale.elementos_otros

    
                #otros accionamientos
                record.accionamientos_correderas_mecanicas = sale.accionamientos_correderas_mecanicas
                record.accionamientos_correderas_hidraulicas = sale.accionamientos_correderas_hidraulicas
                record.accionamientos_cilindros_hidraulicas = sale.accionamientos_cilindros_hidraulicas
                record.accionamientos_cilindros_aire = sale.accionamientos_cilindros_aire
                record.accionamientos_muelles = sale.accionamientos_muelles
                record.accionamientos_cilindros_gas = sale.accionamientos_cilindros_gas
                record.accionamientos_telescopicos = sale.accionamientos_telescopicos
                record.accionamientos_otros = sale.accionamientos_otros
                
                
                if len(record.parque_maquinaria_ids) <= 0:
                    for parque in sale.parque_maquinaria_ids:
                        self.env['parque.maquinaria.sale'].create({'sale_id': record.id, 
                                                                  'fabricante': parque.fabricante, 
                                                                  'modelo': parque.modelo,
                                                                  'tonelaje': parque.tonelaje,
                                                                  'plato_anc': parque.plato_anc,
                                                                  'paso_columnas': parque.paso_columnas,
                                                                  'columnas': parque.columnas,
                                                                  'espesor_min_max': parque.espesor_min_max,
                                                                  'centrador_parte_fija': parque.centrador_parte_fija,
                                                                  'centrador_parte_movil': parque.centrador_parte_movil,
                                                                  'apoyo_maquina': parque.apoyo_maquina,
                                                                  'paso': parque.paso,
                                                                 })
    
    
    
    @api.multi
    def cargar_datos_cliente(self):
        for record in self:
        
            #inyeccion
            record.tipo_inyeccion_ids = record.partner_id.tipo_inyeccion_ids
            record.valvula_gate_obt_ids = record.partner_id.valvula_gate_obt_ids
            record.pro_diff_inyec_ids = record.partner_id.pro_diff_inyec_ids
            record.filtro_en_camara = record.partner_id.filtro_en_camara
            
            #expulsion
            record.tipo_expulsion_ids = record.partner_id.tipo_expulsion_ids
            record.expulsion_piezas_ids = record.partner_id.expulsion_piezas_ids
            record.expulsion_acontecimientos_ids = record.partner_id.expulsion_acontecimientos_ids
            
            
        
            if len(record.parque_maquinaria_ids) <= 0:
                for parque in record.partner_id.parque_maquinaria_ids:
                    self.env['parque.maquinaria.sale'].create({'sale_id': record.id, 
                                                              'fabricante': parque.fabricante, 
                                                              'modelo': parque.modelo,
                                                              'tonelaje': parque.tonelaje,
                                                              'plato_anc': parque.plato_anc,
                                                              'paso_columnas': parque.paso_columnas,
                                                              'columnas': parque.columnas,
                                                              'espesor_min_max': parque.espesor_min_max,
                                                              'centrador_parte_fija': parque.centrador_parte_fija,
                                                              'centrador_parte_movil': parque.centrador_parte_movil,
                                                              'apoyo_maquina': parque.apoyo_maquina,
                                                              'paso': parque.paso,
                                                             })
    
    
    


        
class ParqueMaquinariaSale(models.Model):
    _name='parque.maquinaria.sale'

    sale_id = fields.Many2one(
        comodel_name='sale.order',
        string="Pedido"
    )

    fabricante = fields.Char(string="FABRICANTE")
    modelo = fields.Char(string="MODELO")
    tonelaje = fields.Char(string="TONELAJE")
    plato_anc = fields.Char(string="PLATO (ANCHOXALTO)")
    paso_columnas = fields.Char(string="PASO COLUMNAS")
    columnas = fields.Char(string="Ø COLUMNAS")
    espesor_min_max = fields.Char(string="ESPESOR MIN-MAX")
    centrador_parte_fija = fields.Char(string="CENTRADOR PARTE FIJA")
    centrador_parte_movil = fields.Char(string="CENTRADOR PARTE MOVIL")
    apoyo_maquina = fields.Char(string="APOYO MÁQUINA")
    paso = fields.Char(string="Ø PASO")
    
    attachment_file = fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_parque_maquinaria_attach_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Adjunto")
                                
                                
