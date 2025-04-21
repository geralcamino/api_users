from flask import Flask
from flask_restx import Api
from routes.usuarios import api as usuarios_ns

app = Flask(__name__)
api = Api(app, title="API de Usuarios", version="1.0", description="Documentación con Swagger")

api.add_namespace(usuarios_ns)

if __name__ == '__main__':
    app.run(debug=True)
