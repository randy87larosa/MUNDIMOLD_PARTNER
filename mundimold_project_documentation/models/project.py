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

        
class project_task(models.Model):
    _name = 'project.task'
    _inherit = 'project.task'

    document_line_id = fields.Many2one('project.document.line', string="Documento",)
        
        
class project_project(models.Model):
    _name = 'project.project'
    _inherit = 'project.project'

   
    document_lines_ids = fields.One2many('project.document.line', 'project_id', string="Fases de documentación", readonly=False)
    
    @api.multi
    def crear_fases_documentacion(self):
        for record in self:
        
            FASES = [('01','Info inicial del proyecto'),   
             ('02','Gantt proyecto'),
             ('03','Info inicial pieza'),
             ('04','Info de diseño de pieza'),
             ('05','Info cálculos moldflow'),
             ('06','Info cálculos estructurales'),
             ('07','Info diseño cliente'),
             ('08','Informe'),
             ('09','Ok del cliente'),
             ('10','Info de molde'),
             ('11','Revisión de molde'),
             ('12','Subconjuntos y componentes'),
             ('13','Info cámara caliente'),
             ('14','Info para prueba'),
             ('15','Documentación de molde'),
             ('16','Escandallo'),
             ('18','Info prueba de molde'),
             ('19','Procedimiento control de pieza'),
             ('20','Procedimiento control de molde'),
             ]
             
            for fase in FASES:
                if len(self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', fase)])) <= 0:
                    line_id = self.env['project.document.line'].create({'project_id': record.id, 
                                                                       'name': fase[0],
                                                                       'state': 'PEN',
                                                                     })
                                                                     
    STATES = [('PEN','Pendiente'),   
             ('EJE','En ejecución'),
             ('VAL','Pdte validar'),
             ('FIN','Finalizado'),
             ]
             
             
    ########################
    ####### ESTADOS   ######
    ########################
    
    state_01 = fields.Selection(selection=STATES, string='Estado 01', compute="_get_state_documentation")
    state_02 = fields.Selection(selection=STATES, string='Estado 02', compute="_get_state_documentation")
    state_03 = fields.Selection(selection=STATES, string='Estado 03', compute="_get_state_documentation")
    state_04 = fields.Selection(selection=STATES, string='Estado 04', compute="_get_state_documentation")
    state_05 = fields.Selection(selection=STATES, string='Estado 05', compute="_get_state_documentation")
    state_06 = fields.Selection(selection=STATES, string='Estado 06', compute="_get_state_documentation")
    state_07 = fields.Selection(selection=STATES, string='Estado 07', compute="_get_state_documentation")
    state_08 = fields.Selection(selection=STATES, string='Estado 08', compute="_get_state_documentation")
    state_09 = fields.Selection(selection=STATES, string='Estado 09', compute="_get_state_documentation")
    state_10 = fields.Selection(selection=STATES, string='Estado 10', compute="_get_state_documentation")
    
    @api.depends('document_lines_ids', 'document_lines_ids.state')
    def _get_state_documentation(self):
    
        for record in self:
            record.state_01 = 'PEN'
            for fase in self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '01')]):
                record.state_01 = fase.state
                break
            for fase in self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '02')]):
                record.state_02 = fase.state
                break
            for fase in self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '03')]):
                record.state_03 = fase.state
                break
            for fase in self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '04')]):
                record.state_04 = fase.state
                break
            for fase in self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '05')]):
                record.state_05 = fase.state
                break
            for fase in self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '06')]):
                record.state_06 = fase.state
                break
            for fase in self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '07')]):
                record.state_07 = fase.state
                break
            for fase in self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '08')]):
                record.state_08 = fase.state
                break
            for fase in self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '09')]):
                record.state_09 = fase.state
                break
            for fase in self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '10')]):
                record.state_10 = fase.state
                break
    
    
    ########################
    ########   01   ########
    ########################
    
    @api.multi
    def action_01_recoger_datos_pedido(self):
        for record in self:
            for sale in self.env['sale.order'].search([('sale_project_id', '=', record.id)]):
            
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
                        self.env['parque.maquinaria.project'].create({'project_id': record.id, 
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
    def action_01_empezar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '01')])[0]
            fase_id.date_ini = datetime.now()
            fase_id.state = 'EJE'
            
            
    @api.multi
    def action_01_finalizar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '01')])[0]
            fase_id.state = 'VAL'
            
    @api.multi
    def action_01_validar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '01')])[0]
            fase_id.date_fin = datetime.now()
            fase_id.state = 'FIN'
            
    @api.multi
    def action_01_reabrir(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '01')])[0]
            fase_id.date_fin = None
            fase_id.state = 'VAL'
            
            
            
    ########################
    ########   02   ########
    ########################
        
    @api.multi
    def action_02_empezar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '02')])[0]
            fase_id.date_ini = datetime.now()
            fase_id.state = 'EJE'
            
            
    @api.multi
    def action_02_finalizar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '02')])[0]
            fase_id.state = 'VAL'
            
    @api.multi
    def action_02_validar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '02')])[0]
            fase_id.date_fin = datetime.now()
            fase_id.state = 'FIN'
            
    @api.multi
    def action_02_reabrir(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '02')])[0]
            fase_id.date_fin = None
            fase_id.state = 'VAL'
            
            
    ########################
    ########   03   ########
    ########################
        
    @api.multi
    def action_03_empezar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '03')])[0]
            fase_id.date_ini = datetime.now()
            fase_id.state = 'EJE'
            
            
    @api.multi
    def action_03_finalizar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '03')])[0]
            fase_id.state = 'VAL'
            
    @api.multi
    def action_03_validar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '03')])[0]
            fase_id.date_fin = datetime.now()
            fase_id.state = 'FIN'
            
    @api.multi
    def action_03_reabrir(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '03')])[0]
            fase_id.date_fin = None
            fase_id.state = 'VAL'
            
            
    ########################
    ########   04   ########
    ########################
        
    @api.multi
    def action_04_empezar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '04')])[0]
            fase_id.date_ini = datetime.now()
            fase_id.state = 'EJE'
            
            
    @api.multi
    def action_04_finalizar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '04')])[0]
            fase_id.state = 'VAL'
            
    @api.multi
    def action_04_validar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '04')])[0]
            fase_id.date_fin = datetime.now()
            fase_id.state = 'FIN'
            
    @api.multi
    def action_04_reabrir(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '04')])[0]
            fase_id.date_fin = None
            fase_id.state = 'VAL'
            
            
    ########################
    ########   05   ########
    ########################
        
    @api.multi
    def action_05_empezar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '05')])[0]
            fase_id.date_ini = datetime.now()
            fase_id.state = 'EJE'
            
            
    @api.multi
    def action_05_finalizar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '05')])[0]
            fase_id.state = 'VAL'
            
    @api.multi
    def action_05_validar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '05')])[0]
            fase_id.date_fin = datetime.now()
            fase_id.state = 'FIN'
            
    @api.multi
    def action_05_reabrir(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '05')])[0]
            fase_id.date_fin = None
            fase_id.state = 'VAL'
            
            
    ########################
    ########   06   ########
    ########################
        
    @api.multi
    def action_06_empezar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '06')])[0]
            fase_id.date_ini = datetime.now()
            fase_id.state = 'EJE'
            
            
    @api.multi
    def action_06_finalizar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '06')])[0]
            fase_id.state = 'VAL'
            
    @api.multi
    def action_06_validar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '06')])[0]
            fase_id.date_fin = datetime.now()
            fase_id.state = 'FIN'
            
    @api.multi
    def action_06_reabrir(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '06')])[0]
            fase_id.date_fin = None
            fase_id.state = 'VAL'
            
            
    ########################
    ########   07   ########
    ########################
        
    @api.multi
    def action_07_empezar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '07')])[0]
            fase_id.date_ini = datetime.now()
            fase_id.state = 'EJE'
            
            
    @api.multi
    def action_07_finalizar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '07')])[0]
            fase_id.state = 'VAL'
            
    @api.multi
    def action_07_validar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '07')])[0]
            fase_id.date_fin = datetime.now()
            fase_id.state = 'FIN'
            
    @api.multi
    def action_07_reabrir(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '07')])[0]
            fase_id.date_fin = None
            fase_id.state = 'VAL'
            
            
            
    ########################
    ########   08   ########
    ########################
        
    @api.multi
    def action_08_empezar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '08')])[0]
            fase_id.date_ini = datetime.now()
            fase_id.state = 'EJE'
            
            
    @api.multi
    def action_08_finalizar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '08')])[0]
            fase_id.state = 'VAL'
            
    @api.multi
    def action_08_validar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '08')])[0]
            fase_id.date_fin = datetime.now()
            fase_id.state = 'FIN'
            
    @api.multi
    def action_08_reabrir(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '08')])[0]
            fase_id.date_fin = None
            fase_id.state = 'VAL'
            
            
            
    ########################
    ########   10   ########
    ########################
        
    @api.multi
    def action_10_empezar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '10')])[0]
            fase_id.date_ini = datetime.now()
            fase_id.state = 'EJE'
            
            
    @api.multi
    def action_10_finalizar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '10')])[0]
            fase_id.state = 'VAL'
            
    @api.multi
    def action_10_validar(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '10')])[0]
            fase_id.date_fin = datetime.now()
            fase_id.state = 'FIN'
            
    @api.multi
    def action_10_reabrir(self):
        for record in self:
            fase_id = self.env['project.document.line'].search([('project_id', '=', record.id),('name', '=', '10')])[0]
            fase_id.date_fin = None
            fase_id.state = 'VAL'
            
            
            
    ###################################################
    ############## INFO INICIAL PROYECTO ##############
    ###################################################
    
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
    material1_pieza_ids = fields.Many2many('product.mundimold.material', string="Otro material (NO)", )
    material1_pieza_id = fields.Many2one('product.template', string="Material 1")
    otro_material_pieza_ids = fields.Many2many('product.mundimold.material', string="Otro material (NO)", )
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
        comodel_name='parque.maquinaria.project',
        inverse_name='project_id'
    )
    
    
    
    ################################################
    ############## INFO INICIAL PIEZA ##############
    ################################################
    
    #calculo moldflow
    moldflow_nombre_comercial = fields.Char(string="Nombre comercial", )
    moldflow_marca = fields.Char(string="Marca", )
    moldflow_mfi = fields.Char(string="Mfi", )
    moldflow_temp_masa_fundida = fields.Float(string="Temperatura masa fundida", digits = (8,2) )
    moldflow_temp_molde = fields.Float(string="Temperatura molde", digits = (8,2) )
    
    #calculo estructural
    estructural_altura = fields.Char(string="Altura de apilado (cadas; palets)", )
    estructural_tiempo = fields.Char(string="Tiempo soporta la carga", )
    estructural_temp_exterior = fields.Char(string="Temperatura exterior", )
    estructural_temp_uso = fields.Char(string="Temperatura de uso", )
    
    #analisis holgura
    holgura_maxima = fields.Char(string="Holgura máxima entre ellas", )
    holgura_link = fields.Char(string="Link excel de holguras", )
    
    #tabla
    disenador_asignado_id = fields.Many2one('res.users', string="Diseñador asignado",)
    
    #parque maquinaria
    diseno_pieza_ids = fields.One2many(
        comodel_name='diseno.pieza.project',
        inverse_name='project_id'
    )
    
    
    ###########################################
    ############## INFO DE MOLDE ##############
    ###########################################
    
    #molde general
    info_largo = fields.Integer(string="Largo (Horizontal entre barras) mm" )
    info_ancho = fields.Integer(string="Ancho (Contando Pies) mm" )
    info_grueso = fields.Integer(string="Grueso entre platos mm" )
    info_apertura = fields.Integer(string="Apertura necesaria mm" )
    info_aro_fijo = fields.Integer(string="Aro centrdo lado fijo mm" )
    info_aro_movil = fields.Integer(string="Aro centrdo lado móvil mm" )
    
    #Inyeccion
    info_zonas_calefaccion = fields.Char(string="Zonas de claefacción" )
    info_num_boquillas = fields.Char(string="Num boquillas" )
    info_potencia_maxima = fields.Char(string="Potencia máxima" )
    info_conector_resistencia = fields.Char(string="Tipo conector y base para resistencias" )
    info_conector_termopares = fields.Char(string="Tipo conector y base para termopares" )
    info_conector_secuencial = fields.Char(string="Tipo conector y base para secuencial" )
    info_finales_carrera = fields.Boolean(string="Finales de carrera" )
    info_peso_inyeccion = fields.Integer(string="Peso lado de inyección kg" )
    info_peso_expulsion = fields.Integer(string="Peso lado de expulsión kg" )
    info_peso_total = fields.Integer(string="Peso total kg" )
    info_asiento_tipo = fields.Char(string="Asiento boquilla Tipo" )
    info_asiento_angulo = fields.Char(string="Asiento Ángulo o Radio" )
    
    #expulsion
    info_barras_expulsion = fields.Char(string="Barras expulsión máquina" )
    info_carrera_expulsion = fields.Integer(string="Carrera expulsión necesaria" )
    info_expulsion_abrochada = fields.Boolean(string="Expulsión abrochada a máquina" )
    info_distancia_barras_a = fields.Float(string="A - Distancia entre centros barras exp mm" )
    info_distancia_barras_b = fields.Float(string="B - Distancia entre centros barras exp mm" )
    info_distancia_barras_c = fields.Float(string="C - Distancia entre centros barras exp mm" )
    info_distancia_barras_d = fields.Float(string="D - Distancia entre centros barras exp mm" )
    info_metrica_rosca = fields.Char(string="Métrica de rosca" )
    info_ras_enroscada = fields.Char(string="A ras o mm enroscda mm" )
    info_agujero_molde = fields.Integer(string="Agujero de molde mm" )
    
    #sistema hidraulico aceite
    info_fijo_tipo_tomas = fields.Char(string="Tipo de tomas (espita o rosca)" )
    info_fijo_num_accionamientos = fields.Char(string="Num accionamientos" )
    info_fijo_presion_requerida = fields.Float(string="Presión requerida" )
    info_fijo_tipo_contactor = fields.Char(string="Tipo de contactor" )
    info_movil_tipo_tomas = fields.Char(string="Tipo de tomas (espita o rosca)" )
    info_movil_num_accionamientos = fields.Char(string="Num accionamientos" )
    info_movil_presion_requerida = fields.Float(string="Presión requerida" )
    info_movil_tipo_contactor = fields.Char(string="Tipo de contactor" )
    
    #sistema hidraulico refrigeracion
    info_colectores_circuitos = fields.Char(string="Num circuitos por parte" )
    info_colectores_rosca = fields.Char(string="O rosca" )
    info_colectores_acople = fields.Char(string="Tipo de acople" )
    info_colectores_temperatura = fields.Char(string="Temperatura requerida" )
    info_mangueras_circuitos = fields.Char(string="Num circuitos por parte" )
    info_mangueras_acople = fields.Char(string="Tipo de espita" )
    info_mangueras_temperatura = fields.Char(string="Temperatura requerida" )
    
    


