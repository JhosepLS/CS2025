# API Biblioteca con Express y MongoDB

API RESTful para gestionar Autores y Libros usando Mongoose, Express.js y MongoDB.

## Requisitos previos

1. **Node.js 14 o superior**
2. **MongoDB 4.4 o superior**
3. **Postman** para probar la API

## Instalación desde cero

### 1. Clonar el repositorio

```bash
git clone https://github.com/JhosepLS/CS2025.git
cd CS2025/AutoresMongo
```

### 2. Instalar dependencias

```bash
npm install
```

### 3. Configurar variables de entorno

Crea un archivo `.env` con el siguiente contenido:

```
MONGODB_URI=mongodb://localhost:27017/biblioteca_db
JWT_SECRET_KEY=altosecreto
PORT=5000
```

### 4. Configurar la base de datos

Asegúrate de que MongoDB esté en ejecución y luego ejecuta:

```bash
node db_setup.js
```

Este script creará las colecciones necesarias e insertará datos de ejemplo de géneros, autores y libros.

### 5. Crear usuario administrador

```bash
node admin_creator.js
```

Este script creará un usuario administrador con las siguientes credenciales:
- Username: admin
- Password: admin123

### 6. Iniciar la aplicación

```bash
npm start
```

La API estará disponible en `http://localhost:5000`

## Guía completa de pruebas con Postman

### 1. Autenticación

#### Iniciar sesión como administrador

- **Método**: POST
- **URL**: `http://localhost:5000/auth/login`
- **Body**:
```json
{
    "username": "admin",
    "password": "admin123"
}
```
- **Resultado esperado**: Status 200 con token JWT
- **IMPORTANTE**: Guarda el token recibido para usarlo en las siguientes pruebas

#### Iniciar sesión con credenciales incorrectas (Prueba de error)

- **Método**: POST
- **URL**: `http://localhost:5000/auth/login`
- **Body**:
```json
{
    "username": "admin",
    "password": "contraseña_incorrecta"
}
```
- **Resultado esperado**: Status 401 con mensaje "Contraseña incorrecta"

#### Registrar nuevo usuario

- **Método**: POST
- **URL**: `http://localhost:5000/auth/register`
- **Body**:
```json
{
    "username": "yeyo",
    "password": "contraseña123",
    "email": "usuario@ejemplo.com"
}
```
- **Resultado esperado**: Status 201 con datos del usuario creado (sin contraseña)

#### Verificar token

- **Método**: GET
- **URL**: `http://localhost:5000/auth/verify`
- **Headers**: Authorization: Bearer {tu_token}
- **Resultado esperado**: Status 200 confirmando que el token es válido

#### Intentar acceder sin token (Prueba de error)

- **Método**: GET
- **URL**: `http://localhost:5000/auth/verify`
- **Resultado esperado**: Status 401 con mensaje "Token requerido"

### 2. Géneros

#### Obtener todos los géneros

- **Método**: GET
- **URL**: `http://localhost:5000/generos`
- **Resultado esperado**: Status 200 con lista de géneros

#### Obtener un género específico

- **Método**: GET
- **URL**: `http://localhost:5000/genero/{id}` (usa un ID de la lista anterior)
- **Resultado esperado**: Status 200 con detalles del género

#### Crear un nuevo género (requiere token de admin)

- **Método**: POST
- **URL**: `http://localhost:5000/genero`
- **Headers**: Authorization: Bearer {token_de_admin}
- **Body**:
```json
{
    "nombre": "Sátira",
    "descripcion": "Crítica humorística de las costumbres y vicios"
}
```
- **Resultado esperado**: Status 201 con datos del género creado

#### Crear género con nombre duplicado (Prueba de error)

- **Método**: POST
- **URL**: `http://localhost:5000/genero`
- **Headers**: Authorization: Bearer {token_de_admin}
- **Body**:
```json
{
    "nombre": "Sátira",
    "descripcion": "Otra descripción"
}
```
- **Resultado esperado**: Status 409 indicando que ya existe un género con ese nombre

#### Actualizar un género

