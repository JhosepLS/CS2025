# API Biblioteca (Mejorada) con PostgreSQL

## Requisitos previos

1. **Python 3.8 o superior**
2. **PostgreSQL 12 o superior**
3. **Postman** para probar la API

## Instalación

### 1. Clonar el repositorio

```bash# I API Biblioteca (mejorado) con PostgreSQL

## Requisitos previos

1. **Python 3.8 o superior**
2. **PostgreSQL 12 o superior**
3. **Postman** para probar la API

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/JhosepLS/CS2025.git
cd CS2025/Autores
```

### 2. Crear un entorno virtual

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

Alternativa más simple (usando el requirements.txt actualizado):

```bash
pip install -r requirements.txt
```

Nota: Si encuentras problemas con algún paquete, intenta instalarlo individualmente como se muestra ahora

Para una instalación más robusta, instalar cada paquete individualmente:
```bash
# Instalar Flask y dependencias principales
pip install flask==2.3.3
pip install flask-cors==4.0.0

# Instalar PostgreSQL
pip install psycopg2-binary==2.9.10

# Instalar dotenv
python -m pip install python-dotenv==1.0.0

# Instalar bcrypt con flask-bcrypt
pip install flask-bcrypt==1.0.1

# Instalar JWT para autenticación
pip install PyJWT==2.8.0
```

### 4. Configurar variables de entorno

Crea un archivo `.env` basado en `.env.example`:

```bash
# Windows
copy .env.example .env
```

Edita el archivo `.env` con tus credenciales de PostgreSQL:

En este caso:
```
DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=admin
DB_NAME=biblioteca_db
DB_PORT=5432
```

### 5. Configurar la base de datos

Asegúrate de que PostgreSQL esté en ejecución y luego ejecuta:

```bash
python db_setup.py
```
### 6. Iniciar la aplicación

```bash
python app.py
```

La API estará disponible en `http://localhost:5000`


## Flujo de Pruebas

### 1. Autenticación

#### Registrar un nuevo usuario

1. Crea una nueva solicitud:
   - Método: POST
   - URL: `http://localhost:5000/auth/register`
   - Body:
   ```json
   {
       "username": "nuevo_usuario",
       "password": "contrasena123",
       "email": "usuario@example.com"
   }
   ```
2. Envía la solicitud
3. Deberías recibir una respuesta 201 con los datos del usuario creado

#### Iniciar sesión y obtener token

1. Crea una nueva solicitud:
   - Método: POST
   - URL: `http://localhost:5000/auth/login`
   - Body:
   ```json
   {
       "username": "admin",
       "password": "admin123"
   }
   ```
2. Envía la solicitud
3. Deberías recibir una respuesta 200 con un token JWT
4. **Importante**: Copia este token y guárdalo en la variable de entorno `token`

#### Verificar tu token

1. Crea una nueva solicitud:
   - Método: GET
   - URL: `http://localhost:5000/auth/verify`
   - Headers: `Authorization: Bearer (token)`
2. Envía la solicitud
3. Deberías recibir una respuesta 200 confirmando que el token es válido

### 2. Géneros

#### Obtener todos los géneros

1. Crea una nueva solicitud:
   - Método: GET
   - URL: `http://localhost:5000/generos`
2. Envía la solicitud
3. Deberías recibir una lista de géneros

#### Crear un nuevo género (requiere token de administrador)

1. Crea una nueva solicitud:
   - Método: POST
   - URL: `http://localhost:5000/genero`
   - Headers: 
     - `Authorization: Bearer (token)`
   - Body:
   ```json
   {
       "nombre": "Biografía",
       "descripcion": "Obras que narran la vida de una persona"
   }
   ```
2. Envía la solicitud
3. Deberías recibir una respuesta 201 con los datos del género creado

### 3. Autores

#### Obtener todos los autores

1. Crea una nueva solicitud:
   - Método: GET
   - URL: `http://localhost:5000/autores`
2. Envía la solicitud
3. Deberías recibir una lista de autores

#### Crear un nuevo autor (requiere token)

