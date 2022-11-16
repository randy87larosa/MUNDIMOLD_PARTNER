
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError



class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ##################
    #campos genericos#
    ##################
    
    
    #################
    #campos moldrent#
    #################
    date_moldrent = fields.Date(string="Fecha Moldrent", )
    caracteristicas_tecnicas = fields.Html(string="Características técnicas", )
    descripcion_corta = fields.Text(string="Descripción corta", )
    tipo_moldrent = fields.Selection([('P', 'Plástico'),('M', 'Molde'),], string="Tipo Moldrent", )
    formulario_moldrent = fields.Html(string="Formulario de producto", )
    
    ## NO
    lugar_envio = fields.Char(string="Lugar de envío", )
    precio_asociado = fields.Float(string="Precio asociado envío",)
    ##
    envio_ids = fields.One2many('product.moldrent.envios', 'product_id', string="Envios")
    
    
    
    category_moldrent_id = fields.Many2one('product.moldrent.category', string="Categoría Moldrent",)
    subcategory_moldrent_id = fields.Many2one('product.moldrent.category', string="Subcategoría Moldrent",)
    
    #molde
    meses_ids = fields.Many2many('product.moldrent.meses', string="Disponibilidad")
    precio_alquiler_dia = fields.Float('Precio alquiler día', digits = (8,2))
    tiempo_ciclo = fields.Float('Tiempo de ciclo', digits = (8,2))
    ubicacion_molde = fields.Char(string="Ubicación molde", )
    ubicacion_molde_id = fields.Many2one('res.country', string="Ubicación molde",)
    precio_nuevo = fields.Float('Precio nuevo', digits = (8,2))
    precio_usado = fields.Float('Precio usado', digits = (8,2))
    pieza_asociada_id = fields.Many2one('product.template', string="Producto asociado",)
    
    #piezas
    precio_desde = fields.Float('Precio desde', digits = (8,2))
    muestras_contenedor = fields.Char(string="Muestras por contenedor", )
    precio_contenedor = fields.Float('Precio por contenedor', digits = (8,2))
    molde_asociado_id = fields.Many2one('product.template', string="Molde asociado",)
    
    
    ##############
    #campos molde#
    ##############
    
    #todos
    estado_pieza_id = fields.Many2one('product.mundimold.estado.pieza', string="Estado actual pieza", )
    tonelaje_mquina_inyeccion = fields.Float(string="Tonelaje máquina inyección",)
    num_cavidades = fields.Float(string="Num cavidades",)
    num_puntos_inyeccion = fields.Float(string="Num puntos inyección",)
    anos_fabricacion = fields.Float(string="Años de fabricación",)
    dimensiones_molde = fields.Char(string="Dimensiones",)
    peso_total = fields.Float(string="Peso total",)
    peso_parte_fija = fields.Float(string="Peso parte fija",)
    peso_parte_movil = fields.Float(string="Peso parte móvil",)
    plazo_molde_nuevo = fields.Float(string="Plazo entrega molde nuevo",)
    tipo_molde_id = fields.Many2one('product.mundimold.molde.tipo', string="Tipo de molde",)
    clase_molde_id = fields.Many2one('product.mundimold.molde.clase', string="Clase de molde",)
    tecnologia_aplicada_id = fields.Many2one('product.mundimold.molde.tecnologia', string="Tecnología aplicada",)
    construccion_molde_id = fields.Many2one('product.mundimold.molde.construccion', string="Construcción de molde",)
    tipo_extraccion_pieza_id = fields.Many2one('product.mundimold.molde.extraccion', string="Tipo extracción de pieza",)
    
    
    
    ##############
    #campos pieza#
    ##############
    
    #todos
    denominacion_pieza = fields.Char(string="Denominación Pieza", )
    uso_especifico = fields.Char(string="Uso especifico", )
    dimensiones_nominales = fields.Char(string="Dimensiones nominales", )
    altura_apilamiento = fields.Float(string="Altura de apilamiento", )
    peso_nominal = fields.Float(string="Peso nominal", )
    material1_pieza_ids = fields.Many2many('product.mundimold.material', string="Material 1", )
    otro_material_pieza_ids = fields.Many2many('product.mundimold.material', string="Otro material", )
    peso_otro_material = fields.Float(string="Peso otro material", )
    material_reciclado = fields.Boolean(string="Se puede usar material reciclado", )
    carga_estatica = fields.Float(string="Carga estática", )
    carga_dinamica = fields.Float(string="Carga dinámica", )
    detalles_funcionales = fields.Char(string="Detalles funcionales", )
    limitaciones_funcionales = fields.Char(string="Limitaciones funcionales", )
    volumen_interno_contenido = fields.Float(string="Volume interno / Contenido:", )
    producto_contener = fields.Char(string="Producto a contener", )
    otro_pieza = fields.Text(string="Otro", )
    analisis_moldflow = fields.Boolean(string="Análisis moldflow", )
    analisis_estructural = fields.Boolean(string="Análisis estructural", )
    
    
    
    
    
    ##############################
    #campos material y aleaciones#
    ##############################
    
    fija_material_piezas_figura_ids = fields.Many2many('product.mundimold.material', string="Fija Material piezas de figura", )
    fija_material_base_fija_ids = fields.Many2many('product.mundimold.material', string="Fija Material base fija del molde", )
    fija_material_piezas_moviles_ids = fields.Many2many('product.mundimold.material', string="Fija Material Piezas móviles", )
    fija_aleacines_ids = fields.Many2many('product.mundimold.aleacion', string="Fija Aleaciones especiales", )
    
    movil_material_piezas_figura_ids = fields.Many2many('product.mundimold.material', string="Móvil Material piezas de figura", )
    movil_material_base_fija_ids = fields.Many2many('product.mundimold.material', string="Móvil Material base fija del molde", )
    movil_material_piezas_moviles_ids = fields.Many2many('product.mundimold.material', string="Móvil Material Piezas móviles", )
    movil_aleacines_ids = fields.Many2many('product.mundimold.aleacion', string="Móvil Aleaciones especiales", )
    
    mas_material_piezas_figura_ids = fields.Many2many('product.mundimold.material', string="Más Material piezas de figura", )
    mas_material_base_fija_ids = fields.Many2many('product.mundimold.material', string="Más Material base fija del molde", )
    mas_material_piezas_moviles_ids = fields.Many2many('product.mundimold.material', string="Más Material Piezas móviles", )
    mas_aleacines_ids = fields.Many2many('product.mundimold.aleacion', string="Más Aleaciones especiales", )
    
    tratamientos_piezas_figura_ids = fields.Many2many('product.mundimold.tratamiento', string="Tratamiento piezas de figura", )
    tratamientos_piezas_especificas_ids = fields.Many2many('product.mundimold.tratamiento', string="Tratamiento piezas específicas", )
    tratamientos_piezas_moviles_ids = fields.Many2many('product.mundimold.tratamiento', string="Tratamiento piezas móviles", )
    
    tipo_textura = fields.Char(string="Tipo de textura", )
    proveedor_textura = fields.Char(string="Proveedor de textura", )
    
    acabados_macho_ids = fields.Many2many('product.mundimold.acabado', string="Acabados parte macho", )
    acabados_hembra_ids = fields.Many2many('product.mundimold.acabado', string="Acabados parte hembra", )
    
    elementos_date_codes = fields.Float('Date Codes', digits = (8,2))
    elementos_shift_codes = fields.Float('Shift Codes', digits = (8,2))
    elementos_material = fields.Float('Material ID', digits = (8,2))
    elementos_floating_plates = fields.Float('Floating Plates', digits = (8,2))
    elementos_transducers = fields.Float('Transducers', digits = (8,2))
    elementos_pl_locks = fields.Float('PL Locks', digits = (8,2))
    elementos_switches = fields.Float('Switches', digits = (8,2))
    elementos_engraving = fields.Float('Engraving', digits = (8,2))
    elementos_qmc_plates = fields.Float('QMC Plates', digits = (8,2))
    elementos_cycle_counter = fields.Float('Cycle Counter', digits = (8,2))
    elementos_mold_samples = fields.Float('Mold Samples', digits = (8,2))
    elementos_gate_inserts = fields.Float('Gate Inserts', digits = (8,2))
    elementos_cavity_shut_off= fields.Float('Cavity Shut-Off', digits = (8,2))
    elementos_split_rib_inserts = fields.Float('Split Rib Inserts', digits = (8,2))
    
    
    #csv moldrent
    csv_moldrent = fields.Text(string="CSV MOLDRENT", compute='_get_csv_moldrent' )
    
    @api.depends('name')
    def _get_csv_moldrent(self):
        for record in self:
            csv_moldrent = ''
            
            sku = record.default_code
            title = record.name
            content = ''
            if record.caracteristicas_tecnicas:
                content = record.caracteristicas_tecnicas.replace('"', '""')
            excerpt = ''
            if record.descripcion_corta:
                excerpt = record.descripcion_corta.replace('"', '""')
            date5 = record.create_date
            post_type = record.create_date
            slug = record.name.replace(" ", "-")
            _wcpa_product_meta = 162
            if record.tipo_moldrent == 'M':
                _wcpa_product_meta = 188
            wcpa_pcf_muestras_por_container = record.muestras_contenedor
            wcpa_pcf_pvp_container = record.precio_contenedor
            lugar_envio_precio = ''
            if record.lugar_envio and record.precio_asociado:
                lugar_envio_precio = '"[{""field_5dfc844d04e78"":""' + record.lugar_envio + '"",""field_5dfc846804e79"":""' + str(record.precio_asociado) + '""},'
                lugar_envio_precio = lugar_envio_precio + '""},{""field_5dfc844d04e78"":""Otro"",""field_5dfc846804e79"":""0""}""]"'
            disp = []
            for elem in record.meses_ids:
                disp.append(elem.name)
            disponibilidad = ','.join([str(x) for x in disp])
            precio_alquiler = record.precio_alquiler_dia
            ubicacion_molde = record.ubicacion_molde
            tiempo_ciclo = record.tiempo_ciclo
            precio_molde_nuevo = record.precio_nuevo
            precio_molde_usado = record.precio_usado
            image_url = ''
            regular_price = 0.0
            if record.tipo_moldrent == 'P': 
                regular_price = record.precio_desde
            product_type = 'simple'
            product_visibility = 'visible'
            categorias = ''
            if record.category_moldrent_id and record.subcategory_moldrent_id:
                categorias = record.category_moldrent_id.name + '>' + record.subcategory_moldrent_id.name
            etiquetas = 'Molde'
            if record.tipo_moldrent == 'P': 
                etiquetas = 'Producto'
            visibility = ''
            cross_sells = ''
            tipo_simulador = 188
            if record.tipo_moldrent == 'P':
                tipo_simulador = 162
                
            csv_moldrent = str(sku) + ',"' + title + '","' + str(content) + '","' + str(excerpt) + '",' + str(date5) + ',' + str(post_type) + ',' + slug + ',' + str(_wcpa_product_meta) + ',' + str(wcpa_pcf_muestras_por_container) + ',' + str(wcpa_pcf_pvp_container) + ',' + lugar_envio_precio + ',"' + disponibilidad + '",' + str(precio_alquiler) + ',' + str(ubicacion_molde) + ',' + str(tiempo_ciclo) + ',' + str(precio_molde_nuevo) + ',' + str(precio_molde_usado) + ',' + image_url + ',' + str(regular_price) + ',' + product_type + ',' + product_visibility + ',' + categorias + ',' + etiquetas + ',' + visibility + ',' + cross_sells + ',' + str(tipo_simulador)
            record.csv_moldrent = csv_moldrent
    
    
