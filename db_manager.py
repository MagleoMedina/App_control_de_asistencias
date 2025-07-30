# App_control_de_asistencias/db_manager.py

import libsql
import os
import sys
from dotenv import load_dotenv

class DBManager:
    """
    Clase para gestionar la conexión y las operaciones con la base de datos Turso (SQLite).
    """

    def __init__(self):
        """
        Inicializa el gestor de la base de datos, cargando las credenciales
        y preparando la conexión.
        """
        # Carga las variables de entorno desde el archivo .env
        load_dotenv()

        # Variables de conexión, obtenidas de las variables de entorno
        self.url = os.getenv("TURSO_DATABASE_URL")
        self.auth_token = os.getenv("TURSO_AUTH_TOKEN")

        # Verifica que las credenciales estén disponibles
        if not self.url or not self.auth_token:
            print("Error: Las variables de entorno 'TURSO_DATABASE_URL' o 'TURSO_AUTH_TOKEN' no están configuradas.")
            sys.exit(1) # Termina la aplicación si las credenciales no están disponibles

        # Variable para almacenar la conexión a la base de datos (inicialmente None)
        self._connection = None
        print("DBManager inicializado. Credenciales cargadas.")

    def get_db_connection(self):
        """
        Establece y devuelve una conexión a la base de datos Turso.
        Reutiliza la conexión si ya está abierta.
        """
        if self._connection is None:
            try:
                # Conecta a la réplica local ("salu.db" en este caso) y la sincroniza con Turso
                self._connection = libsql.connect("salu.db", sync_url=self.url, auth_token=self.auth_token)
                self._connection.sync()
                print("Conexión a la base de datos Turso establecida y sincronizada.")
            except Exception as e:
                print(f"Error al conectar con Turso: {e}")
                self._connection = None # Asegura que la conexión sea None si falla
        return self._connection

    def close_db_connection(self):
        """
        Cierra la conexión a la base de datos si está abierta.
        Debe llamarse al finalizar la aplicación.
        """
        if self._connection is not None:
            self._connection.close()
            self._connection = None
            print("Conexión a la base de datos cerrada.")

    def execute_query(self, query, params=None, fetch_one=False, commit=False):
        """
        Ejecuta una consulta SQL en la base de datos.
        :param query: La cadena de consulta SQL a ejecutar.
        :param params: Una tupla o lista de parámetros para la consulta (opcional).
        :param fetch_one: Si es True, retorna solo la primera fila del resultado.
        :param commit: Si es True, realiza un commit y sincroniza los cambios.
        :return: El resultado de la consulta (fila/s o True/False para commit), o None en caso de error.
        """
        conn = self.get_db_connection()
        if conn is None:
            print("No hay conexión a la base de datos disponible.")
            return None

        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if commit:
                conn.commit()
                conn.sync() # Sincroniza después de un commit para enviar los cambios a Turso
                return True
            else:
                if fetch_one:
                    return cursor.fetchone()
                else:
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error al ejecutar la consulta '{query}': {e}")
            if conn:
                conn.rollback() # Revierte la transacción en caso de error
            return None
        finally:
            # El cursor se gestiona automáticamente por libsql, no es necesario cerrarlo explícitamente aquí.
            pass

    def init_database(self):
        """
        Inicializa la base de datos, creando las tablas necesarias si no existen.
        """
        # Define las consultas SQL para crear tus tablas
        # Cada sentencia CREATE TABLE es un elemento separado en el array
        create_tables_sql = [
            """
            CREATE TABLE IF NOT EXISTS "Tipo" (
                "ID"	INTEGER,
                "Descripcion"	TEXT,
                PRIMARY KEY("ID" AUTOINCREMENT)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Usuario" (
                "Numero_de_ficha"	INTEGER,
                "Username"	TEXT NOT NULL UNIQUE,
                "Password"	TEXT NOT NULL,
                PRIMARY KEY("Numero_de_ficha" AUTOINCREMENT)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Persona" (
                "ID"	INTEGER,
                "Nombre"	TEXT NOT NULL,
                "Apellido"	TEXT NOT NULL,
                "Cedula"	TEXT NOT NULL,
                "Nro_telefono"	TEXT NOT NULL,
                PRIMARY KEY("ID" AUTOINCREMENT)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Usuario_laboratorio" (
                "Persona"	INTEGER,
                "Nombre_organizacion"	TEXT NOT NULL,
                PRIMARY KEY("Persona"),
                FOREIGN KEY("Persona") REFERENCES "Persona"("ID")
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Administrador" (
                "Persona"	INTEGER,
                "Tipo"	INTEGER NOT NULL,
                "Usuario"	INTEGER NOT NULL,
                PRIMARY KEY("Persona"),
                FOREIGN KEY("Persona") REFERENCES "Persona"("ID"),
                FOREIGN KEY("Usuario") REFERENCES "Usuario"("Numero_de_ficha"),
                FOREIGN KEY("Tipo") REFERENCES "Tipo"("ID")
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Sede" (
                "ID"	INTEGER,
                "Nombre"	TEXT NOT NULL,
                PRIMARY KEY("ID" AUTOINCREMENT)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Laboratorio" (
                "ID"	INTEGER,
                "Sede"	INTEGER NOT NULL,
                "Nombre"	TEXT NOT NULL,
                PRIMARY KEY("ID" AUTOINCREMENT),
                FOREIGN KEY("Sede") REFERENCES "Sede"("ID")
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Equipo" (
                "Nro_de_bien"	INTEGER,
                "Laboratorio"	INTEGER NOT NULL,
                "Status"	TEXT NOT NULL,
                PRIMARY KEY("Nro_de_bien"),
                FOREIGN KEY("Laboratorio") REFERENCES "Laboratorio"("ID")
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Componente" (
                "Nro_de_bien"	INTEGER,
                "Descripcion"	TEXT NOT NULL,
                PRIMARY KEY("Nro_de_bien"),
                FOREIGN KEY("Nro_de_bien") REFERENCES "Equipo"("Nro_de_bien")
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Tipo_de_uso" (
                "ID"	INTEGER,
                "Descripcion"	TEXT NOT NULL,
                PRIMARY KEY("ID" AUTOINCREMENT)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Asignacion" (
                "ID"	INTEGER,
                "Equipo"	INTEGER,
                "Componente"	INTEGER,
                PRIMARY KEY("ID" AUTOINCREMENT),
                FOREIGN KEY("Equipo") REFERENCES "Equipo"("Nro_de_bien"),
                FOREIGN KEY("Componente") REFERENCES "Componente"("Nro_de_bien")
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Uso_laboratorio_usr" (
                "ID"	INTEGER,
                "Laboratorio"	INTEGER NOT NULL,
                "Administrador"	INTEGER NOT NULL,
                "Tipo_de_uso"	INTEGER NOT NULL,
                "Fecha"	TEXT NOT NULL,
                "Hora_inicio"	TEXT NOT NULL,
                "Hora_finalizacion"	TEXT NOT NULL,
                PRIMARY KEY("ID" AUTOINCREMENT),
                FOREIGN KEY("Tipo_de_uso") REFERENCES "Tipo_de_uso"("ID"),
                FOREIGN KEY("Administrador") REFERENCES "Administrador"("Persona"),
                FOREIGN KEY("Laboratorio") REFERENCES "Laboratorio"("ID")
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Asistencia_usr" (
                "ID"	INTEGER,
                "Uso_laboratorio_usr"	INTEGER NOT NULL,
                "Usuario_laboratorio"	INTEGER NOT NULL,
                "Equipo"	INTEGER NOT NULL,
                PRIMARY KEY("ID" AUTOINCREMENT),
                FOREIGN KEY("Equipo") REFERENCES "Equipo"("Nro_de_bien"),
                FOREIGN KEY("Usuario_laboratorio") REFERENCES "Usuario_laboratorio"("Persona"),
                FOREIGN KEY("Uso_laboratorio_usr") REFERENCES "Uso_laboratorio_usr"("ID")
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Falla_equipo_usr" (
                "ID"	INTEGER,
                "Asistencia_usr"	INTEGER NOT NULL,
                PRIMARY KEY("ID"),
                FOREIGN KEY("Asistencia_usr") REFERENCES "Asistencia_usr"("ID")
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Uso_laboratorio_estudiante" (
                "ID"	INTEGER,
                "Administrador"	INTEGER NOT NULL,
                "Laboratorio"	INTEGER NOT NULL,
                "Fecha"	TEXT NOT NULL,
                "Cantidad"	INTEGER,
                PRIMARY KEY("ID" AUTOINCREMENT),
                FOREIGN KEY("Laboratorio") REFERENCES "Laboratorio"("ID"),
                FOREIGN KEY("Administrador") REFERENCES "Administrador"("Persona")
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Falla_equipo_estudiante" (
                "ID"	INTEGER,
                "Equipo"	INTEGER NOT NULL,
                "Uso_laboratorio_estudiante"	INTEGER NOT NULL,
                PRIMARY KEY("ID" AUTOINCREMENT),
                FOREIGN KEY("Equipo") REFERENCES "Equipo"("Nro_de_bien"),
                FOREIGN KEY("Uso_laboratorio_estudiante") REFERENCES "Uso_laboratorio_estudiante"("ID")
            )
            """
        ]

        print("Inicializando base de datos...")
        for sql in create_tables_sql:
            # Usamos execute_query con commit=True para cada sentencia CREATE TABLE
            result = self.execute_query(sql, commit=True)
            if result is None:
                print(f"Advertencia: Falló la creación de tabla con la consulta: {sql[:50]}...")
        
        print("Base de datos inicializada: tablas creadas o verificadas.")

