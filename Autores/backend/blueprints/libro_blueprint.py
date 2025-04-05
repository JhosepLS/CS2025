from flask import Blueprint
from flask import request
from flask import jsonify
from flask_cors import cross_origin 

from backend.models.sqlite_libro_model import LibroModel
model = LibroModel()

libro_blueprint = Blueprint('libro_blueprint', __name__)

@libro_blueprint.route('/libro', methods=['POST'])
@cross_origin()
def crear_libro():
    content = model.crear_libro(
        request.json['titulo'], 
        request.json['anio'], 
        request.json['genero'],
        request.json['autor_id']
    )    
    return jsonify(content)

@libro_blueprint.route('/libro/<int:libro_id>', methods=['PUT'])
@cross_origin()
def actualizar_libro(libro_id):
    content = model.actualizar_libro(
        libro_id,
        request.json['titulo'], 
        request.json['anio'], 
        request.json['genero'],
        request.json['autor_id']
    )    
    return jsonify(content)

@libro_blueprint.route('/libro/<int:libro_id>', methods=['DELETE'])
@cross_origin()
def eliminar_libro(libro_id):
    return jsonify(model.eliminar_libro(libro_id))

@libro_blueprint.route('/libro/<int:libro_id>', methods=['GET'])
@cross_origin()
def libro(libro_id):
    return jsonify(model.obtener_libro(libro_id))

@libro_blueprint.route('/libros', methods=['GET'])
@cross_origin()
def libros():
    return jsonify(model.obtener_libros())

@libro_blueprint.route('/libros/autor/<int:autor_id>', methods=['GET'])
@cross_origin()
def libros_por_autor(autor_id):
    return jsonify(model.obtener_libros_por_autor(autor_id))