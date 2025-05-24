from flask import Blueprint, request, jsonify, g
from flask_cors import cross_origin
from functools import wraps
import os

from backend.models.postgres_auth_model import AuthModel

auth_model = AuthModel()
auth_blueprint = Blueprint('auth_blueprint', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Buscar token en headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Token requerido'}), 401
        
        # Verificar token
        data, status = auth_model.verify_token(token)
        if status != 200:
            return jsonify(data), status
        
        # Almacenar datos del usuario en el contexto g
        g.user = data
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # token_required debe usarse primero
        if not hasattr(g, 'user'):
            return jsonify({'error': 'No autenticado'}), 401
        
        if g.user.get('role') != 'admin':
            return jsonify({'error': 'Se requieren privilegios de administrador'}), 403
        
        return f(*args, **kwargs)
    
    return decorated

@auth_blueprint.route('/auth/register', methods=['POST'])
@cross_origin()
def register():
    data = request.json
    
    if not data or not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({'error': 'Datos incompletos. Se requiere username, password y email'}), 400
    
    # Si se especifica role y no eres admin, ignora el role solicitado
    if 'role' in data and data['role'] == 'admin':
        # En registro público, no permitir crear admins
        data['role'] = 'usuario'
    
    result, status = auth_model.registrar_usuario(
        data['username'], 
        data['password'],
        data['email'],
        data.get('role', 'usuario')
    )
    
    return jsonify(result), status

@auth_blueprint.route('/auth/login', methods=['POST'])
@cross_origin()
def login():
    data = request.json
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Se requiere username y password'}), 400
    
    result, status = auth_model.login(data['username'], data['password'])
    return jsonify(result), status

@auth_blueprint.route('/auth/verify', methods=['GET'])
@cross_origin()
@token_required
def verify_token():
    return jsonify({
        'message': 'Token válido',
        'user': {
            'user_id': g.user['user_id'],
            'username': g.user['username'],
            'role': g.user['role']
        }
    }), 200