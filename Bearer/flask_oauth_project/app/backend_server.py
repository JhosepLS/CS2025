from flask import Flask, request, jsonify
import jwt
import functools

SECRET_KEY = "mi_secreto_super_seguro"

backend_server = Flask(__name__)

def token_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token requerido"}), 400

        try:
            parts = token.split()
            if len(parts) != 2 or parts[0] != "Bearer":
                return jsonify({"error": "Formato de token inválido"}), 401

            jwt.decode(parts[1], SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401
        
        return f(*args, **kwargs)
    
    return decorated

@backend_server.route("/secure-data", methods=["GET"])
@token_required
def secure_data():
    return jsonify({"message": "Acceso autorizado", "data": "Información segura"})

if __name__ == "__main__":
    backend_server.run(port=5001, debug=True)
