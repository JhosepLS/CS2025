# API Biblioteca (Mejorada) con PostgreSQL + Frontend Vue.js

## Requisitos previos

1. **Python 3.8 o superior**
2. **PostgreSQL 12 o superior**
3. **Node.js 16 o superior** (para el frontend)
4. **npm** (incluido con Node.js)

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/JhosepLS/CS2025.git
cd CS2025/AutoresFrontend
```

## Configuración del Backend

### 2. Crear un entorno virtual

```bash
python -m venv venv
venv\Scripts\activate  # En Windows
# source venv/bin/activate  # En Linux/Mac
```

### 3. Instalar dependencias del backend

Instalacion usando el requirements.txt actualizado:

```bash
pip install -r requirements.txt
```

Para una instalación más robusta por si existiera algun error, instalar cada paquete individualmente:
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

```
DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=admin
DB_NAME=biblioteca_db
DB_PORT=5432
JWT_SECRET_KEY=altosecreto
PORT=5000
FLASK_ENV=development
```

### 5. Configurar la base de datos

Asegúrate de que PostgreSQL esté en ejecución y luego ejecuta:

```bash
python db_setup.py
```

## Configuración del Frontend

### 6. Instalar dependencias del frontend

```bash
cd frontend
npm install
```

Si encuentras errores durante la instalación, instala las dependencias principales manualmente:

```bash
npm install vue@3 vue-router@4 vue-toastification@2.0.0-rc.5 axios
```

## Ejecución del Sistema

Para ejecutar el sistema completo, necesitas abrir **2 terminales** diferentes:

### Terminal 1 - Backend (API)

```bash
# Desde la carpeta raíz AutoresMejorado/
venv\Scripts\activate  # En Windows
# source venv/bin/activate  # En Linux/Mac
python app.py
```

El backend estará disponible en: `http://localhost:5000`

### Terminal 2 - Frontend (Interfaz Web)

```bash
# Desde la carpeta AutoresMejorado/frontend/
npm run serve
```

El frontend estará disponible en: `http://localhost:8080`

## Acceso al Sistema

### URLs de Acceso

- **Frontend (Interfaz Web):** http://localhost:8080
- **Backend (API):** http://localhost:5000

### Credenciales de Prueba

El sistema viene con usuarios predefinidos para pruebas:

**Administrador:**
- Usuario: `admin`
- Contraseña: `admin123`
- Permisos: Gestión completa (crear, editar, eliminar autores, libros y géneros)

**Usuario Normal:**
- Usuario: `usuario`
- Contraseña: `user123`
- Permisos: Crear y editar autores y libros (no puede eliminar ni gestionar géneros)

## Funcionalidades del Sistema

### Frontend Web (Vue.js)
- **Dashboard principal** con estadísticas del sistema
- **Gestión de Autores:** Crear, ver, editar y eliminar autores
- **Gestión de Libros:** Crear, ver, editar y eliminar libros con múltiples autores
- **Gestión de Géneros:** Crear, ver, editar y eliminar géneros (solo administradores)
- **Sistema de autenticación** con roles de usuario
- **Vistas de detalle** para autores y libros
- **Filtros y búsqueda** en el catálogo de libros
- **Diseño responsive** para dispositivos móviles
- **Validaciones en tiempo real** en formularios
- **Notificaciones** para feedback del usuario

### API Backend (Flask)
- **Autenticación JWT** con roles de usuario
- **CRUD completo** para autores, libros y géneros
- **Relaciones complejas** (libros con múltiples autores)
- **Validaciones de datos** en el servidor
- **Borrado lógico** para mantener integridad referencial
- **Documentación de endpoints** disponible

## Endpoints API Principales

### Autenticación
- **POST /auth/register** - Registrar nuevo usuario
- **POST /auth/login** - Iniciar sesión
- **GET /auth/verify** - Verificar token

### Autores
- **GET /autores** - Listar todos los autores
- **GET /autor/{id}** - Obtener un autor por ID
- **POST /autor** - Crear autor (requiere autenticación)
- **PUT /autor/{id}** - Actualizar autor (requiere autenticación)
- **DELETE /autor/{id}** - Eliminar autor (requiere admin)

### Libros
- **GET /libros** - Listar todos los libros
- **GET /libro/{id}** - Obtener libro por ID
- **POST /libro** - Crear libro (requiere autenticación)
- **PUT /libro/{id}** - Actualizar libro (requiere autenticación)
- **DELETE /libro/{id}** - Eliminar libro (requiere admin)

### Géneros
- **GET /generos** - Listar todos los géneros
- **POST /genero** - Crear género (requiere admin)
- **PUT /genero/{id}** - Actualizar género (requiere admin)
- **DELETE /genero/{id}** - Eliminar género (requiere admin)
