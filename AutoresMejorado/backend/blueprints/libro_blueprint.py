from flask import Blueprint, request, jsonify, g
from flask_cors import cross_origin
from backend.blueprints.auth_blueprint import token_required, admin_required
from backend.models.postgres_libro_model import LibroModel

model = LibroModel()
libro_blueprint = Blueprint('libro_blueprint', __name__)

@libro_blueprint.route('/libro', methods=['POST'])
@cross_origin()
@token_required
def crear_libro():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
            
        # Validar datos requeridos
        campos_requeridos = ['titulo', 'anio', 'genero_id', 'autores_ids']
        for campo in campos_requeridos:
            if campo not in data:
                return jsonify({"error": f"El campo '{campo}' es requerido"}), 400
                
        content, status = model.crear_libro(
            data['titulo'], 
            data['anio'], 
            data['genero_id'],
            data['autores_ids']
        )
        return jsonify(content), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@libro_blueprint.route('/libro/<int:libro_id>', methods=['PUT'])
@cross_origin()
@token_required
def actualizar_libro(libro_id):
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
            
        # Validar datos requeridos
        campos_requeridos = ['titulo', 'anio', 'genero_id', 'autores_ids']
        for campo in campos_requeridos:
            if campo not in data:
                return jsonify({"error": f"El campo '{campo}' es requerido"}), 400
                
        content, status = model.actualizar_libro(
            libro_id,
            data['titulo'], 
            data['anio'], 
            data['genero_id'],
            data['autores_ids']
        )
        return jsonify(content), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@libro_blueprint.route('/libro/<int:libro_id>', methods=['DELETE'])
@cross_origin()
@token_required
@admin_required
def eliminar_libro(libro_id):
    try:
        content, status = model.eliminar_libro(libro_id)
        return jsonify(content), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@libro_blueprint.route('/libro/<int:libro_id>', methods=['GET'])
@cross_origin()
def obtener_libro(libro_id):
    try:
        content, status = model.obtener_libro(libro_id)
        return jsonify(content), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@libro_blueprint.route('/libros', methods=['GET'])
@cross_origin()
def obtener_libros():
    try:
        content, status = model.obtener_libros()
        return jsonify(content), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@libro_blueprint.route('/libro/<int:libro_id>/autores', methods=['GET'])
@cross_origin()
def obtener_autores_por_libro(libro_id):
    try:
        content, status = model.obtener_autores_por_libro(libro_id)
        return jsonify(content), status
    except Exception as e:
        return jsonify({"error": str(e)}), 500