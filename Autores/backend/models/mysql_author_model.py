from backend.models.mysql_connection_pool import MySQLPool

class AutorModel:
    def __init__(self):        
        self.mysql_pool = MySQLPool()

    def obtener_autor(self, autor_id):    
        params = {'autor_id': autor_id}      
        rv = self.mysql_pool.execute("SELECT * FROM autores WHERE autor_id=%(autor_id)s", params)                
        data = []
        for result in rv:
            content = {
                'autor_id': result[0], 
                'autor_nombre': result[1], 
                'autor_pais': result[2], 
                'anio_nacimiento': result[3]
            }
            data.append(content)
        return data

    def obtener_autores(self):  
        rv = self.mysql_pool.execute("SELECT * FROM autores")  
        data = []
        for result in rv:
            content = {
                'autor_id': result[0], 
                'autor_nombre': result[1], 
                'autor_pais': result[2], 
                'anio_nacimiento': result[3]
            }
            data.append(content)
        return data

    def crear_autor(self, autor_nombre, autor_pais, anio_nacimiento):    
        data = {
            'autor_nombre': autor_nombre,
            'autor_pais': autor_pais,
            'anio_nacimiento': anio_nacimiento
        }  
        query = """INSERT INTO autores (autor_nombre, autor_pais, anio_nacimiento) 
            VALUES (%(autor_nombre)s, %(autor_pais)s, %(anio_nacimiento)s)"""    
        cursor = self.mysql_pool.execute(query, data, commit=True)   

        data['autor_id'] = cursor.lastrowid
        return data

    def actualizar_autor(self, autor_id, autor_nombre, autor_pais, anio_nacimiento):    
        data = {
            'autor_id': autor_id,
            'autor_nombre': autor_nombre,
            'autor_pais': autor_pais,
            'anio_nacimiento': anio_nacimiento
        }  
        query = """UPDATE autores SET autor_nombre = %(autor_nombre)s, autor_pais = %(autor_pais)s,
                    anio_nacimiento = %(anio_nacimiento)s WHERE autor_id = %(autor_id)s"""    
        self.mysql_pool.execute(query, data, commit=True)   
        return {'resultado': 1} 

    def eliminar_autor(self, autor_id):    
        params = {'autor_id': autor_id}      
        query = """DELETE FROM autores WHERE autor_id = %(autor_id)s"""    
        self.mysql_pool.execute(query, params, commit=True)   
        return {'resultado': 1}