1. Crea una nueva solicitud:
   - Método: POST
   - URL: `http://localhost:5000/autor`
   - Headers: 
     - `Authorization: Bearer (token)`
   - Body:
   ```json
   {
       "nombre": "Mario Vargas Llosa",
       "pais": "Perú",
       "anio": 1936
   }
   ```
2. Envía la solicitud
3. Deberías recibir una respuesta 201 con los datos del autor creado
4. **Guarda el `autor_id`** para usarlo más adelante

#### Actualizar un autor (requiere token)

1. Crea una nueva solicitud:
   - Método: PUT
   - URL: `http://localhost:5000/autor/6` (usa el ID del autor creado anteriormente)
   - Headers: 
     - `Content-Type: application/json`
     - `Authorization: Bearer (token)`
   - Body:
   ```json
   {
       "nombre": "Mario Vargas Llosa",
       "pais": "Perú",
       "anio": 1935
   }
   ```
2. Envía la solicitud
3. Deberías recibir una respuesta 200 con los datos actualizados

### 4. Libros

#### Obtener todos los libros

1. Crea una nueva solicitud:
   - Método: GET
   - URL: `http://localhost:5000/libros`
2. Envía la solicitud
3. Deberías recibir una lista de libros con sus autores y géneros

#### Crear un nuevo libro (requiere token)

1. Crea una nueva solicitud:
   - Método: POST
   - URL: `http://localhost:5000/libro`
   - Headers: 
     - `Authorization: Bearer (token)`
   - Body:
   ```json
   {
       "titulo": "La ciudad y los perros",
       "anio": 1963,
       "genero_id": 1,
       "autores_ids": [6]
   }
   ```
   Nota: Usa el ID del género "Novela" (que es 1) y el ID del autor que creaste anteriormente.

2. Envía la solicitud
3. Deberías recibir una respuesta 201 con los datos del libro creado
4. **Guarda el `libro_id`** para usarlo más adelante

#### Obtener un libro específico

1. Crea una nueva solicitud:
   - Método: GET
   - URL: `http://localhost:5000/libro/6` (usa el ID del libro creado anteriormente)
2. Envía la solicitud
3. Deberías recibir los datos completos del libro, incluyendo los autores

#### Obtener todos los autores de un libro

1. Crea una nueva solicitud:
   - Método: GET
   - URL: `http://localhost:5000/libro/6/autores` (usa el ID del libro creado anteriormente)
2. Envía la solicitud
3. Deberías recibir la lista de autores de ese libro

#### Obtener todos los libros de un autor

1. Crea una nueva solicitud:
   - Método: GET
   - URL: `http://localhost:5000/autor/6/libros` (usa el ID del autor creado anteriormente)
2. Envía la solicitud
3. Deberías recibir la lista de libros escritos por ese autor

#### Actualizar un libro para agregarle otro autor (requiere token)

1. Crea una nueva solicitud:
   - Método: PUT
   - URL: `http://localhost:5000/libro/6` (usa el ID del libro creado anteriormente)
   - Headers: 
     - `Authorization: Bearer (token)`
   - Body:
   ```json
   {
       "titulo": "La ciudad y los perros",
       "anio": 1963,
       "genero_id": 1,
       "autores_ids": [6, 1]
   }
   ```
   Nota: Ahora el libro tiene dos autores (el ID 6 que creamos y el ID 1 que ya existía)

2. Envía la solicitud
3. Deberías recibir una respuesta 200 con los datos actualizados

### 5. Probar validaciones y errores

#### Intentar crear un autor con nombre duplicado

1. Crea una nueva solicitud:
   - Método: POST
   - URL: `http://localhost:5000/autor`
   - Headers: 
     - `Authorization: Bearer (token)`
   - Body:
   ```json
   {
       "nombre": "Mario Vargas Llosa",
       "pais": "España",
       "anio": 1940
   }
   ```
2. Envía la solicitud
3. Deberías recibir un error 409 (Conflict) indicando que ya existe un autor con ese nombre

#### Intentar crear un libro sin título

