from flask import Flask, request, jsonify
from db import get_connection
from datetime import datetime

app = Flask(__name__)

@app.route("/api/usuarios", methods=["POST"])
def agregar_usuario():
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
        conn.close()

        return jsonify({"mensaje": "Usuario agregado exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/usuarios", methods=["GET"])
def obtener_usuario():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("EXEC get_user")
        rows = cursor.fetchall()

        users =[]
        for row in rows:
            users.append({
                "id":row[0],
                "nombre":row[1],
                "email":row[2],
                "fecha_registro": str(row[3])
            })

        cursor.close()
        conn.close()

        return jsonify(users), 200
    except Exception as e: 
        return jsonify({"error": str(e)}), 500


@app.route("/api/usuarios/<int:id_usuario>", methods=["DELETE"])
def eliminar_usuario(id_usuario):
    try: 
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("EXEC delete_user @id = ?", (id_usuario,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"mensaje":f"Usario con ID {id_usuario} eliminado"}), 200
    
    except Exception as e: 
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
