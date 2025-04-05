from backend.models.sqlite_connection import SQLiteConnection

class AutorModel:
    def __init__(self):        
        self.db = SQLiteConnection()

    def obtener_autor(self, autor_id):    
        query = "SELECT * FROM autores WHERE autor_id = ?"
        resultados = self.db.execute_query(query, (autor_id,))
        data = []
        for result in resultados:
            content = {
                'autor_id': result['autor_id'], 
                'autor_nombre': result['autor_nombre'], 
                'autor_pais': result['autor_pais'], 
                'anio_nacimiento': result['anio_nacimiento']
            }
            data.append(content)
        return data

    def obtener_autores(self):  
        query = "SELECT * FROM autores"
        resultados = self.db.execute_query(query)
        data = []
        for result in resultados:
            content = {
                'autor_id': result['autor_id'], 
                'autor_nombre': result['autor_nombre'], 
                'autor_pais': result['autor_pais'], 
                'anio_nacimiento': result['anio_nacimiento']
            }
            data.append(content)
        return data

    def crear_autor(self, autor_nombre, autor_pais, anio_nacimiento):    
        data = {
            'autor_nombre': autor_nombre,
            'autor_pais': autor_pais,
            'anio_nacimiento': anio_nacimiento
        }  
        query = "INSERT INTO autores (autor_nombre, autor_pais, anio_nacimiento) VALUES (?, ?, ?)"    
        autor_id = self.db.execute_query(query, (autor_nombre, autor_pais, anio_nacimiento), True)   

        data['autor_id'] = autor_id
        return data

    def actualizar_autor(self, autor_id, autor_nombre, autor_pais, anio_nacimiento):    
        query = "UPDATE autores SET autor_nombre = ?, autor_pais = ?, anio_nacimiento = ? WHERE autor_id = ?"
        self.db.execute_query(query, (autor_nombre, autor_pais, anio_nacimiento, autor_id), True)   
        return {'resultado': 1} 

    def eliminar_autor(self, autor_id):    
        query = "DELETE FROM autores WHERE autor_id = ?"
        self.db.execute_query(query, (autor_id,), True)   
        return {'resultado': 1}