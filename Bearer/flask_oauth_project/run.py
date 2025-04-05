from threading import Thread
from app.oauth_server import oauth_server
from app.backend_server import backend_server

if __name__ == "__main__":
    Thread(target=lambda: oauth_server.run(port=5000, debug=True, use_reloader=False)).start()
    Thread(target=lambda: backend_server.run(port=5001, debug=True, use_reloader=False)).start()
