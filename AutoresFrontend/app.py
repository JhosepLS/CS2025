from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Importar blueprints
from backend.blueprints.auth_blueprint import auth_blueprint
from backend.blueprints.autor_blueprint import autor_blueprint
from backend.blueprints.libro_blueprint import libro_blueprint
from backend.blueprints.genero_blueprint import genero_blueprint

# Inicializar aplicación Flask
app = Flask(__name__)

# Registrar blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(autor_blueprint)
app.register_blueprint(libro_blueprint)
app.register_blueprint(genero_blueprint)

# Configurar CORS
CORS(app)

# Ruta raíz
@app.route('/', methods=['GET'])
def index():
    return jsonify({'mensaje': '¡Bienvenido a la API de Biblioteca con PostgreSQL!'})

# Ruta para verificar estado
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'version': '1.0.0'})

# Ejecutar la aplicación
if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)