class project_document_line(models.Model):
    _name = 'project.document.line'

    project_id = fields.Many2one('project.project', string="Proyecto", required=True)
    
    FASES = [('01','Info inicial del proyecto'),   
             ('02','Gantt proyecto'),
             ('03','Info inicial pieza'),
             ('04','Info de diseño de pieza'),
             ('05','Info cálculos moldflow'),
             ('06','Info cálculos estructurales'),
             ('07','Info diseño cliente'),
             ('08','Informe'),
             ('09','Ok del cliente'),
             ('10','Info de molde'),
             ('11','Revisión de molde'),
             ('12','Subconjuntos y componentes'),
             ('13','Info cámara caliente'),
             ('14','Info para prueba'),
             ('15','Documentación de molde'),
             ('16','Escandallo'),
             ('18','Info prueba de molde'),
             ('19','Procedimiento control de pieza'),
             ('20','Procedimiento control de molde'),
             ]
    name = fields.Selection(selection=FASES, string='Fase', readonly=True)
    
    
    STATES = [('PEN','Pendiente'),   
             ('EJE','En ejecución'),
             ('VAL','Pdte validar'),
             ('FIN','Finalizado'),
             ]
    state = fields.Selection(selection=STATES, string='Estado', readonly=True)
    date_ini = fields.Datetime(string="Fecha inicio", readonly=True)
    date_fin = fields.Datetime(string="Fecha completado", readonly=True)
    
    attachment_file = fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_document_attach_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Adjunto")
    
    
    
    
    @api.multi
    def action_view_form_documentation_form(self):
    
        view_name = 'mundimold_project_documentation.view_project_project_doc_' + self.name + '_form'
        
    
        view = self.env.ref(view_name)
        project_id = self.project_id.id
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'project.project',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'res_id': project_id,
            'context': self.env.context,
        }
        
        
        
