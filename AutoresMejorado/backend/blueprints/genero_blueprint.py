from flask import Blueprint, request, jsonify, g
from flask_cors import cross_origin
from backend.blueprints.auth_blueprint import token_required, admin_required
from backend.models.postgres_genero_model import GeneroModel

model = GeneroModel()
genero_blueprint = Blueprint('genero_blueprint', __name__)

@genero_blueprint.route('/genero', methods=['POST'])
@cross_origin()
@token_required
@admin_required
def crear_genero():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
            
        # Validar datos requeridos
        if 'nombre' not in data:
            return jsonify({"error": "El nombre del género es requerido"}), 400
                
        content, status = model.crear_genero(
            data['nombre'], 
            data.get('descripcion')
        )
        return jsonify(content), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@genero_blueprint.route('/genero/<int:genero_id>', methods=['PUT'])
@cross_origin()
@token_required
@admin_required
def actualizar_genero(genero_id):
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
            
        # Validar datos requeridos
        if 'nombre' not in data:
            return jsonify({"error": "El nombre del género es requerido"}), 400
                
        content, status = model.actualizar_genero(
            genero_id,
            data['nombre'], 
            data.get('descripcion')
        )
        return jsonify(content), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@genero_blueprint.route('/genero/<int:genero_id>', methods=['DELETE'])
@cross_origin()
@token_required
@admin_required
def eliminar_genero(genero_id):
    try:
        content, status = model.eliminar_genero(genero_id)
        return jsonify(content), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@genero_blueprint.route('/genero/<int:genero_id>', methods=['GET'])
@cross_origin()
def obtener_genero(genero_id):
    try:
        content, status = model.obtener_genero(genero_id)
        return jsonify(content), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@genero_blueprint.route('/generos', methods=['GET'])
@cross_origin()
def obtener_generos():
    try:
        content, status = model.obtener_generos()
        return jsonify(content), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500