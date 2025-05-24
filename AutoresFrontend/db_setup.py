import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Inicializar bcrypt
bcrypt = Bcrypt()

# Parámetros de conexión desde variables de entorno o valores predeterminados
host = os.getenv('DB_HOST', 'localhost')
user = os.getenv('DB_USER', 'postgres')
password = os.getenv('DB_PASSWORD', 'admin')
port = os.getenv('DB_PORT', '5432')
database = os.getenv('DB_NAME', 'biblioteca_db')

def crear_base_datos():
    """Crea la base de datos si no existe"""
    conn = None
    try:
        # Conectar a PostgreSQL sin especificar base de datos
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Verificar si la base de datos ya existe
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (database,))
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f"CREATE DATABASE {database}")
            print(f"Base de datos '{database}' creada exitosamente.")
        else:
            print(f"La base de datos '{database}' ya existe.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creando la base de datos: {e}")
        if conn:
            conn.close()

def crear_tablas():
    """Crea las tablas necesarias"""
    conn = None
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            database=database
        )
        cursor = conn.cursor()
        
        # Crear tabla de usuarios
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            role VARCHAR(20) NOT NULL DEFAULT 'usuario',
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Crear tabla de autores
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS autores (
            autor_id SERIAL PRIMARY KEY,
            autor_nombre VARCHAR(100) NOT NULL,
            autor_pais VARCHAR(50),
            anio_nacimiento INTEGER,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Crear tabla de géneros
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS generos (
            genero_id SERIAL PRIMARY KEY,
            genero_nombre VARCHAR(50) UNIQUE NOT NULL,
            descripcion TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Crear tabla de libros
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            libro_id SERIAL PRIMARY KEY,
            libro_titulo VARCHAR(200) NOT NULL,
            anio_publicacion INTEGER,
            genero_id INTEGER REFERENCES generos(genero_id),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Crear tabla de relación libro-autor (muchos a muchos)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS libro_autor (
            libro_id INTEGER REFERENCES libros(libro_id) ON DELETE CASCADE,
            autor_id INTEGER REFERENCES autores(autor_id) ON DELETE CASCADE,
            PRIMARY KEY (libro_id, autor_id)
        )
        """)
        
        conn.commit()
        print("Tablas creadas exitosamente.")
        
        # Insertar datos de ejemplo
        insertar_datos_ejemplo(cursor, conn)
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creando las tablas: {e}")
        if conn:
            conn.rollback()
            conn.close()

def insertar_datos_ejemplo(cursor, conn):
    """Inserta datos de ejemplo en las tablas"""
    try:
        # Verificar si ya hay datos en la tabla de usuarios
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Crear usuario administrador usando flask_bcrypt
            hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
            cursor.execute(
                "INSERT INTO usuarios (username, password, email, role) VALUES (%s, %s, %s, %s)",
                ('admin', hashed_password, 'admin@biblioteca.com', 'admin')
            )
            
            # Crear usuario normal
            hashed_password = bcrypt.generate_password_hash('user123').decode('utf-8')
            cursor.execute(
                "INSERT INTO usuarios (username, password, email, role) VALUES (%s, %s, %s, %s)",
                ('usuario', hashed_password, 'usuario@biblioteca.com', 'usuario')
            )
            
            print("Usuarios de ejemplo creados.")
        
        # Verificar si ya hay datos en la tabla de géneros
        cursor.execute("SELECT COUNT(*) FROM generos")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Insertar géneros
            generos = [
                ('Novela', 'Narración en prosa de considerable extensión'),
                ('Poesía', 'Composición literaria que se concibe como expresión artística'),
                ('Ciencia Ficción', 'Género basado en elementos imaginarios'),
                ('Fantasía', 'Género que incluye elementos mágicos y sobrenaturales'),
                ('Historia', 'Obras basadas en hechos reales del pasado')
            ]
            
            for genero in generos:
                cursor.execute(
                    "INSERT INTO generos (genero_nombre, descripcion) VALUES (%s, %s)",
                    genero
                )
            
            print("Géneros de ejemplo creados.")
        
        # Verificar si ya hay datos en la tabla de autores
        cursor.execute("SELECT COUNT(*) FROM autores")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Insertar autores
            autores = [
                ('Gabriel García Márquez', 'Colombia', 1927),
                ('J.K. Rowling', 'Reino Unido', 1965),
                ('Haruki Murakami', 'Japón', 1949),
                ('Isabel Allende', 'Chile', 1942),
                ('Julio Cortázar', 'Argentina', 1914)
            ]
            
            for autor in autores:
                cursor.execute(
                    "INSERT INTO autores (autor_nombre, autor_pais, anio_nacimiento) VALUES (%s, %s, %s)",
                    autor
                )
            
            print("Autores de ejemplo creados.")
        
        # Verificar si ya hay datos en la tabla de libros
        cursor.execute("SELECT COUNT(*) FROM libros")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Obtener IDs de géneros
            cursor.execute("SELECT genero_id FROM generos WHERE genero_nombre = 'Novela'")
            novela_id = cursor.fetchone()[0]
            
            cursor.execute("SELECT genero_id FROM generos WHERE genero_nombre = 'Fantasía'")
            fantasia_id = cursor.fetchone()[0]
            
            # Insertar libros
            libros = [
                ('Cien años de soledad', 1967, novela_id),
                ('Harry Potter y la piedra filosofal', 1997, fantasia_id),
                ('Tokio blues', 1987, novela_id),
                ('La casa de los espíritus', 1982, novela_id),
                ('Rayuela', 1963, novela_id)
            ]
            
            for libro in libros:
                cursor.execute(
                    "INSERT INTO libros (libro_titulo, anio_publicacion, genero_id) VALUES (%s, %s, %s) RETURNING libro_id",
                    libro
                )
                libro_id = cursor.fetchone()[0]
                
                # Asignar autor correspondiente (mismo índice para simplificar)
                cursor.execute("SELECT autor_id FROM autores LIMIT 1 OFFSET %s", (libros.index(libro),))
                autor_id = cursor.fetchone()[0]
                
                cursor.execute(
                    "INSERT INTO libro_autor (libro_id, autor_id) VALUES (%s, %s)",
                    (libro_id, autor_id)
                )
            
            print("Libros de ejemplo creados con sus relaciones.")
        
        conn.commit()
        print("Datos de ejemplo insertados correctamente.")
        
    except Exception as e:
        conn.rollback()
        print(f"Error insertando datos de ejemplo: {e}")

if __name__ == "__main__":
    print("Configurando base de datos PostgreSQL...")
    crear_base_datos()
    crear_tablas()
    print("Configuración completada.")