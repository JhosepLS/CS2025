import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class PostgresConnection:
    @staticmethod
    def get_connection():
        """Obtiene una conexión a la base de datos PostgreSQL"""
        try:
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'biblioteca_db'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', 'admin'),
                port=os.getenv('DB_PORT', '5432')
            )
            return conn
        except Exception as e:
            print(f"Error de conexión: {e}")
            raise

    @staticmethod
    def execute_query(query, params=None, commit=False):
        """Ejecuta una consulta SQL y devuelve los resultados"""
        conn = None
        try:
            conn = PostgresConnection.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            if commit:
                conn.commit()
                if cursor.rowcount > 0 and cursor.description is not None:
                    result = cursor.fetchone()
                    return result
                elif hasattr(cursor, 'lastrowid'):
                    return cursor.lastrowid
                else:
                    return {"status": "success", "rows_affected": cursor.rowcount}
            else:
                if cursor.description is not None:
                    result = cursor.fetchall()
                    return result
                return []
                
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error en consulta: {e}")
            raise
        finally:
            if conn:
                cursor.close()
                conn.close()