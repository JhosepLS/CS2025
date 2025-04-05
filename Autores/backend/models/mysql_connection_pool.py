import mysql.connector.pooling
import configparser
import os

# Crear config.ini si no existe
def crear_config_si_no_existe():
    if not os.path.exists('config.ini'):
        config = configparser.ConfigParser()
        config['mysql'] = {
            'host': 'localhost',
            'port': '3306',
            'user': 'root',
            'pass': '123456',
            'database': 'biblioteca_db'
        }
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

crear_config_si_no_existe()

# Leer configuración
config = configparser.ConfigParser()
config.read('config.ini')

dbconfig = {
    "host": config.get('mysql', 'host'),
    "port": config.get('mysql', 'port'),
    "user": config.get('mysql', 'user'),
    "password": config.get('mysql', 'pass'),
    "database": config.get('mysql', 'database'),
}

class MySQLPool(object):
    """
    Crea un pool de conexiones a MySQL, lo que reduce el tiempo de conexión
    """
    def __init__(self):             
        self.pool = self.create_pool(pool_name='biblioteca_pool', pool_size=3)

    def create_pool(self, pool_name, pool_size):
        """
        Crea un pool de conexiones
        """
        pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name=pool_name,
            pool_size=pool_size,
            pool_reset_session=True,
            **dbconfig)
        return pool

    def close(self, conn, cursor):
        """
        Cierra la conexión
        """
        cursor.close()
        conn.close()

    def execute(self, sql, args=None, commit=False):
        """
        Ejecuta una consulta SQL
        """
        # Obtiene conexión del pool
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        if args:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)
        if commit is True:
            conn.commit()
            self.close(conn, cursor)
            return cursor
        else:
            res = cursor.fetchall()
            self.close(conn, cursor)
            return res