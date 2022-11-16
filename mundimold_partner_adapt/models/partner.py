from odoo import fields,models,api

####TABLAS AUXILIARES###
#SISTEMA DE REFRIGERACIÓN

class ResPartnerTipoEnchufe(models.Model):
    _name='res.partner.tipo.enchufe'
    name = fields.Char(string="Nombre")

class ResPartnerColectore(models.Model):
    _name='res.partner.colectores'
    name = fields.Char(string="Nombre")

class ResPartnerEnchufeEntrada(models.Model):
    _name='res.partner.enchufe.entrada'
    name = fields.Char(string="Nombre")

class ResPartnerEnchufeSalida(models.Model):
    _name='res.partner.enchufe.salida'
    name = fields.Char(string="Nombre")

class ResPartnerConexion(models.Model):
    _name='res.partner.conexion'
    name = fields.Char(string="Nombre")

#SISTEMA HIDRÁULICO
class ResPartnerTipoProvCilinhid(models.Model):
    _name='res.partner.provcilinhid'
    name = fields.Char(string="Nombre")

class ResPartnerConexiónEntrada(models.Model):
    _name='res.partner.conexion.entrada'
    name = fields.Char(string="Nombre")

class ResPartnerConexiónSalida(models.Model):
    _name='res.partner.conexion.salida'
    name = fields.Char(string="Nombre")

#SISTEMA DE INYECCIÓN
class ResPartnerTipoInyeccion(models.Model):
    _name='res.partner.tipo.inyeccion'
    name = fields.Char(string="Nombre")

class ResPartnerValculaObturacion(models.Model):
    _name='res.partner.valvula.obturacion'
    name = fields.Char(string="Nombre")

class ResPartnerProvDif(models.Model):
    _name='res.partner.prov.diff'
    name = fields.Char(string="Nombre")

class ResPartnerAboVoMaq(models.Model):
    _name='res.partner.abovvomaq'
    name = fields.Char(string="Nombre")

#NEUMÁTICA
class ResPartnerConexionNeumatica(models.Model):
    _name='res.partner.conexion.neumatica'
    name = fields.Char(string="Nombre")

#EXPULSIÓN
class ResPartnerTipoExpulsion(models.Model):
    _name='res.partner.tipo.expulsion'
    name = fields.Char(string="Nombre")

class ResPartnerExpulsionPieza(models.Model):
    _name='res.partner.expulsion.pieza'
    name = fields.Char(string="Nombre")

class ResPartnerExpulsionAcontecimientos(models.Model):
    _name='res.partner.expulsion.acontecimientos'
    name = fields.Char(string="Nombre")

#ACCIONAMIENTOS
class ResPartnerTipoAccionamineto(models.Model):
    _name='res.partner.tipo.accionamiento'
    name = fields.Char(string="Nombre")

class ResPartnerDetecMov(models.Model):
    _name='res.partner.detec.mov'
    name = fields.Char(string="Nombre")

#MANIPULACIÓN DE MOLDE
class ResPartnerPuenteGrua(models.Model):
    _name='res.partner.puente.grua'
    name = fields.Char(string="Nombre")

class ResPartnerCarretillaElevadora(models.Model):
    _name='res.partner.carretilla.elevadora'
    name = fields.Char(string="Nombre")

class ResPartnerEntregaMolde(models.Model):
    _name='res.partner.entrega.molde'
    name = fields.Char(string="Nombre")

#DOCUMENTACIÓN

class ResPartnerCarpetaDoc(models.Model):
    _name='res.partner.carpeta.doc'
    name = fields.Char(string="Nombre")

#VARIOS
class ResPartnerMoldePintado(models.Model):
    _name='res.partner.molde.pintado'
    name = fields.Char(string="Nombre")

class ResPartnerFijMaquina(models.Model):
    _name='res.partner.fij.maqui'
    name = fields.Char(string="Nombre")


class ParqueMaquinaria(models.Model):
    _name='parque.maquinaria'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Cliente"
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

