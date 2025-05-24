from backend.models.postgres_connection import PostgresConnection
import psycopg2.extras

class LibroModel:
    def __init__(self):        
        self.db = PostgresConnection()

    def obtener_libro(self, libro_id):
        """Obtiene un libro por su ID con todos sus autores"""
        try:
            # Obtener información del libro
            query = """
                SELECT l.libro_id, l.libro_titulo, l.anio_publicacion, 
                       g.genero_id, g.genero_nombre,
                       l.created_at, l.updated_at, l.is_active
                FROM libros l
                JOIN generos g ON l.genero_id = g.genero_id
                WHERE l.libro_id = %s AND l.is_active = true
            """
            resultados = self.db.execute_query(query, (libro_id,))
            
            if not resultados:
                return {"error": "Libro no encontrado o ha sido eliminado"}, 404
                
            libro = resultados[0]
            
            # Obtener los autores del libro
            query = """
                SELECT a.autor_id, a.autor_nombre, a.autor_pais, a.anio_nacimiento
                FROM autores a
                JOIN libro_autor la ON a.autor_id = la.autor_id
                WHERE la.libro_id = %s AND a.is_active = true
            """
            autores = self.db.execute_query(query, (libro_id,))
            
            # Combinar información
            return {
                "libro": libro,
                "autores": autores
            }, 200
            
        except Exception as e:
            return {"error": str(e)}, 500

    def obtener_libros(self):
        """Obtiene todos los libros activos con su género"""
        try:
            query = """
                SELECT l.libro_id, l.libro_titulo, l.anio_publicacion,
                       g.genero_id, g.genero_nombre
                FROM libros l
                JOIN generos g ON l.genero_id = g.genero_id
                WHERE l.is_active = true
                ORDER BY l.libro_titulo
            """
            resultados = self.db.execute_query(query)
            
            # Para cada libro, obtener la lista de autores
            libros_con_autores = []
            for libro in resultados:
                query = """
                    SELECT a.autor_id, a.autor_nombre
                    FROM autores a
                    JOIN libro_autor la ON a.autor_id = la.autor_id
                    WHERE la.libro_id = %s AND a.is_active = true
                """
                autores = self.db.execute_query(query, (libro['libro_id'],))
                libro_con_autores = dict(libro)
                libro_con_autores['autores'] = autores
                libros_con_autores.append(libro_con_autores)
                
            return libros_con_autores, 200
            
        except Exception as e:
            return {"error": str(e)}, 500

    def crear_libro(self, libro_titulo, anio_publicacion, genero_id, autores_ids):
        """Crea un nuevo libro con múltiples autores y validaciones"""
        try:
            # Validar datos
            if not libro_titulo or not libro_titulo.strip():
                return {"error": "El título del libro es obligatorio"}, 400
                
            if anio_publicacion and (anio_publicacion < 0 or anio_publicacion > 2100):
                return {"error": "El año de publicación debe estar entre 0 y 2100"}, 400
                
            if not genero_id:
                return {"error": "El género es obligatorio"}, 400
                
            if not autores_ids or len(autores_ids) == 0:
                return {"error": "Debe especificar al menos un autor"}, 400
                
            # Verificar si ya existe un libro con el mismo título
            query = "SELECT * FROM libros WHERE libro_titulo = %s AND is_active = true"
            libro_existente = self.db.execute_query(query, (libro_titulo,))
            
            if libro_existente:
                return {"error": "Ya existe un libro con ese título"}, 409
                
            # Verificar si el género existe
            query = "SELECT * FROM generos WHERE genero_id = %s"
            genero = self.db.execute_query(query, (genero_id,))
            
            if not genero:
                return {"error": f"El género con ID {genero_id} no existe"}, 404
                
            # Verificar si todos los autores existen y están activos
            for autor_id in autores_ids:
                query = "SELECT * FROM autores WHERE autor_id = %s AND is_active = true"
                autor = self.db.execute_query(query, (autor_id,))
                
                if not autor:
                    return {"error": f"El autor con ID {autor_id} no existe o ha sido eliminado"}, 404
            
            # Iniciar transacción para insertar libro y relaciones con autores
            conn = self.db.get_connection()
            try:
                cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                
                # Insertar libro
                query = """
                    INSERT INTO libros (libro_titulo, anio_publicacion, genero_id, is_active) 
                    VALUES (%s, %s, %s, true)
                    RETURNING libro_id, libro_titulo, anio_publicacion, genero_id, created_at, updated_at, is_active
                """
                cursor.execute(query, (libro_titulo, anio_publicacion, genero_id))
                nuevo_libro = cursor.fetchone()
                libro_id = nuevo_libro['libro_id']
                
                # Insertar relaciones con autores
                for autor_id in autores_ids:
                    query = "INSERT INTO libro_autor (libro_id, autor_id) VALUES (%s, %s)"
                    cursor.execute(query, (libro_id, autor_id))
                
                # Obtener información completa del género
                query = "SELECT * FROM generos WHERE genero_id = %s"
                cursor.execute(query, (genero_id,))
                genero_info = cursor.fetchone()
                
                # Obtener información de los autores
                query = """
                    SELECT a.autor_id, a.autor_nombre, a.autor_pais, a.anio_nacimiento
                    FROM autores a
                    WHERE a.autor_id IN %s AND a.is_active = true
                """
                cursor.execute(query, (tuple(autores_ids),))
                autores_info = cursor.fetchall()
                
                conn.commit()
                
                # Construir respuesta
                respuesta = dict(nuevo_libro)
                respuesta['genero'] = genero_info
                respuesta['autores'] = autores_info
                
                return respuesta, 201
                
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()
            
        except Exception as e:
            return {"error": str(e)}, 500
            
    def actualizar_libro(self, libro_id, libro_titulo, anio_publicacion, genero_id, autores_ids):
        """Actualiza un libro con múltiples autores y validaciones"""
        try:
            # Verificar si el libro existe y está activo
            query = "SELECT * FROM libros WHERE libro_id = %s AND is_active = true"
            libro = self.db.execute_query(query, (libro_id,))
            
            if not libro:
                return {"error": "Libro no encontrado o ha sido eliminado"}, 404
                
            # Validar datos
            if not libro_titulo or not libro_titulo.strip():
                return {"error": "El título del libro es obligatorio"}, 400
                
            if anio_publicacion and (anio_publicacion < 0 or anio_publicacion > 2100):
                return {"error": "El año de publicación debe estar entre 0 y 2100"}, 400
                
            if not genero_id:
                return {"error": "El género es obligatorio"}, 400
                
            if not autores_ids or len(autores_ids) == 0:
                return {"error": "Debe especificar al menos un autor"}, 400
                
            # Verificar si ya existe otro libro con el mismo título
            query = "SELECT * FROM libros WHERE libro_titulo = %s AND libro_id != %s AND is_active = true"
            libro_existente = self.db.execute_query(query, (libro_titulo, libro_id))
            
            if libro_existente:
                return {"error": "Ya existe otro libro con ese título"}, 409
                
            # Verificar si el género existe
            query = "SELECT * FROM generos WHERE genero_id = %s"
            genero = self.db.execute_query(query, (genero_id,))
            
            if not genero:
                return {"error": f"El género con ID {genero_id} no existe"}, 404
                
            # Verificar si todos los autores existen y están activos
            for autor_id in autores_ids:
                query = "SELECT * FROM autores WHERE autor_id = %s AND is_active = true"
                autor = self.db.execute_query(query, (autor_id,))
                
                if not autor:
                    return {"error": f"El autor con ID {autor_id} no existe o ha sido eliminado"}, 404
            
            # Iniciar transacción para actualizar libro y relaciones con autores
            conn = self.db.get_connection()
            try:
                cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                
                # Actualizar libro
                query = """
                    UPDATE libros 
                    SET libro_titulo = %s, anio_publicacion = %s, genero_id = %s, updated_at = NOW()
                    WHERE libro_id = %s
                    RETURNING libro_id, libro_titulo, anio_publicacion, genero_id, created_at, updated_at, is_active
                """
                cursor.execute(query, (libro_titulo, anio_publicacion, genero_id, libro_id))
                libro_actualizado = cursor.fetchone()
                
                # Eliminar todas las relaciones con autores existentes
                query = "DELETE FROM libro_autor WHERE libro_id = %s"
                cursor.execute(query, (libro_id,))
                
                # Insertar nuevas relaciones con autores
                for autor_id in autores_ids:
                    query = "INSERT INTO libro_autor (libro_id, autor_id) VALUES (%s, %s)"
                    cursor.execute(query, (libro_id, autor_id))
                
                # Obtener información completa del género
                query = "SELECT * FROM generos WHERE genero_id = %s"
                cursor.execute(query, (genero_id,))
                genero_info = cursor.fetchone()
                
                # Obtener información de los autores
                query = """
                    SELECT a.autor_id, a.autor_nombre, a.autor_pais, a.anio_nacimiento
                    FROM autores a
                    WHERE a.autor_id IN %s AND a.is_active = true
                """
                cursor.execute(query, (tuple(autores_ids),))
                autores_info = cursor.fetchall()
                
                conn.commit()
                
                # Construir respuesta
                respuesta = dict(libro_actualizado)
                respuesta['genero'] = genero_info
                respuesta['autores'] = autores_info
                
                return respuesta, 200
                
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()
            
        except Exception as e:
            return {"error": str(e)}, 500

    def eliminar_libro(self, libro_id):
        """Marca un libro como eliminado (borrado lógico)"""
        try:
            # Verificar si el libro existe y está activo
            query = "SELECT * FROM libros WHERE libro_id = %s AND is_active = true"
            libro = self.db.execute_query(query, (libro_id,))
            
            if not libro:
                return {"error": "Libro no encontrado o ya ha sido eliminado"}, 404
                
            # Marcar como eliminado (borrado lógico)
            query = """
                UPDATE libros
                SET is_active = false, updated_at = NOW()
                WHERE libro_id = %s
                RETURNING libro_id
            """
            resultado = self.db.execute_query(query, (libro_id,), True)
            
            return {"mensaje": "Libro marcado como eliminado"}, 200
            
        except Exception as e:
            return {"error": str(e)}, 500

    def obtener_autores_por_libro(self, libro_id):
        """Obtiene todos los autores de un libro específico"""
        try:
            # Verificar si el libro existe y está activo
            query = "SELECT * FROM libros WHERE libro_id = %s AND is_active = true"
            libro = self.db.execute_query(query, (libro_id,))
            
            if not libro:
                return {"error": "Libro no encontrado o ha sido eliminado"}, 404
                
            # Obtener los autores del libro
            query = """
                SELECT a.autor_id, a.autor_nombre, a.autor_pais, a.anio_nacimiento,
                       a.created_at, a.updated_at, a.is_active
                FROM autores a
                JOIN libro_autor la ON a.autor_id = la.autor_id
                WHERE la.libro_id = %s AND a.is_active = true
                ORDER BY a.autor_nombre
            """
            autores = self.db.execute_query(query, (libro_id,))
            
            return {
                "libro": libro[0],
                "autores": autores
            }, 200
            
        except Exception as e:
            return {"error": str(e)}, 500