from flask import Blueprint, request, jsonify
from models import Autor, Libro

# Blueprint para la API
api = Blueprint('api', __name__)

# Rutas para Autores
@api.route('/autores', methods=['GET'])
def obtener_autores():
    return jsonify(Autor.obtener_todos())

@api.route('/autor/<int:id>', methods=['GET'])
def obtener_autor(id):
    autor = Autor.obtener_por_id(id)
    if autor:
        return jsonify(autor)
    return jsonify({'error': 'Autor no encontrado'}), 404

@api.route('/autor', methods=['POST'])
def crear_autor():
    data = request.json
    resultado = Autor.crear(
        data['nombre'],
        data['pais'],
        data['anio']
    )
    return jsonify(resultado), 201

@api.route('/autor/<int:id>', methods=['PUT'])
def actualizar_autor(id):
    data = request.json
    resultado = Autor.actualizar(
        id,
        data['nombre'],
        data['pais'],
        data['anio']
    )
    return jsonify(resultado)

@api.route('/autor/<int:id>', methods=['DELETE'])
def eliminar_autor(id):
    resultado = Autor.eliminar(id)
    return jsonify(resultado)

# Rutas para Libros
@api.route('/libros', methods=['GET'])
def obtener_libros():
    return jsonify(Libro.obtener_todos())

@api.route('/libro/<int:id>', methods=['GET'])
def obtener_libro(id):
    libro = Libro.obtener_por_id(id)
    if libro:
        return jsonify(libro)
    return jsonify({'error': 'Libro no encontrado'}), 404

@api.route('/libros/autor/<int:autor_id>', methods=['GET'])
def obtener_libros_por_autor(autor_id):
    return jsonify(Libro.obtener_por_autor(autor_id))

@api.route('/libro', methods=['POST'])
def crear_libro():
    data = request.json
    resultado = Libro.crear(
        data['titulo'],
        data['anio'],
        data['genero'],
        data['autor_id']
    )
    return jsonify(resultado), 201

@api.route('/libro/<int:id>', methods=['PUT'])
def actualizar_libro(id):
    data = request.json
    resultado = Libro.actualizar(
        id,
        data['titulo'],
        data['anio'],
        data['genero'],
        data['autor_id']
    )
    return jsonify(resultado)

@api.route('/libro/<int:id>', methods=['DELETE'])
def eliminar_libro(id):
    resultado = Libro.eliminar(id)
    return jsonify(resultado)