- **Método**: PUT
- **URL**: `http://localhost:5000/genero/{id}` (usa el ID del género creado)
- **Headers**: Authorization: Bearer {token_de_admin}
- **Body**:
```json
{
    "nombre": "Sátira Moderna",
    "descripcion": "Crítica humorística contemporánea"
}
```
- **Resultado esperado**: Status 200 con datos actualizados

#### Eliminar un género (solo si no tiene libros asociados)

- **Método**: DELETE
- **URL**: `http://localhost:5000/genero/{id}` (usa el ID del género creado)
- **Headers**: Authorization: Bearer {token_de_admin}
- **Resultado esperado**: Status 200 con mensaje de éxito

### 3. Autores

#### Obtener todos los autores

- **Método**: GET
- **URL**: `http://localhost:5000/autores`
- **Resultado esperado**: Status 200 con lista de autores

#### Obtener un autor específico

- **Método**: GET
- **URL**: `http://localhost:5000/autor/{id}` (usa un ID de la lista anterior)
- **Resultado esperado**: Status 200 con detalles del autor

#### Crear un nuevo autor

- **Método**: POST
- **URL**: `http://localhost:5000/autor`
- **Headers**: Authorization: Bearer {tu_token}
- **Body**:
```json
{
    "nombre": "Jorge Luis Borges",
    "pais": "Argentina",
    "anio": 1899
}
```
- **Resultado esperado**: Status 201 con datos del autor creado
- **IMPORTANTE**: Guarda el ID del autor para usarlo en otras pruebas

#### Crear autor sin nombre (Prueba de error)

- **Método**: POST
- **URL**: `http://localhost:5000/autor`
- **Headers**: Authorization: Bearer {tu_token}
- **Body**:
```json
{
    "nombre": "",
    "pais": "España",
    "anio": 1950
}
```
- **Resultado esperado**: Status 400 con mensaje "El nombre del autor es obligatorio"

#### Crear autor con año fuera de rango (Prueba de error)

- **Método**: POST
- **URL**: `http://localhost:5000/autor`
- **Headers**: Authorization: Bearer {tu_token}
- **Body**:
```json
{
    "nombre": "Autor Inválido",
    "pais": "España",
    "anio": 3000
}
```
- **Resultado esperado**: Status 400 con mensaje sobre el rango de años

#### Actualizar un autor

- **Método**: PUT
- **URL**: `http://localhost:5000/autor/{id}` (usa el ID del autor creado)
- **Headers**: Authorization: Bearer {tu_token}
- **Body**:
```json
{
    "nombre": "Jorge Luis Borges",
    "pais": "Argentina",
    "anio": 1900
}
```
- **Resultado esperado**: Status 200 con datos actualizados

### 4. Libros

#### Obtener todos los libros

- **Método**: GET
- **URL**: `http://localhost:5000/libros`
- **Resultado esperado**: Status 200 con lista de libros, incluyendo géneros y autores

#### Obtener un libro específico

- **Método**: GET
- **URL**: `http://localhost:5000/libro/{id}` (usa un ID de la lista anterior)
- **Resultado esperado**: Status 200 con detalles del libro

#### Crear un nuevo libro

- **Método**: POST
- **URL**: `http://localhost:5000/libro`
- **Headers**: Authorization: Bearer {tu_token}
- **Body**:
```json
{
    "titulo": "Ficciones",
    "anio": 1944,
    "genero_id": "{id_del_genero}",
    "autores_ids": ["{id_del_autor}"]
}
```
- **Resultado esperado**: Status 201 con datos del libro creado
- **IMPORTANTE**: Guarda el ID del libro para usarlo en otras pruebas

#### Crear libro sin título (Prueba de error)

- **Método**: POST
- **URL**: `http://localhost:5000/libro`
- **Headers**: Authorization: Bearer {tu_token}
- **Body**:
```json
{
    "titulo": "",
    "anio": 2000,
    "genero_id": "{id_del_genero}",
    "autores_ids": ["{id_del_autor}"]
}
```
- **Resultado esperado**: Status 400 con mensaje "El título del libro es obligatorio"

#### Crear libro con autor inexistente (Prueba de error)

