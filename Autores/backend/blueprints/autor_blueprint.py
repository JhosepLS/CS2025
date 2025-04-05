from flask import Blueprint
from flask import request
from flask import jsonify
from flask_cors import cross_origin 

from backend.models.sqlite_autor_model import AutorModel
model = AutorModel()

autor_blueprint = Blueprint('autor_blueprint', __name__)

@autor_blueprint.route('/autor', methods=['POST'])
@cross_origin()
def crear_autor():
    content = model.crear_autor(
        request.json['nombre'], 
        request.json['pais'], 
        request.json['anio']
    )    
    return jsonify(content)

@autor_blueprint.route('/autor/<int:autor_id>', methods=['PUT'])
@cross_origin()
def actualizar_autor(autor_id):
    content = model.actualizar_autor(
        autor_id, 
        request.json['nombre'], 
        request.json['pais'], 
        request.json['anio']
    )    
    return jsonify(content)

@autor_blueprint.route('/autor/<int:autor_id>', methods=['DELETE'])
@cross_origin()
def eliminar_autor(autor_id):
    return jsonify(model.eliminar_autor(autor_id))

@autor_blueprint.route('/autor/<int:autor_id>', methods=['GET'])
@cross_origin()
def autor(autor_id):
    return jsonify(model.obtener_autor(autor_id))

@autor_blueprint.route('/autores', methods=['GET'])
@cross_origin()
def autores():
    return jsonify(model.obtener_autores())