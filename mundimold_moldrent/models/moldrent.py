
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError



class ProductMolderent(models.Model):
    _name = 'product.moldrent'

    ##################
    #campos genericos#
    ##################
    name = fields.Char(string="Nombre", required=True)
    default_code = fields.Char(string="SKU", )
    
    
    
    
    #################
    #campos moldrent#
    #################
    date_moldrent = fields.Date(string="Fecha Moldrent", default=fields.Date.today())
    caracteristicas_tecnicas = fields.Html(string="Características técnicas", )
    descripcion_corta = fields.Text(string="Descripción corta", )
    tipo_moldrent = fields.Selection([('P', 'Pieza'),('M', 'Molde'),], string="Tipo Moldrent", )
    formulario_moldrent = fields.Html(string="Formulario de producto", )
    
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
    pieza_asociada_id = fields.Many2one('product.moldrent', string="Producto asociado",)
    
    #piezas
    precio_desde = fields.Float('Precio desde', digits = (8,2))
    muestras_contenedor = fields.Char(string="Muestras por contenedor", )
    precio_contenedor = fields.Float('Precio por contenedor', digits = (8,2))
    molde_asociado_id = fields.Many2one('product.moldrent', string="Molde asociado",)
    
    #adjuntos
    attachments = fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_moldrent_attach_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Adjuntos")
    

    
    
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
            #if record.lugar_envio and record.precio_asociado:
            #    lugar_envio_precio = '"[{""field_5dfc844d04e78"":""' + record.lugar_envio + '"",""field_5dfc846804e79"":""' + str(record.precio_asociado) + '""},'
            #    lugar_envio_precio = lugar_envio_precio + '""},{""field_5dfc844d04e78"":""Otro"",""field_5dfc846804e79"":""0""}""]"'
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
    

    
