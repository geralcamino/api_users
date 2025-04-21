from flask import request
from flask_restx import Namespace, Resource
from datetime import datetime
from db import get_connection
from models.usuario_model import get_usuario_model

api = Namespace("usuarios", path="/api/usuarios", description="Operaciones con usuarios")
usuario_model = get_usuario_model(api)

@api.route("/")
class UsuarioList(Resource):
    @api.doc("obtener_usuarios")
    def get(self):
        """Obtener todos los usuarios"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("EXEC get_user")
            rows = cursor.fetchall()

            users = []
            for row in rows:
                users.append({
                    "id": row[0],
                    "nombre": row[1],
                    "email": row[2],
                    "fecha_registro": str(row[3])
                })

            cursor.close()
            conn.close()

            return users, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @api.doc("agregar_usuario")
    @api.expect(usuario_model)
    def post(self):
        """Agregar un nuevo usuario"""
        try:
            data = request.get_json()
            nombre = data.get("nombre")
            email = data.get("email")
            fecha_registro = data.get("fecha_registro")

            fecha_dt = datetime.fromisoformat(fecha_registro)

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("EXEC add_user @nombre = ?, @email = ?, @fecha_registro = ?", 
                           (nombre, email, fecha_dt))
            conn.commit()
            cursor.close()
            conn.close()

            return {"mensaje": "Usuario agregado exitosamente"}, 201
        except Exception as e:
            return {"error": str(e)}, 500

@api.route("/<int:id_usuario>")
@api.param("id_usuario", "ID del usuario a eliminar")
class Usuario(Resource):
    @api.doc("eliminar_usuario")
    def delete(self, id_usuario):
        """Eliminar un usuario por ID"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("EXEC delete_user @id = ?", (id_usuario,))
            affected_rows = cursor.rowcount

            if affected_rows == 0:
                cursor.close()
                conn.close()
                return {"mensaje": "Usuario no encontrado"}, 404

            conn.commit()
            cursor.close()
            conn.close()
            return {"mensaje": f"Usuario con ID {id_usuario} eliminado"}, 200

        except Exception as e:
            return {"error": str(e)}, 500
