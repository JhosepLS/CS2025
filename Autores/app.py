from flask import Flask
from flask import jsonify
from flask_cors import CORS

from backend.blueprints.libro_blueprint import libro_blueprint
from backend.blueprints.autor_blueprint import autor_blueprint

app = Flask(__name__)

app.register_blueprint(libro_blueprint)
app.register_blueprint(autor_blueprint)

cors = CORS(app)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'mensaje': '¡Bienvenido a la API de Biblioteca!'})

if __name__ == "__main__":
    app.run(debug=True)