class ProductMoldrentMeses(models.Model):
    _name = 'product.moldrent.meses'
    _order = 'sequence'

    name = fields.Char('Nombre')
    sequence = fields.Integer('Orden')
    
    
class ProductMoldrentEnvios(models.Model):
    _name = 'product.moldrent.envios'

    product_id = fields.Many2one('product.template', string="Producto",)
    envio_ids = fields.Many2one('res.country', string="País",)
    precio = fields.Float('Precio')
    
    
    
class ProductMoldrentCategory(models.Model):
    _name = 'product.moldrent.category'
    _order = 'name'

    name = fields.Char('Nombre')
    parent_id = fields.Many2one('product.moldrent.category', string="Categoría padre",)
    
    
class ProductMundimoldMaterial(models.Model):
    _name = 'product.mundimold.material'
    _order = 'name'

    name = fields.Char('Nombre')

    
class ProductMundimoldMoldeTipo(models.Model):
    _name = 'product.mundimold.molde.tipo'
    _order = 'name'

    name = fields.Char('Nombre')

class ProductMundimoldMoldeClase(models.Model):
    _name = 'product.mundimold.molde.clase'
    _order = 'name'

    name = fields.Char('Nombre')
    
class ProductMundimoldMoldeTecnologia(models.Model):
    _name = 'product.mundimold.molde.tecnologia'
    _order = 'name'

    name = fields.Char('Nombre')
    
class ProductMundimoldMoldeConstruccion(models.Model):
    _name = 'product.mundimold.molde.construccion'
    _order = 'name'

    name = fields.Char('Nombre')
    
class ProductMundimoldMoldeExtraccion(models.Model):
    _name = 'product.mundimold.molde.extraccion'
    _order = 'name'

    name = fields.Char('Nombre')
    
    
class ProductMundimoldEstadoPieza(models.Model):
    _name = 'product.mundimold.estado.pieza'
    _order = 'name'

    name = fields.Char('Nombre')
    
    
class ProductMundimoldAleacion(models.Model):
    _name = 'product.mundimold.aleacion'
    _order = 'name'

    name = fields.Char('Nombre')
    
class ProductMundimoldTratamiento(models.Model):
    _name = 'product.mundimold.tratamiento'
    _order = 'name'

    name = fields.Char('Nombre')
    
    
class ProductMundimoldAcabado(models.Model):
    _name = 'product.mundimold.acabado'
    _order = 'name'

    name = fields.Char('Nombre')
    
    
