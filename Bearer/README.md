# Instrucciones

## Pre-requisitos
- Instalar Postman --> [Pagina de Postman](https://learning.postman.com)
- Python

### 1. Clonar Repositorio 
```bash
git clone https://github.com/JhosepLS/CS2025.git
```

### 2. Instalar Flask
```bash
pip install flask pyjwt
```

### 3. Ejecutar codigo run.py
```bash
from threading import Thread
from app.oauth_server import oauth_server
from app.backend_server import backend_server

if __name__ == "__main__":
    Thread(target=lambda: oauth_server.run(port=5000, debug=True, use_reloader=False)).start()
    Thread(target=lambda: backend_server.run(port=5001, debug=True, use_reloader=False)).start()
```
### 4. Postman
Crear Post y Get. En el Get colocar la URL:
```bash
http://127.0.0.1:5000/token
```
Colcar en el body el ID del cliente pre-establesido:
```bash
{
  "client_id": "Paneton"
}
```
### 4.1 (Parametros opcionales)
Definir los parametros con:

**Key**   --> Content-Type

**Value** --> application/json



### 5. Header
Colocar los siguientes parametros

**Key** --> Authorization

**Value** --> Beare *"Token"*

## Integrantes:
- Jhosep Alonso Mollapaza Morocco
- Diego Alessandro Alvarez Cruz
- José Carlos Machaca Vera
