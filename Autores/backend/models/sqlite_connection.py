import sqlite3

# Archivo de base de datos
DB_FILE = 'biblioteca.db'

class SQLiteConnection:
    @staticmethod
    def get_connection():
        """Obtiene una conexión a la base de datos SQLite"""
        try:
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            return conn
        except Exception as e:
            print(f"Error de conexión: {e}")
            return None

    @staticmethod
    def execute_query(query, params=None, commit=False):
        """Ejecuta una consulta SQL y devuelve los resultados"""
        conn = SQLiteConnection.get_connection()
        cursor = conn.cursor()
        result = None
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            if commit:
                conn.commit()
                return cursor.lastrowid
            else:
                result = [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error en consulta: {e}")
        finally:
            cursor.close()
            conn.close()
            
        return result