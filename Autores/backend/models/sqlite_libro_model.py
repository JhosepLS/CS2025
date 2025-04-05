from backend.models.sqlite_connection import SQLiteConnection

class LibroModel:
    def __init__(self):        
        self.db = SQLiteConnection()

    def obtener_libro(self, libro_id):    
        query = """
            SELECT l.libro_id, l.libro_titulo, l.anio_publicacion, l.genero, 
                   a.autor_nombre, a.autor_id 
            FROM libros l
            JOIN autores a ON l.autor_id = a.autor_id
            WHERE l.libro_id = ?
        """
        resultados = self.db.execute_query(query, (libro_id,))
        data = []
        for result in resultados:
            content = {
                'libro_id': result['libro_id'], 
                'libro_titulo': result['libro_titulo'], 
                'anio_publicacion': result['anio_publicacion'], 
                'genero': result['genero'],
                'autor_nombre': result['autor_nombre'],
                'autor_id': result['autor_id']
            }
            data.append(content)
        return data

    def obtener_libros(self):  
        query = """
            SELECT l.libro_id, l.libro_titulo, l.anio_publicacion, l.genero, 
                   a.autor_nombre, a.autor_id 
            FROM libros l
            JOIN autores a ON l.autor_id = a.autor_id
        """
        resultados = self.db.execute_query(query)
        data = []
        for result in resultados:
            content = {
                'libro_id': result['libro_id'], 
                'libro_titulo': result['libro_titulo'], 
                'anio_publicacion': result['anio_publicacion'], 
                'genero': result['genero'],
                'autor_nombre': result['autor_nombre'],
                'autor_id': result['autor_id']
            }
            data.append(content)
        return data

    def crear_libro(self, libro_titulo, anio_publicacion, genero, autor_id):    
        data = {
            'libro_titulo': libro_titulo,
            'anio_publicacion': anio_publicacion,
            'genero': genero,
            'autor_id': autor_id
        }  
        query = "INSERT INTO libros (libro_titulo, anio_publicacion, genero, autor_id) VALUES (?, ?, ?, ?)"    
        libro_id = self.db.execute_query(query, (libro_titulo, anio_publicacion, genero, autor_id), True)   
        data['libro_id'] = libro_id
        return data

    def actualizar_libro(self, libro_id, libro_titulo, anio_publicacion, genero, autor_id):    
        query = """
            UPDATE libros 
            SET libro_titulo = ?, anio_publicacion = ?, genero = ?, autor_id = ? 
            WHERE libro_id = ?
        """
        self.db.execute_query(query, (libro_titulo, anio_publicacion, genero, autor_id, libro_id), True)   
        return {'resultado': 1} 

    def eliminar_libro(self, libro_id):    
        query = "DELETE FROM libros WHERE libro_id = ?"
        self.db.execute_query(query, (libro_id,), True)   
        return {'resultado': 1}

    def obtener_libros_por_autor(self, autor_id):    
        query = """
            SELECT l.libro_id, l.libro_titulo, l.anio_publicacion, l.genero, 
                   a.autor_nombre, a.autor_id 
            FROM libros l
            JOIN autores a ON l.autor_id = a.autor_id
            WHERE l.autor_id = ?
        """
        resultados = self.db.execute_query(query, (autor_id,))
        data = []
        for result in resultados:
            content = {
                'libro_id': result['libro_id'], 
                'libro_titulo': result['libro_titulo'], 
                'anio_publicacion': result['anio_publicacion'], 
                'genero': result['genero'],
                'autor_nombre': result['autor_nombre'],
                'autor_id': result['autor_id']
            }
            data.append(content)
        return data