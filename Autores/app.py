from flask import Flask, jsonify
from flask_cors import CORS
from routes import api

# Inicializar la aplicación Flask
app = Flask(__name__)
CORS(app)  # Permitir CORS para todas las rutas

# Registrar blueprint
app.register_blueprint(api)

# Ruta raíz
@app.route('/', methods=['GET'])
def index():
    return jsonify({'mensaje': '¡Bienvenido a la API de Biblioteca!'})

# Iniciar el servidor
if __name__ == "__main__":
    app.run(debug=True)