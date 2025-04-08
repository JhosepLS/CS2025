from flask import Blueprint, request, jsonify, g
from flask_cors import cross_origin
from backend.blueprints.auth_blueprint import token_required, admin_required
from backend.models.postgres_autor_model import AutorModel

model = AutorModel()
autor_blueprint = Blueprint('autor_blueprint', __name__)

@autor_blueprint.route('/autor', methods=['POST'])
@cross_origin()
@token_required
def crear_autor():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
            
        # Validar datos requeridos
        if 'nombre' not in data:
            return jsonify({"error": "El nombre del autor es requerido"}), 400
                
        content, status = model.crear_autor(
            data['nombre'], 
            data.get('pais'), 
            data.get('anio')
        )
        return jsonify(content), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@autor_blueprint.route('/autor/<int:autor_id>', methods=['PUT'])
@cross_origin()
@token_required
def actualizar_autor(autor_id):
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
            
        # Validar datos requeridos
        if 'nombre' not in data:
            return jsonify({"error": "El nombre del autor es requerido"}), 400
                
        content, status = model.actualizar_autor(
            autor_id,
            data['nombre'], 
            data.get('pais'), 
            data.get('anio')
        )
        return jsonify(content), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@autor_blueprint.route('/autor/<int:autor_id>', methods=['DELETE'])
@cross_origin()
@token_required
@admin_required
def eliminar_autor(autor_id):
    try:
        content, status = model.eliminar_autor(autor_id)
        return jsonify(content), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@autor_blueprint.route('/autor/<int:autor_id>', methods=['GET'])
@cross_origin()
def obtener_autor(autor_id):
    try:
        content, status = model.obtener_autor(autor_id)
        return jsonify(content), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@autor_blueprint.route('/autores', methods=['GET'])
@cross_origin()
def obtener_autores():
    try:
        content, status = model.obtener_autores()
        return jsonify(content), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@autor_blueprint.route('/autor/<int:autor_id>/libros', methods=['GET'])
@cross_origin()
def obtener_libros_por_autor(autor_id):
    try:
        content, status = model.obtener_libros_por_autor(autor_id)
        return jsonify(content), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500