
from odoo import fields, models, api



class HrAttendance(models.Model):
    _inherit = 'hr.attendance'
    
    comentario = fields.Char(string="Comentario")
    
    

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    
    #campos
    personal_phone = fields.Char(string="Teléfono personal")
    personal_mobile = fields.Char(string="Móvil personal")
    personal_email = fields.Char(string="Email personal")
    personal_bank = fields.Char(string="Cuenta bancaria")
    
    talla_camisa = fields.Char(string="Talla camisa")
    talla_pantalones = fields.Char(string="Talla pantalones")
    talla_sueter = fields.Char(string="Talla suéter")
    talla_zapato = fields.Char(string="Talla zapato")
    
    maquina_id = fields.Many2one('mrp.workcenter', string="Máquina")
    
    
    
    
    #costes
    coste_extra = fields.Float(string="Coste hora extra")
    coste_festivo = fields.Float(string="Coste Sábado / festivo")
    
    
    #DOCUMENTACION
    
    file_documentos = fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_hr_documentos_attach_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Documentos")
                                
    file_contratos = fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_hr_contratos_attach_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Contratos")
                                
    file_curriculum = fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_hr_curriculum_attach_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Curriculum")
                                
    file_formacion = fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_hr_formacion_attach_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Formación")

    file_reconocimiento = fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_hr_reconocimiento_attach_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Reconocimiento médico")

    file_amonestaciones = fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_hr_amonestaciones_attach_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Amonestaciones")

    file_funciones = fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_hr_funciones_attach_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Funciones")
                                
    #campos relacionados
    vida_laboral_ids = fields.One2many(
        comodel_name='hr.employee.laboral',
        inverse_name='employee_id'
    )
    
    formacion_ids = fields.One2many(
        comodel_name='hr.employee.formacion',
        inverse_name='employee_id'
    )
    
    resource_planning_id = fields.Many2one(
        comodel_name='resource.resource',
        string="Recurso planificación"
    )

    
 




class HrEmployeeLaboral(models.Model):
    _name='hr.employee.laboral'

    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string="Empleado", required=True
    )

    date = fields.Date(string="Fecha", required=True)
    contract_type = fields.Selection([('Temporal', 'Temporal'),('Indefinido', 'Indefinido'),('Practicas', 'Contrato en prácticas'),('FP', 'FP Dual'),('FCT', 'FCT')], string="Tipo de contrato", required=True)

    duration = fields.Selection([('1', '1 mes'),('3', '3 meses'),('6', '6 meses'),('12', '1 año'), ('24', '2 años')], string="Duración", )
    categoria_id = fields.Many2one('hr.job', string="Puesto de trabajo")
    categoria_oficial_id = fields.Many2one('hr.job.category', string="Categoría")
    salario_bruto = fields.Integer(string="Salario bruto")
    date_finalizacion = fields.Date(string="Finalización")
    bonificacion = fields.Char(string="Bonificación")
    cuantia_bonificada = fields.Integer(string="Cuantía bonificada")
    
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_emp_contratos_attach_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Adjuntos")
    
    

class HrJobCategory(models.Model):
    _name='hr.job.category'
    
    name = fields.Char(string="Nombre", required=True)

    
class HrEmployeeFormacion(models.Model):
    _name='hr.employee.formacion'

    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string="Empleado", required=True
    )

    date = fields.Date(string="Fecha", required=True)
    curso = fields.Char(string="Curso", required=True)
    duracion = fields.Char(string="Duración")
    ponente = fields.Char(string="Ponente")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", 
                                relation="m2m_emp_formacion_attach_rel", 
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Adjuntos")
                                
                                
class HrHorasExtra(models.Model):
    _name='hr.horas.extra'

    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string="Empleado", required=True
    )

    date = fields.Date(string="Fecha", required=True)
    horas = fields.Float(string="Horas extra")