"""
# Código de ejemplo para probar la clase DBManager
if __name__ == '__main__':
    print("--- Probando DBManager ---")
    db_manager = DBManager()
    
    # Inicializa la base de datos (crea las tablas)
    db_manager.init_database()

    # Ejemplo de inserción de datos en la tabla 'Tipo'
    print("\n--- Insertando datos de prueba en 'Tipo' ---")
    insert_tipo_query = "INSERT INTO Tipo (Descripcion) VALUES (?)"
    if db_manager.execute_query(insert_tipo_query, ("Administrador",), commit=True):
        print("Tipo 'Administrador' insertado.")
    if db_manager.execute_query(insert_tipo_query, ("Profesor",), commit=True):
        print("Tipo 'Profesor' insertado.")
    if db_manager.execute_query(insert_tipo_query, ("Estudiante",), commit=True):
        print("Tipo 'Estudiante' insertado.")

    # Ejemplo de consulta de datos de la tabla 'Tipo'
    print("\n--- Consultando datos de 'Tipo' ---")
    tipos = db_manager.execute_query("SELECT * FROM Tipo")
    if tipos:
        print("Tipos de usuario existentes:")
        for tipo in tipos:
            print(f"ID: {tipo[0]}, Descripción: {tipo[1]}")
    else:
        print("No se encontraron tipos de usuario o hubo un error.")

    # Cierra la conexión al finalizar las pruebas
    db_manager.close_db_connection()
    print("\n--- Pruebas de DBManager finalizadas ---")
"""