class ParqueMaquinariaProject(models.Model):
    _name='parque.maquinaria.project'

    project_id = fields.Many2one(
        comodel_name='project.project',
        string="Proyecto"
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
                                
                                
                                
class DisenoPiezaProject(models.Model):
    _name='diseno.pieza.project'

    project_id = fields.Many2one(
        comodel_name='project.project',
        string="Proyecto"
    )

    enviado = fields.Date(string="Enviado")
    is_ok = fields.Boolean(string="Ok")
    name = fields.Char(string="Versión", required=True)
    links = fields.Char(string="Links")
    observaciones = fields.Char(string="Observaciones")
    llenado_ok = fields.Boolean(string="Llenado ok?")
    deformacion_ok = fields.Boolean(string="Deformación ok?")
    archivo_stl = fields.Char(string="Archivo STL")
    material = fields.Char(string="Material")
    nombre = fields.Char(string="Nom comercial")
    marca = fields.Char(string="Marca")
    mfi = fields.Char(string="MFI")
    fecha_cierre_lim = fields.Date(string="F cierre limitada")
    temp_masa_fundida = fields.Float(string="Temp masa fundida")
    temp_molde = fields.Float(string="Temp molde")
    ref_disenada = fields.Char(string="Ref diseñada")
    puntos_inyeccion = fields.Float(string="Puntos inyección")
    presion_maxima_inyeccion = fields.Float(string="Presión max inyección")
    ciclo_limitado = fields.Float(string="Ciclo limitado")
    tiempo_real_llenado = fields.Float(string="Tiempo real llenado")
    presion_llenado = fields.Float(string="Presión llenado")
    f_cierre_max = fields.Date(string="F cierre max")
    defelexion_nominal = fields.Float(string="Deflexión nominal")


    attachment_file = fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_parque_maquinaria_attach_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Adjunto")
