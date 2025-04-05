from backend.models.mysql_connection_pool import MySQLPool

class LibroModel:
    def __init__(self):        
        self.mysql_pool = MySQLPool()

    def obtener_libro(self, libro_id):    
        params = {'libro_id': libro_id}      
        rv = self.mysql_pool.execute("""
            SELECT l.libro_id, l.libro_titulo, l.anio_publicacion, l.genero, a.autor_nombre 
            FROM libros l
            INNER JOIN autores a ON l.autor_id = a.autor_id
            WHERE l.libro_id = %(libro_id)s
        """, params)                
        data = []
        for result in rv:
            content = {
                'libro_id': result[0], 
                'libro_titulo': result[1], 
                'anio_publicacion': result[2], 
                'genero': result[3],
                'autor_nombre': result[4]
            }
            data.append(content)
        return data

    def obtener_libros(self):  
        rv = self.mysql_pool.execute("""
            SELECT l.libro_id, l.libro_titulo, l.anio_publicacion, l.genero, a.autor_nombre 
            FROM libros l
            INNER JOIN autores a ON l.autor_id = a.autor_id
        """)  
        data = []
        for result in rv:
            content = {
                'libro_id': result[0], 
                'libro_titulo': result[1], 
                'anio_publicacion': result[2], 
                'genero': result[3],
                'autor_nombre': result[4]
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
        query = """INSERT INTO libros (libro_titulo, anio_publicacion, genero, autor_id) 
            VALUES (%(libro_titulo)s, %(anio_publicacion)s, %(genero)s, %(autor_id)s)"""    
        cursor = self.mysql_pool.execute(query, data, commit=True)   
        data['libro_id'] = cursor.lastrowid
        return data

    def actualizar_libro(self, libro_id, libro_titulo, anio_publicacion, genero, autor_id):    
        data = {
            'libro_id': libro_id,
            'libro_titulo': libro_titulo,
            'anio_publicacion': anio_publicacion,
            'genero': genero,
            'autor_id': autor_id
        }  
        query = """UPDATE libros SET 
                    libro_titulo = %(libro_titulo)s, 
                    anio_publicacion = %(anio_publicacion)s,
                    genero = %(genero)s,
                    autor_id = %(autor_id)s 
                WHERE libro_id = %(libro_id)s"""    
        self.mysql_pool.execute(query, data, commit=True)   
        return {'resultado': 1} 

    def eliminar_libro(self, libro_id):    
        params = {'libro_id': libro_id}      
        query = """DELETE FROM libros WHERE libro_id = %(libro_id)s"""    
        self.mysql_pool.execute(query, params, commit=True)   
        return {'resultado': 1}

    def obtener_libros_por_autor(self, autor_id):    
        params = {'autor_id': autor_id}      
        rv = self.mysql_pool.execute("""
            SELECT l.libro_id, l.libro_titulo, l.anio_publicacion, l.genero, a.autor_nombre 
            FROM libros l
            INNER JOIN autores a ON l.autor_id = a.autor_id
            WHERE l.autor_id = %(autor_id)s
        """, params)                
        data = []
        for result in rv:
            content = {
                'libro_id': result[0], 
                'libro_titulo': result[1], 
                'anio_publicacion': result[2], 
                'genero': result[3],
                'autor_nombre': result[4]
            }
            data.append(content)
        return data