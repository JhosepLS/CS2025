from backend.models.postgres_connection import PostgresConnection
from flask_bcrypt import Bcrypt
import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
bcrypt = Bcrypt()

class AuthModel:
    def __init__(self):
        self.db = PostgresConnection()
        self.secret_key = os.getenv('JWT_SECRET_KEY', 'clave_secreta_predeterminada')

    def registrar_usuario(self, username, password, email, role='usuario'):
        """Registra un nuevo usuario"""
        try:
            # Verificar si el usuario ya existe
            query = "SELECT * FROM usuarios WHERE username = %s"
            user = self.db.execute_query(query, (username,))
            
            if user:
                return {"error": "El nombre de usuario ya existe"}, 400
            
            # Hash de la contraseña usando flask_bcrypt
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            
            # Insertar nuevo usuario
            query = """
                INSERT INTO usuarios (username, password, email, role, is_active)
                VALUES (%s, %s, %s, %s, true)
                RETURNING user_id, username, email, role
            """
            result = self.db.execute_query(query, (username, hashed_password, email, role), True)
            
            return result, 201
        except Exception as e:
            return {"error": str(e)}, 500

    def login(self, username, password):
        """Autentica un usuario y genera un token JWT"""
        try:
            # Buscar usuario
            query = "SELECT * FROM usuarios WHERE username = %s AND is_active = true"
            users = self.db.execute_query(query, (username,))
            
            if not users:
                return {"error": "Usuario no encontrado o inactivo"}, 404
            
            user = users[0]
            
            # Verificar contraseña usando flask_bcrypt
            if not bcrypt.check_password_hash(user['password'], password):
                return {"error": "Contraseña incorrecta"}, 401
            
            # Generar token
            token_payload = {
                'user_id': user['user_id'],
                'username': user['username'],
                'role': user['role'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }
            
            token = jwt.encode(token_payload, self.secret_key, algorithm='HS256')
            
            return {
                'token': token,
                'user': {
                    'user_id': user['user_id'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role']
                }
            }, 200
            
        except Exception as e:
            return {"error": str(e)}, 500

    def verify_token(self, token):
        """Verifica si un token JWT es válido"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload, 200
        except jwt.ExpiredSignatureError:
            return {"error": "Token expirado"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Token inválido"}, 401