import sqlite3
import os

# Archivo de base de datos
DB_FILE = 'biblioteca.db'

def crear_base_datos():
    try:
        # Eliminar la base de datos si ya existe
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            print(f"Base de datos existente eliminada para recrearla.")
            
        # Conectar a SQLite (crea el archivo)
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Crear tabla autores
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS autores (
            autor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            autor_nombre TEXT NOT NULL,
            autor_pais TEXT,
            anio_nacimiento INTEGER
        )
        """)
        
        # Crear tabla libros
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            libro_id INTEGER PRIMARY KEY AUTOINCREMENT,
            libro_titulo TEXT NOT NULL,
            anio_publicacion INTEGER,
            genero TEXT,
            autor_id INTEGER,
            FOREIGN KEY (autor_id) REFERENCES autores(autor_id) ON DELETE CASCADE
        )
        """)
        
        # Insertar autores de ejemplo
        autores = [
            ("Gabriel García Márquez", "Colombia", 1927),
            ("J.K. Rowling", "Reino Unido", 1965),
            ("Haruki Murakami", "Japón", 1949)
        ]
        
        cursor.executemany(
            "INSERT INTO autores (autor_nombre, autor_pais, anio_nacimiento) VALUES (?, ?, ?)",
            autores
        )
        
        # Obtener IDs de autores
        cursor.execute("SELECT autor_id FROM autores")
        autor_ids = [row[0] for row in cursor.fetchall()]
        
        # Insertar libros de ejemplo
        libros = [
            ("Cien años de soledad", 1967, "Realismo mágico", autor_ids[0]),
            ("El amor en los tiempos del cólera", 1985, "Novela", autor_ids[0]),
            ("Harry Potter y la piedra filosofal", 1997, "Fantasía", autor_ids[1]),
            ("Tokio blues", 1987, "Novela", autor_ids[2])
        ]
        
        cursor.executemany(
            "INSERT INTO libros (libro_titulo, anio_publicacion, genero, autor_id) VALUES (?, ?, ?, ?)",
            libros
        )
        
        conn.commit()
        print("Base de datos configurada correctamente con datos de ejemplo.")
        
    except sqlite3.Error as err:
        print(f"Error: {err}")
        
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    crear_base_datos()