- **Método**: POST
- **URL**: `http://localhost:5000/libro`
- **Headers**: Authorization: Bearer {tu_token}
- **Body**:
```json
{
    "titulo": "Libro con autor inexistente",
    "anio": 2000,
    "genero_id": "{id_del_genero}",
    "autores_ids": ["637a8f1a1c9d440000000001"]
}
```
- **Resultado esperado**: Status 404 con mensaje sobre autor inexistente

#### Obtener los autores de un libro

- **Método**: GET
- **URL**: `http://localhost:5000/libro/{id_del_libro}/autores`
- **Resultado esperado**: Status 200 con lista de autores del libro

#### Obtener los libros de un autor

- **Método**: GET
- **URL**: `http://localhost:5000/autor/{id_del_autor}/libros`
- **Resultado esperado**: Status 200 con lista de libros del autor

#### Actualizar un libro (añadir co-autor)

- **Método**: PUT
- **URL**: `http://localhost:5000/libro/{id_del_libro}`
- **Headers**: Authorization: Bearer {tu_token}
- **Body**:
```json
{
    "titulo": "Ficciones",
    "anio": 1944,
    "genero_id": "{id_del_genero}",
    "autores_ids": ["{id_del_autor", "{id_de_otro_autor}"]
}
```
- **Resultado esperado**: Status 200 con datos actualizados mostrando ambos autores

### 5. Pruebas de eliminación lógica

#### Eliminar un autor (borrado lógico)

- **Método**: DELETE
- **URL**: `http://localhost:5000/autor/{id_del_autor}` (usa un ID de autor que tenga libros)
- **Headers**: Authorization: Bearer {token_de_admin}
- **Resultado esperado**: Status 200 con mensaje "Autor marcado como eliminado"

#### Verificar que el autor no aparece en la lista

- **Método**: GET
- **URL**: `http://localhost:5000/autores`
- **Resultado esperado**: El autor eliminado ya no aparece en la lista

#### Intentar obtener el autor eliminado

- **Método**: GET
- **URL**: `http://localhost:5000/autor/{id_del_autor_eliminado}`
- **Resultado esperado**: Status 404 con mensaje "Autor no encontrado o ha sido eliminado"

#### Eliminar un libro (borrado lógico)

- **Método**: DELETE
- **URL**: `http://localhost:5000/libro/{id_del_libro}`
- **Headers**: Authorization: Bearer {token_de_admin}
- **Resultado esperado**: Status 200 con mensaje "Libro marcado como eliminado"

### 6. Pruebas de autorización

#### Iniciar sesión como usuario normal

- **Método**: POST
- **URL**: `http://localhost:5000/auth/login`
- **Body**:
```json
{
    "username": "usuario_nuevo",
    "password": "contraseña123"
}
```
- **Resultado esperado**: Status 200 con token JWT
- **IMPORTANTE**: Guarda este token como "token_usuario_normal"

#### Intentar crear un género con usuario normal (Prueba de error)

- **Método**: POST
- **URL**: `http://localhost:5000/genero`
- **Headers**: Authorization: Bearer {token_usuario_normal}
- **Body**:
```json
{
    "nombre": "Ciencia",
    "descripcion": "Textos científicos"
}
```
- **Resultado esperado**: Status 403 con mensaje sobre privilegios de administrador

#### Intentar eliminar un género con usuario normal (Prueba de error)

- **Método**: DELETE
- **URL**: `http://localhost:5000/genero/{id_del_genero}`
- **Headers**: Authorization: Bearer {token_usuario_normal}
- **Resultado esperado**: Status 403 con mensaje sobre privilegios de administrador

## Algunas pruebas adiciones que se podría realizar

1. Crear y actualizar géneros con tokens inválidos
2. Buscar libros o autores con IDs inexistentes
3. Intentar crear libros con géneros inexistentes

## Notas importantes

- Todos los endpoints protegidos requieren el header `Authorization: Bearer {tu_token}`
- Los endpoints para eliminar géneros, autores y libros requieren permisos de administrador
- El borrado de autores es lógico si tienen libros asociados, o físico si no los tienen
- El borrado de libros siempre es lógico