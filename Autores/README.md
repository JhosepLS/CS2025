# API Biblioteca - Autores y Libros

API para gestionar autores y libros usando Flask y SQLite.

## Instalación en Windows

1. **Instalar Python**:
   - Descargar e instalar Python 3.8 o superior desde [python.org](https://www.python.org/downloads/)
   - Asegurarse de marcar la opción "Add Python to PATH" durante la instalación

2. **Clonar o descargar el repositorio**:
   ```
   git clone https://github.com/JhosepLS/CS2025.git
   cd CS2025\Autores
   ```

3. **Instalar dependencias**:
   ```
   pip install flask flask-cors
   ```

4. **Configurar base de datos**:
   ```
   python db_setup.py
   ```
   Esto creará un archivo `biblioteca.db` con las tablas y datos de ejemplo.

5. **Iniciar la aplicación**:
   ```
   python app.py
   ```
   La aplicación estará disponible en `http://localhost:5000`

## Pruebas con Postman

1. **Descargar e instalar** [Postman](https://www.postman.com/downloads/)

2. **Crear una nueva colección** llamada "API Biblioteca"

### Pruebas con Autores

1. **Obtener todos los autores**:
   - Método: GET
   - URL: `http://localhost:5000/autores`
   - Resultado esperado: Lista de todos los autores en formato JSON

2. **Obtener un autor específico**:
   - Método: GET
   - URL: `http://localhost:5000/autor/1`
   - Resultado esperado: Detalles del autor con ID 1

3. **Crear un nuevo autor**:
   - Método: POST
   - URL: `http://localhost:5000/autor`
   - Body:
   ```json
   {
       "nombre": "Isabel Allende",
       "pais": "Chile",
       "anio": 1942
   }
   ```
   - Resultado esperado: Detalles del autor creado con su ID

4. **Actualizar un autor**:
   - Método: PUT
   - URL: `http://localhost:5000/autor/1`
   - Body:
   ```json
   {
       "nombre": "Gabriel García Márquez",
       "pais": "Colombia",
       "anio": 1928
   }
   ```
   - Resultado esperado: `{"resultado": 1}`

5. **Eliminar un autor**:
   - Método: DELETE
   - URL: `http://localhost:5000/autor/4`
   - Resultado esperado: `{"resultado": 1}`

### Pruebas con Libros

1. **Obtener todos los libros**:
   - Método: GET
   - URL: `http://localhost:5000/libros`
   - Resultado esperado: Lista de todos los libros en formato JSON

2. **Obtener un libro específico**:
   - Método: GET
   - URL: `http://localhost:5000/libro/1`
   - Resultado esperado: Detalles del libro con ID 1

3. **Obtener libros de un autor**:
   - Método: GET
   - URL: `http://localhost:5000/libros/autor/1`
   - Resultado esperado: Lista de libros del autor con ID 1

4. **Crear un nuevo libro**:
   - Método: POST
   - URL: `http://localhost:5000/libro`
   - Body:
   ```json
   {
       "titulo": "Crónica de una muerte anunciada",
       "anio": 1981,
       "genero": "Novela",
       "autor_id": 1
   }
   ```
   - Resultado esperado: Detalles del libro creado con su ID

5. **Actualizar un libro**:
   - Método: PUT
   - URL: `http://localhost:5000/libro/1`
   - Body:
   ```json
   {
       "titulo": "Cien años de soledad (Edición Especial)",
       "anio": 1967,
       "genero": "Realismo mágico",
       "autor_id": 1
   }
   ```
   - Resultado esperado: `{"resultado": 1}`

6. **Eliminar un libro**:
   - Método: DELETE
   - URL: `http://localhost:5000/libro/5`
   - Resultado esperado: `{"resultado": 1}`
