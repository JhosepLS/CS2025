from database import execute_query

# Modelo para Autores
class Autor:
    @staticmethod
    def obtener_todos():
        query = "SELECT * FROM autores"
        return execute_query(query)
    
    @staticmethod
    def obtener_por_id(id):
        query = "SELECT * FROM autores WHERE autor_id = ?"
        resultados = execute_query(query, (id,))
        if resultados and len(resultados) > 0:
            return resultados[0]
        return None
    
    @staticmethod
    def crear(nombre, pais, anio):
        query = "INSERT INTO autores (autor_nombre, autor_pais, anio_nacimiento) VALUES (?, ?, ?)"
        autor_id = execute_query(query, (nombre, pais, anio), True)
        return {
            'id': autor_id,
            'nombre': nombre,
            'pais': pais,
            'anio': anio
        }
    
    @staticmethod
    def actualizar(id, nombre, pais, anio):
        query = "UPDATE autores SET autor_nombre = ?, autor_pais = ?, anio_nacimiento = ? WHERE autor_id = ?"
        execute_query(query, (nombre, pais, anio, id), True)
        return {'resultado': 1}
    
    @staticmethod
    def eliminar(id):
        query = "DELETE FROM autores WHERE autor_id = ?"
        execute_query(query, (id,), True)
        return {'resultado': 1}

# Modelo para Libros
class Libro:
    @staticmethod
    def obtener_todos():
        query = """
            SELECT l.libro_id, l.libro_titulo, l.anio_publicacion, l.genero, 
                   a.autor_nombre, a.autor_id 
            FROM libros l
            JOIN autores a ON l.autor_id = a.autor_id
        """
        return execute_query(query)
    
    @staticmethod
    def obtener_por_id(id):
        query = """
            SELECT l.libro_id, l.libro_titulo, l.anio_publicacion, l.genero, 
                   a.autor_nombre, a.autor_id 
            FROM libros l
            JOIN autores a ON l.autor_id = a.autor_id
            WHERE l.libro_id = ?
        """
        resultados = execute_query(query, (id,))
        if resultados and len(resultados) > 0:
            return resultados[0]
        return None
    
    @staticmethod
    def obtener_por_autor(autor_id):
        query = """
            SELECT l.libro_id, l.libro_titulo, l.anio_publicacion, l.genero, 
                   a.autor_nombre, a.autor_id 
            FROM libros l
            JOIN autores a ON l.autor_id = a.autor_id
            WHERE l.autor_id = ?
        """
        return execute_query(query, (autor_id,))
    
    @staticmethod
    def crear(titulo, anio, genero, autor_id):
        query = "INSERT INTO libros (libro_titulo, anio_publicacion, genero, autor_id) VALUES (?, ?, ?, ?)"
        libro_id = execute_query(query, (titulo, anio, genero, autor_id), True)
        return {
            'id': libro_id,
            'titulo': titulo,
            'anio': anio,
            'genero': genero,
            'autor_id': autor_id
        }
    
    @staticmethod
    def actualizar(id, titulo, anio, genero, autor_id):
        query = """
            UPDATE libros 
            SET libro_titulo = ?, anio_publicacion = ?, genero = ?, autor_id = ? 
            WHERE libro_id = ?
        """
        execute_query(query, (titulo, anio, genero, autor_id, id), True)
        return {'resultado': 1}
    
    @staticmethod
    def eliminar(id):
        query = "DELETE FROM libros WHERE libro_id = ?"
        execute_query(query, (id,), True)
        return {'resultado': 1}