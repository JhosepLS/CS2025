from flask import Flask, request, jsonify
import jwt
import datetime

SECRET_KEY = "mi_secreto_super_seguro"

oauth_server = Flask(__name__)

@oauth_server.route("/token", methods=["POST"])
def generate_token():
    data = request.json
    if not data or data.get("client_id") != "Diego":
        return jsonify({"error": "Invalid client_id"}), 400
    
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({"exp": expiration}, SECRET_KEY, algorithm="HS256")
    return jsonify({"token": token})

if __name__ == "__main__":
    oauth_server.run(port=5000, debug=True)
