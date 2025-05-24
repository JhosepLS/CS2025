from backend.models.postgres_connection import PostgresConnection

class AutorModel:
    def __init__(self):        
        self.db = PostgresConnection()

    def obtener_autor(self, autor_id):
        """Obtiene un autor por su ID, incluyendo una validación"""
        try:
            # Consultar si el autor existe y está activo
            query = "SELECT * FROM autores WHERE autor_id = %s AND is_active = true"
            resultados = self.db.execute_query(query, (autor_id,))
            
            if not resultados:
                return {"error": "Autor no encontrado o ha sido eliminado"}, 404
                
            return resultados, 200
            
        except Exception as e:
            return {"error": str(e)}, 500

    def obtener_autores(self):
        """Obtiene todos los autores activos"""
        try:
            query = "SELECT * FROM autores WHERE is_active = true ORDER BY autor_nombre"
            resultados = self.db.execute_query(query)
            return resultados, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def crear_autor(self, autor_nombre, autor_pais, anio_nacimiento):
        """Crea un nuevo autor con validaciones"""
        try:
            # Validar datos
            if not autor_nombre or not autor_nombre.strip():
                return {"error": "El nombre del autor es obligatorio"}, 400
                
            if anio_nacimiento and (anio_nacimiento < 0 or anio_nacimiento > 2100):
                return {"error": "El año de nacimiento debe estar entre 0 y 2100"}, 400
                
            # Verificar si ya existe un autor con el mismo nombre
            query = "SELECT * FROM autores WHERE autor_nombre = %s AND is_active = true"
            autor_existente = self.db.execute_query(query, (autor_nombre,))
            
            if autor_existente:
                return {"error": "Ya existe un autor con ese nombre"}, 409
                
            # Insertar nuevo autor
            query = """
                INSERT INTO autores (autor_nombre, autor_pais, anio_nacimiento, is_active) 
                VALUES (%s, %s, %s, true)
                RETURNING autor_id, autor_nombre, autor_pais, anio_nacimiento, is_active
            """
            
            nuevo_autor = self.db.execute_query(
                query, 
                (autor_nombre, autor_pais, anio_nacimiento), 
                True
            )
            
            return nuevo_autor, 201
            
        except Exception as e:
            return {"error": str(e)}, 500

    def actualizar_autor(self, autor_id, autor_nombre, autor_pais, anio_nacimiento):
        """Actualiza un autor con validaciones"""
        try:
            # Verificar si el autor existe y está activo
            query = "SELECT * FROM autores WHERE autor_id = %s AND is_active = true"
            autor = self.db.execute_query(query, (autor_id,))
            
            if not autor:
                return {"error": "Autor no encontrado o ha sido eliminado"}, 404
                
            # Validar datos
            if not autor_nombre or not autor_nombre.strip():
                return {"error": "El nombre del autor es obligatorio"}, 400
                
            if anio_nacimiento and (anio_nacimiento < 0 or anio_nacimiento > 2100):
                return {"error": "El año de nacimiento debe estar entre 0 y 2100"}, 400
                
            # Verificar si ya existe otro autor con el mismo nombre
            query = "SELECT * FROM autores WHERE autor_nombre = %s AND autor_id != %s AND is_active = true"
            autor_existente = self.db.execute_query(query, (autor_nombre, autor_id))
            
            if autor_existente:
                return {"error": "Ya existe otro autor con ese nombre"}, 409
                
            # Actualizar autor
            query = """
                UPDATE autores 
                SET autor_nombre = %s, autor_pais = %s, anio_nacimiento = %s
                WHERE autor_id = %s
                RETURNING autor_id, autor_nombre, autor_pais, anio_nacimiento, is_active
            """
            
            autor_actualizado = self.db.execute_query(
                query, 
                (autor_nombre, autor_pais, anio_nacimiento, autor_id), 
                True
            )
            
            return autor_actualizado, 200
            
        except Exception as e:
            return {"error": str(e)}, 500

    def eliminar_autor(self, autor_id):    
        """Marca un autor como eliminado (borrado lógico)"""
        try:
            # Verificar si el autor existe y está activo
            query = "SELECT * FROM autores WHERE autor_id = %s AND is_active = true"
            autor = self.db.execute_query(query, (autor_id,))
            
            if not autor:
                return {"error": "Autor no encontrado o ya ha sido eliminado"}, 404
                
            # Verificar si tiene libros asociados
            query = """
                SELECT COUNT(*) as count FROM libro_autor 
                WHERE autor_id = %s
            """
            resultado = self.db.execute_query(query, (autor_id,))
            
            if resultado and resultado[0]['count'] > 0:
                # Solo marcar como inactivo, no eliminar físicamente
                query = """
                    UPDATE autores
                    SET is_active = false
                    WHERE autor_id = %s
                    RETURNING autor_id
                """
                resultado = self.db.execute_query(query, (autor_id,), True)
                return {"mensaje": "Autor marcado como eliminado"}, 200
            else:
                # Si no tiene libros, podemos eliminarlo completamente
                query = "DELETE FROM autores WHERE autor_id = %s RETURNING autor_id"
                resultado = self.db.execute_query(query, (autor_id,), True)
                return {"mensaje": "Autor eliminado completamente"}, 200
            
        except Exception as e:
            return {"error": str(e)}, 500

    def obtener_libros_por_autor(self, autor_id):
        """Obtiene todos los libros de un autor específico"""
        try:
            # Verificar si el autor existe y está activo
            query = "SELECT * FROM autores WHERE autor_id = %s AND is_active = true"
            autor = self.db.execute_query(query, (autor_id,))
            
            if not autor:
                return {"error": "Autor no encontrado o ha sido eliminado"}, 404
                
            # Obtener los libros del autor
            query = """
                SELECT l.libro_id, l.libro_titulo, l.anio_publicacion, g.genero_nombre,
                       l.created_at, l.updated_at, l.is_active
                FROM libros l
                JOIN libro_autor la ON l.libro_id = la.libro_id
                JOIN generos g ON l.genero_id = g.genero_id
                WHERE la.autor_id = %s AND l.is_active = true
                ORDER BY l.anio_publicacion DESC
            """
            
            libros = self.db.execute_query(query, (autor_id,))
            
            return {
                "autor": autor[0],
                "libros": libros
            }, 200
            
        except Exception as e:
            return {"error": str(e)}, 500