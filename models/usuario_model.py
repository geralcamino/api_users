from flask_restx import fields

def get_usuario_model(api):
    return api.model('Usuario', {
        'nombre': fields.String(required=True, description='Nombre del usuario'),
        'email': fields.String(required=True, description='Correo electrónico'),
        'fecha_registro': fields.String(required=True, description='Fecha de registro (ISO)')
    })