1. Crea una nueva solicitud:
   - Método: POST
   - URL: `http://localhost:5000/libro`
   - Headers: 
     - `Authorization: Bearer (token)`
   - Body:
   ```json
   {
       "titulo": "",
       "anio": 2000,
       "genero_id": 1,
       "autores_ids": [1]
   }
   ```
2. Envía la solicitud
3. Deberías recibir un error 400 indicando que el título es obligatorio

#### Intentar crear un libro con un autor inexistente

1. Crea una nueva solicitud:
   - Método: POST
   - URL: `http://localhost:5000/libro`
   - Headers: 
     - `Authorization: Bearer (token)`
   - Body:
   ```json
   {
       "titulo": "Libro con autor inexistente",
       "anio": 2000,
       "genero_id": 1,
       "autores_ids": [999]
   }
   ```
2. Envía la solicitud
3. Deberías recibir un error 404 indicando que el autor con ID 999 no existe

### 6. Probar eliminación lógica

#### Eliminar un autor (requiere token de administrador)

1. Crea una nueva solicitud:
   - Método: DELETE
   - URL: `http://localhost:5000/autor/6` (usa el ID del autor creado anteriormente)
   - Headers: `Authorization: Bearer (token)`
2. Envía la solicitud
3. Deberías recibir una respuesta 200 indicando que el autor fue marcado como eliminado

#### Verificar que el autor no aparece en la lista

1. Crea una nueva solicitud:
   - Método: GET
   - URL: `http://localhost:5000/autores`
2. Envía la solicitud
3. El autor que eliminaste no debería aparecer en la lista (borrado lógico)

#### Verificar que no se puede acceder al autor eliminado

1. Crea una nueva solicitud:
   - Método: GET
   - URL: `http://localhost:5000/autor/6` (usa el ID del autor eliminado)
2. Envía la solicitud
3. Deberías recibir un error 404 indicando que el autor no existe o ha sido eliminado

### 7. Probar protección de rutas administrativas

#### Cerrar sesión e iniciar con usuario normal

1. Cierra sesión eliminando el token actual
2. Inicia sesión con el usuario normal:
   - Método: POST
   - URL: `http://localhost:5000/auth/login`
   - Headers: `Content-Type: application/json`
   - Body:
   ```json
   {
       "username": "usuario",
       "password": "user123"
   }
   ```
3. Guarda el nuevo token en la variable de entorno

#### Intentar eliminar un género (solo admin)

1. Crea una nueva solicitud:
   - Método: DELETE
   - URL: `http://localhost:5000/genero/6`
   - Headers: `Authorization: Bearer (token)`
2. Envía la solicitud
3. Deberías recibir un error 403 indicando que se requieren privilegios de administrador

### Endpoints disponibles

#### Autenticación
- **POST /auth/register** - Registrar nuevo usuario
- **POST /auth/login** - Iniciar sesión
- **GET /auth/verify** - Verificar token (requiere autenticación)

#### Autores
- **GET /autores** - Listar todos los autores
- **GET /autor/{id}** - Obtener un autor por ID
- **GET /autor/{id}/libros** - Obtener libros de un autor
- **POST /autor** - Crear autor (requiere autenticación)
- **PUT /autor/{id}** - Actualizar autor (requiere autenticación)
- **DELETE /autor/{id}** - Eliminar autor (requiere autenticación de administrador)

#### Libros
- **GET /libros** - Listar todos los libros
- **GET /libro/{id}** - Obtener libro por ID
- **GET /libro/{id}/autores** - Obtener autores de un libro
- **POST /libro** - Crear libro (requiere autenticación)
- **PUT /libro/{id}** - Actualizar libro (requiere autenticación)
- **DELETE /libro/{id}** - Eliminar libro (requiere autenticación de administrador)

#### Géneros
- **GET /generos** - Listar todos los géneros
- **GET /genero/{id}** - Obtener género por ID
- **POST /genero** - Crear género (requiere autenticación de administrador)
- **PUT /genero/{id}** - Actualizar género (requiere autenticación de administrador)
- **DELETE /genero/{id}** - Eliminar género (requiere autenticación de administrador)
