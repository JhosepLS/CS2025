from backend.models.postgres_connection import PostgresConnection

class GeneroModel:
    def __init__(self):        
        self.db = PostgresConnection()

    def obtener_genero(self, genero_id):
        """Obtiene un género por su ID"""
        try:
            query = "SELECT * FROM generos WHERE genero_id = %s"
            resultados = self.db.execute_query(query, (genero_id,))
            
            if not resultados:
                return {"error": "Género no encontrado"}, 404
                
            return resultados[0], 200
            
        except Exception as e:
            return {"error": str(e)}, 500

    def obtener_generos(self):
        """Obtiene todos los géneros"""
        try:
            query = "SELECT * FROM generos ORDER BY genero_nombre"
            resultados = self.db.execute_query(query)
            return resultados, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def crear_genero(self, genero_nombre, descripcion=None):
        """Crea un nuevo género con validaciones"""
        try:
            # Validar datos
            if not genero_nombre or not genero_nombre.strip():
                return {"error": "El nombre del género es obligatorio"}, 400
                
            # Verificar si ya existe un género con el mismo nombre
            query = "SELECT * FROM generos WHERE genero_nombre = %s"
            genero_existente = self.db.execute_query(query, (genero_nombre,))
            
            if genero_existente:
                return {"error": "Ya existe un género con ese nombre"}, 409
                
            # Insertar nuevo género
            query = """
                INSERT INTO generos (genero_nombre, descripcion) 
                VALUES (%s, %s)
                RETURNING *
            """
            
            nuevo_genero = self.db.execute_query(query, (genero_nombre, descripcion), True)
            
            return nuevo_genero, 201
            
        except Exception as e:
            return {"error": str(e)}, 500

    def actualizar_genero(self, genero_id, genero_nombre, descripcion=None):
        """Actualiza un género con validaciones"""
        try:
            # Verificar si el género existe
            query = "SELECT * FROM generos WHERE genero_id = %s"
            genero = self.db.execute_query(query, (genero_id,))
            
            if not genero:
                return {"error": "Género no encontrado"}, 404
                
            # Validar datos
            if not genero_nombre or not genero_nombre.strip():
                return {"error": "El nombre del género es obligatorio"}, 400
                
            # Verificar si ya existe otro género con el mismo nombre
            query = "SELECT * FROM generos WHERE genero_nombre = %s AND genero_id != %s"
            genero_existente = self.db.execute_query(query, (genero_nombre, genero_id))
            
            if genero_existente:
                return {"error": "Ya existe otro género con ese nombre"}, 409
                
            # Actualizar género
            query = """
                UPDATE generos 
                SET genero_nombre = %s, descripcion = %s
                WHERE genero_id = %s
                RETURNING *
            """
            
            genero_actualizado = self.db.execute_query(query, (genero_nombre, descripcion, genero_id), True)
            
            return genero_actualizado, 200
            
        except Exception as e:
            return {"error": str(e)}, 500

    def eliminar_genero(self, genero_id):
        """Elimina un género si no tiene libros asociados"""
        try:
            # Verificar si el género existe
            query = "SELECT * FROM generos WHERE genero_id = %s"
            genero = self.db.execute_query(query, (genero_id,))
            
            if not genero:
                return {"error": "Género no encontrado"}, 404
                
            # Verificar si tiene libros asociados
            query = "SELECT COUNT(*) as count FROM libros WHERE genero_id = %s"
            resultado = self.db.execute_query(query, (genero_id,))
            
            if resultado[0]['count'] > 0:
                return {"error": "No se puede eliminar el género porque tiene libros asociados"}, 400
                
            # Eliminar género
            query = "DELETE FROM generos WHERE genero_id = %s RETURNING genero_id"
            resultado = self.db.execute_query(query, (genero_id,), True)
            
            return {"mensaje": "Género eliminado correctamente"}, 200
            
        except Exception as e:
            return {"error": str(e)}, 500