####TABLAS AUXILIARES###
class ResPartner(models.Model):
    _inherit='res.partner'

    #SISTEMA DE REFRIGERACIÓN
    temperatura = fields.Char(string="Temperatura")
    caudal = fields.Char(string="Caudal")
    presion = fields.Char(string="Presión")
    dos_temperaturas = fields.Boolean(string="¿Dos temperaturas?")
    modelo = fields.Char(string="Modelo")

    tipo_enchufe_ids = fields.Many2many(
        comodel_name='res.partner.tipo.enchufe',
        relation='partner_id_tipo_enchufe_id_rel',
        string="Tipo Enchufe"
    )

    colectores_ids = fields.Many2many(
        comodel_name='res.partner.colectores',
        relation='partner_id_colectores_id_rel',
        string="Colectores"
    )

    enchufe_entrada_ids = fields.Many2many(
        comodel_name='res.partner.enchufe.entrada',
        relation='partner_id_enchufe_ent_id_rel',
        string="Enchufes entrada"
    )

    enchufe_salida_ids = fields.Many2many(
        comodel_name='res.partner.enchufe.salida',
        relation='partner_id_enchufe_sal_id_rel',
        string="Enchufes salida"
    )

    valvulas_conector_salida = fields.Boolean(string="Valvulas en conector salidas")
    zona_dif_temp = fields.Integer(string="Zonas con diferentes temperatura")
    comments_1 = fields.Text(string="Comentarios")

    #SISTEMA HIDRÁULICO

    prov_cil_hid_ids = fields.Many2many(
        comodel_name='res.partner.provcilinhid',
        relation='partner_id_prov_cil_hid_id_rel',
        string="Proveedor cilindros hidráulico"
    )

    conexion_entrada_h_ids = fields.Many2many(
        comodel_name='res.partner.conexion.entrada',
        relation='partner_id_conexion_entrada_h_id_rel',
        string="Conexión entrada"
    )
    conexion_salida_h_ids = fields.Many2many(
        comodel_name='res.partner.conexion.salida',
        relation='partner_id_conexion_salida_h_id_rel',
        string="Conexión salida"
    )
    comments_2 = fields.Text(string="Comentarios")

    #SISTEMA DE INYECCIÓN
    tipo_inyeccion_ids = fields.Many2many(
        comodel_name='res.partner.tipo.inyeccion',
        relation='partner_id_tipo_inyeccion_id_rel',
        string="Tipo"
    )

    valvula_gate_obt_ids = fields.Many2many(
        comodel_name='res.partner.valvula.obturacion',
        relation='partner_id_valvul_gate_obt_id_rel',
        string="Valve gate. Obturación"
    )

    pro_diff_inyec_ids = fields.Many2many(
        comodel_name='res.partner.prov.diff',
        relation='partner_id_pro_diff_inyec_id_rel',
        string="Proveedor diferente"
    )

    filtro_en_camara = fields.Boolean(string="Filtro en cámara")

    apoyo_boqui_maq_ids = fields.Many2many(
        comodel_name='res.partner.abovvomaq',
        relation='partner_id_apoyo_boqui_maq_rel',
        string="Apoyo boquilla máquina"
    )


    comments_3 = fields.Text(string="Comentarios")

    #NEUMÁTICA
    conexion_neumatica_ids = fields.Many2many(
        comodel_name='res.partner.conexion.neumatica',
        relation='partner_id_conexion_neumatica_id_rel',
        string="Conexión"
    )

    comments_4 = fields.Text(string="Comentarios")


    #EXPULSIÓN
    tipo_expulsion_ids = fields.Many2many(
        comodel_name='res.partner.tipo.expulsion',
        relation='partner_id_tipo_expulsion_id_rel',
        string="Tipo"
    )

    expulsion_piezas_ids = fields.Many2many(
        comodel_name='res.partner.expulsion.pieza',
        relation='partner_id_expulsion_piezas_id_rel',
        string="Expulsión pieza"
    )

    expulsion_acontecimientos_ids = fields.Many2many(
        comodel_name='res.partner.expulsion.acontecimientos',
        relation='partner_id_expulsion_acontecimientos_sal_id_rel',
        string="Acontecimientos de expulsión"
    )

    comments_5 = fields.Text(string="Comentarios")
    #ACCIONAMIENTOS

    tipo_accionamineto_ids = fields.Many2many(
        comodel_name='res.partner.tipo.accionamiento',
        relation='partner_id_tipo_accionamineto_id_rel',
        string="Tipo"
    )

    detec_mov_ids = fields.Many2many(
        comodel_name='res.partner.detec.mov',
        relation='partner_id_detec_mov_id_rel',
        string="Detección movimientos"
    )

    comments_6 = fields.Text(string="Comentarios")

    #MANIPULACIÓN DE MOLDE

    puente_grua_ids = fields.Many2many(
        comodel_name='res.partner.puente.grua',
        relation='partner_id_puente_grua_id_rel',
        string="Puente grua"
    )

    carretilla_elevadora_ids = fields.Many2many(
        comodel_name='res.partner.carretilla.elevadora',
        relation='partner_id_carretilla_elevadora_id_rel',
        string="Carretilla elevadora"
    )

    entrega_molde_ids = fields.Many2many(
        comodel_name='res.partner.entrega.molde',
        relation='partner_id_entrega_molde_id_rel',
        string="Entrega de molde"
    )

    #DOCUMENTACIÓN
    entrega_3_molde = fields.Boolean(string="Entrega 3d molde")
    entrega_3_pieza = fields.Boolean(string="Entrega 3d pieza")

    carpeta_doc_ids = fields.Many2many(
        comodel_name='res.partner.carpeta.doc',
        relation='partner_id_carpeta_doc_id_rel',
        string="Carpeta documentación"
    )

    comments_7 = fields.Text(string="Comentarios")

    #VARIOS - REQUERIMIENTOS

    molde_pintado_ids = fields.Many2many(
        comodel_name='res.partner.molde.pintado',
        relation='partner_id_molde_pintado_id_rel',
        string="Molde pintado"
    )

    fijacion_maq_ids = fields.Many2many(
        comodel_name='res.partner.fij.maqui',
        relation='partner_id_fijacion_maq_id_rel',
        string="Fijación molde máquina"
    )
    
    attachment_file_req = fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_partner_requerimientos_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Adjunto")

    comments_8 = fields.Text(string="Comentarios")

    #PARQUE MAQUINARIA

    parque_maquinaria_ids = fields.One2many(
        comodel_name='parque.maquinaria',
        inverse_name='partner_id'
    )