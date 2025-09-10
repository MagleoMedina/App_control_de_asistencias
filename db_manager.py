# App_control_de_asistencias/db_manager.py

import libsql
import os
import sys
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

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
        self._executor = ThreadPoolExecutor(max_workers=4)
        print("DBManager inicializado. Credenciales cargadas.")
        
        self.default_parent = None 
    
    def set_parent(self, parent):
        """Define el parent por defecto para mostrar la pantalla de carga."""
        self.default_parent = parent

    def get_db_connection(self):
        """
        Establece y devuelve una conexión a la base de datos Turso.
        Reutiliza la conexión si ya está abierta.
        """
        if self._connection is None:
            try:
                # Conecta a la réplica local ("salu-db.db" en este caso) y la sincroniza con Turso
                self._connection = libsql.connect("salu-db.db", sync_url=self.url, auth_token=self.auth_token)
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

    def execute_query(self, query, params=None, fetch_one=False, commit=False, parent=None):
        """
        Ejecuta una consulta SQL en la base de datos en un hilo aparte.
        mostrando una pantalla de carga si se pasa un parent.
        :param query: La cadena de consulta SQL a ejecutar.
        :param params: Una tupla o lista de parámetros para la consulta (opcional).
        :param fetch_one: Si es True, retorna solo la primera fila del resultado.
        :param commit: Si es True, realiza un commit y sincroniza los cambios.
        :return: El resultado de la consulta (fila/s o True/False para commit), o None en caso de error.
        """
        
        if parent is None:
            parent = self.default_parent  # usa el parent global por defecto
        
        loading = None
        if parent is not None:
            import customtkinter as ctk
            loading = ctk.CTkToplevel(parent)
            loading.title("Cargando...")
            # Tamaño de la ventana
            ancho, alto = 250, 100
            # Dimensiones de la pantalla
            screen_width = parent.winfo_screenwidth()
            screen_height = parent.winfo_screenheight()
            # Coordenadas para centrar
            x = (screen_width // 2) - (ancho // 2)
            y = (screen_height // 2) - (alto // 2)

            loading.geometry(f"{ancho}x{alto}+{x}+{y}")
            loading.transient(parent)   # Mantener sobre la ventana padre
            label = ctk.CTkLabel(loading, text="Procesando, por favor espere...")
            label.pack(expand=True, padx=20, pady=20)
            loading.deiconify() 
            loading.update()
            loading.grab_set()   
        
        def _run_query():
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

        future = self._executor.submit(_run_query)
        
        if loading:
            loading.destroy()
        
        return future.result()  # Espera el resultado pero no bloquea la interfaz principal

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
                "Username"	TEXT,
                "Password"	TEXT,
                PRIMARY KEY("Numero_de_ficha")
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
            CREATE TABLE IF NOT EXISTS "Administrador" (
                "Persona"	INTEGER,
                "Tipo"	INTEGER NOT NULL,
                "Usuario"	INTEGER NOT NULL,
                PRIMARY KEY("Persona"),
                FOREIGN KEY("Persona") REFERENCES "Persona"("ID") ON UPDATE CASCADE,
                FOREIGN KEY("Usuario") REFERENCES "Usuario"("Numero_de_ficha") ON UPDATE CASCADE,
                FOREIGN KEY("Tipo") REFERENCES "Tipo"("ID") ON UPDATE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Usuario_laboratorio" (
                "Persona"	INTEGER,
                "Nombre_organizacion"	TEXT NOT NULL,
                PRIMARY KEY("Persona"),
                FOREIGN KEY("Persona") REFERENCES "Persona"("ID") ON UPDATE CASCADE
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
                FOREIGN KEY("Sede") REFERENCES "Sede"("ID") ON UPDATE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Equipo" (
                "Nro_de_bien"	TEXT,
                "Laboratorio"	INTEGER NOT NULL,
                "Status"	TEXT NOT NULL,
                PRIMARY KEY("Nro_de_bien"),
                FOREIGN KEY("Laboratorio") REFERENCES "Laboratorio"("ID") ON UPDATE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Componente" (
                "Nro_de_bien"	TEXT,
                "Descripcion"	TEXT NOT NULL,
                PRIMARY KEY("Nro_de_bien"),
                FOREIGN KEY("Nro_de_bien") REFERENCES "Equipo"("Nro_de_bien") ON UPDATE CASCADE
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
                "Equipo"	TEXT,
                "Componente"	TEXT,
                PRIMARY KEY("ID" AUTOINCREMENT),
                FOREIGN KEY("Equipo") REFERENCES "Equipo"("Nro_de_bien") ON UPDATE CASCADE,
                FOREIGN KEY("Componente") REFERENCES "Componente"("Nro_de_bien") ON UPDATE CASCADE
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
                FOREIGN KEY("Tipo_de_uso") REFERENCES "Tipo_de_uso"("ID") ON UPDATE CASCADE,
                FOREIGN KEY("Administrador") REFERENCES "Administrador"("Persona") ON UPDATE CASCADE,
                FOREIGN KEY("Laboratorio") REFERENCES "Laboratorio"("ID") ON UPDATE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Asistencia_usr" (
                "ID"	INTEGER,
                "Uso_laboratorio_usr"	INTEGER NOT NULL,
                "Usuario_laboratorio"	INTEGER NOT NULL,
                "Equipo"	TEXT NOT NULL,
                PRIMARY KEY("ID" AUTOINCREMENT),
                FOREIGN KEY("Equipo") REFERENCES "Equipo"("Nro_de_bien") ON UPDATE CASCADE,
                FOREIGN KEY("Usuario_laboratorio") REFERENCES "Usuario_laboratorio"("Persona") ON UPDATE CASCADE,
                FOREIGN KEY("Uso_laboratorio_usr") REFERENCES "Uso_laboratorio_usr"("ID") ON UPDATE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Falla_equipo"(
                "ID" INTEGER,
                "Equipo" TEXT,
                "Fecha_falla" TEXT,
                "Descripcion_falla" TEXT,
                "Hora_de_la_falla" TEXT,
                PRIMARY KEY ("ID" AUTOINCREMENT),
                FOREIGN KEY("Equipo") REFERENCES "Equipo"("Nro_de_bien") ON UPDATE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Falla_equipo_usr" (
                "ID"	INTEGER,
                "Asistencia_usr"	INTEGER NOT NULL,
                PRIMARY KEY("ID"),
                FOREIGN KEY("ID") REFERENCES "Falla_equipo"("ID") ON UPDATE CASCADE,
                FOREIGN KEY("Asistencia_usr") REFERENCES "Asistencia_usr"("ID") ON UPDATE CASCADE
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
                FOREIGN KEY("Laboratorio") REFERENCES "Laboratorio"("ID") ON UPDATE CASCADE,
                FOREIGN KEY("Administrador") REFERENCES "Administrador"("Persona") ON UPDATE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS "Falla_equipo_estudiante" (
                "ID"	INTEGER,
                "Uso_laboratorio_estudiante"	INTEGER NOT NULL,
                PRIMARY KEY("ID"),
                FOREIGN KEY("ID") REFERENCES "Falla_equipo"("ID") ON UPDATE CASCADE,
                FOREIGN KEY("Uso_laboratorio_estudiante") REFERENCES "Uso_laboratorio_estudiante"("ID") ON UPDATE CASCADE
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


    """ ENDPOINTS DEL PROYECTO """ #no son endpoints REST, son funciones que se pueden llamar desde la aplicación 
                                   # Pero hacen lo mismo pe 

    def registrar_usuario(self, username, password, nombre, apellido, cedula, telefono, ficha, tipo_usuario):
        """
        Registra un nuevo usuario en la base de datos.
        Inserta en Persona, Usuario y Administrador.
        Retorna True si el registro fue exitoso, False si hubo error.
        """
        # Verificar si el usuario ya existe por cedula o username
        existe_persona = self.execute_query(
            "SELECT ID FROM Persona WHERE Cedula = ?", (cedula,), fetch_one=True
        )
        existe_usuario = self.execute_query(
            "SELECT Numero_de_ficha FROM Usuario WHERE Username = ?", (username,), fetch_one=True
        )
        if existe_persona or existe_usuario:
            print("El usuario ya existe en la base de datos.")
            return False

        # Insertar en Persona
        persona_sql = """
            INSERT INTO Persona (Nombre, Apellido, Cedula, Nro_telefono)
            VALUES (?, ?, ?, ?)
        """
        persona_result = self.execute_query(
            persona_sql, (nombre, apellido, cedula, telefono), commit=True
        )
        if persona_result is None:
            print("Error al insertar en Persona.")
            return False

        # Obtener el ID de la persona recién creada
        persona_id = self.execute_query(
            "SELECT ID FROM Persona WHERE Cedula = ?", (cedula,), fetch_one=True
        )
        if not persona_id:
            print("No se pudo obtener el ID de la persona.")
            return False
        persona_id = persona_id[0]

        # Insertar en Usuario (ahora incluye Numero_de_ficha)
        usuario_sql = """
            INSERT INTO Usuario (Numero_de_ficha, Username, Password)
            VALUES (?, ?, ?)
        """
        usuario_result = self.execute_query(
            usuario_sql, (ficha, username, password), commit=True
        )
        if usuario_result is None:
            print("Error al insertar en Usuario.")
            return False

        # Obtener el Numero_de_ficha recién creado 
        ficha_id = ficha

        # Obtener el ID del tipo de usuario
        tipo_id = self.execute_query(
            "SELECT ID FROM Tipo WHERE Descripcion = ?", (tipo_usuario,), fetch_one=True
        )
        if not tipo_id:
            print("No se pudo obtener el tipo de usuario.")
            return False
        tipo_id = tipo_id[0]

        # Insertar en Administrador
        admin_sql = """
            INSERT INTO Administrador (Persona, Tipo, Usuario)
            VALUES (?, ?, ?)
        """
        admin_result = self.execute_query(
            admin_sql, (persona_id, tipo_id, ficha_id), commit=True
        )
        if admin_result is None:
            print("Error al insertar en Administrador.")
            return False

        print("Usuario registrado exitosamente en la base de datos.")
        return True

    def obtener_tipos_usuario(self):
        """
        Obtiene la lista de tipos de usuario desde la tabla Tipo.
        Retorna una lista de descripciones.
        """
        tipos = self.execute_query(
            "SELECT Descripcion FROM Tipo", fetch_one=False
        )
        if tipos is None:
            return []
        return [t[0] for t in tipos]

    def buscar_usuario_por_cedula(self, cedula):
        """
        Busca y retorna los datos completos de un usuario por su cédula.
        Retorna un diccionario con los campos o None si no existe.
        """
        query = """
        SELECT
            u.Username,
            u.Password,
            p.Nombre,
            p.Apellido,
            p.Cedula,
            p.Nro_telefono,
            u.Numero_de_ficha,
            t.Descripcion as Tipo_usuario
        FROM Persona p
        JOIN Administrador a ON a.Persona = p.ID
        JOIN Usuario u ON a.Usuario = u.Numero_de_ficha
        JOIN Tipo t ON a.Tipo = t.ID
        WHERE p.Cedula = ?
        """
        result = self.execute_query(query, (cedula,), fetch_one=True)
        if not result:
            return None
        return {
            "Username": result[0],
            "Password": result[1],
            "Nombre": result[2],
            "Apellido": result[3],
            "Cedula": result[4],
            "Nro_telefono": result[5],
            "Numero_de_ficha": result[6],
            "Tipo_usuario": result[7]
        }

    def actualizar_usuario_por_cedula(self, cedula, username, password, nombre, apellido, telefono, ficha, tipo_usuario):
        """
        Actualiza los datos de un usuario en la base de datos por su cédula.
        Actualiza Persona, Usuario y Administrador.
        Retorna True si la actualización fue exitosa, False si hubo error.
        """
        # Obtener el ID de la persona
        persona_id = self.execute_query(
            "SELECT ID FROM Persona WHERE Cedula = ?", (cedula,), fetch_one=True
        )
        if not persona_id:
            print("No se encontró la persona con esa cédula.")
            return False
        persona_id = persona_id[0]

        # Actualizar Persona
        persona_sql = """
            UPDATE Persona SET Nombre = ?, Apellido = ?, Nro_telefono = ? WHERE ID = ?
        """
        persona_result = self.execute_query(
            persona_sql, (nombre, apellido, telefono, persona_id), commit=True
        )
        if persona_result is None:
            print("Error al actualizar Persona.")
            return False

        # Actualizar Usuario
        usuario_sql = """
            UPDATE Usuario SET Username = ?, Password = ?, Numero_de_ficha = ? WHERE Numero_de_ficha = (
                SELECT Usuario FROM Administrador WHERE Persona = ?
            )
        """
        usuario_result = self.execute_query(
            usuario_sql, (username, password, ficha, persona_id), commit=True
        )
        if usuario_result is None:
            print("Error al actualizar Usuario.")
            return False

        # Obtener el ID del tipo de usuario
        tipo_id = self.execute_query(
            "SELECT ID FROM Tipo WHERE Descripcion = ?", (tipo_usuario,), fetch_one=True
        )
        if not tipo_id:
            print("No se pudo obtener el tipo de usuario.")
            return False
        tipo_id = tipo_id[0]

        # Actualizar Administrador
        admin_sql = """
            UPDATE Administrador SET Tipo = ?, Usuario = ? WHERE Persona = ?
        """
        admin_result = self.execute_query(
            admin_sql, (tipo_id, ficha, persona_id), commit=True
        )
        if admin_result is None:
            print("Error al actualizar Administrador.")
            return False

        print("Usuario actualizado exitosamente en la base de datos.")
        return True

    def recuperar_credenciales_por_cedula(self, cedula):
        """
        Recupera el Username y Password de un usuario por su cédula.
        Retorna un diccionario con 'Username' y 'Password', o None si no existe.
        """
        query = """
        SELECT u.Username, u.Password
        FROM Persona p
        JOIN Administrador a ON a.Persona = p.ID
        JOIN Usuario u ON a.Usuario = u.Numero_de_ficha
        WHERE p.Cedula = ?
        """
        result = self.execute_query(query, (cedula,), fetch_one=True)
        if not result:
            return None
        return {"Username": result[0], "Password": result[1]}

    def eliminar_credenciales_por_cedula(self, cedula):
        """
        Elimina únicamente el Username y Password de la tabla Usuario para el usuario con la cédula dada.
        Mantiene el registro y la primary key Numero_de_ficha.
        Retorna True si la operación fue exitosa, False si hubo error o no existe.
        """
        # Obtener el Numero_de_ficha del usuario por la cédula
        ficha = self.execute_query(
            "SELECT u.Numero_de_ficha FROM Persona p JOIN Administrador a ON a.Persona = p.ID JOIN Usuario u ON a.Usuario = u.Numero_de_ficha WHERE p.Cedula = ?",
            (cedula,), fetch_one=True
        )
        if not ficha:
            print("No se encontró usuario con esa cédula.")
            return False
        ficha = ficha[0]

        # Actualizar Usuario: dejar Username y Password vacíos
        update_sql = "UPDATE Usuario SET Username = '', Password = '' WHERE Numero_de_ficha = ?"
        result = self.execute_query(update_sql, (ficha,), commit=True)
        if result:
            print("Credenciales eliminadas de la tabla Usuario.")
            return True
        else:
            print("Error al eliminar las credenciales del usuario.")
            return False

    def agregar_sede(self, nombre):
        """
        Inserta una nueva sede en la tabla Sede.
        Retorna True si fue exitoso, False si hubo error.
        """
        sql = "INSERT INTO Sede (Nombre) VALUES (?)"
        result = self.execute_query(sql, (nombre,), commit=True)
        return result is not None

    def obtener_sedes(self):
        """
        Obtiene la lista de sedes (ID y Nombre).
        Retorna una lista de tuplas (ID, Nombre).
        """
        sql = "SELECT ID, Nombre FROM Sede"
        result = self.execute_query(sql)
        if result is None:
            return []
        return result

    def obtener_laboratorios_por_sede(self, sede_id):
        """
        Obtiene la lista de laboratorios (ID y Nombre) para una sede específica.
        Retorna una lista de tuplas (ID, Nombre).
        """
        sql = "SELECT ID, Nombre FROM Laboratorio WHERE Sede = ?"
        result = self.execute_query(sql, (sede_id,))
        if result is None:
            return []
        #print(f"[DEBUG] Laboratorios encontrados para sede_id={sede_id}: {result}")
        return result
        

    def agregar_laboratorio(self, nombre, sede_id):
        """
        Inserta un nuevo laboratorio relacionado con una sede.
        Retorna True si fue exitoso, False si hubo error.
        """
        sql = "INSERT INTO Laboratorio (Sede, Nombre) VALUES (?, ?)"
        result = self.execute_query(sql, (sede_id, nombre), commit=True)
        return result is not None

    def agregar_equipo(self, nro_bien, laboratorio_id, status, descripcion_equipo):
        """
        Inserta un nuevo equipo en la tabla Equipo y su tipo en la tabla Componente.
        Retorna True si fue exitoso, False si hubo error.
        """
        # Verificar si ya existe el equipo
        existe = self.execute_query(
            "SELECT Nro_de_bien FROM Equipo WHERE Nro_de_bien = ?", (nro_bien,), fetch_one=True
        )
        if existe:
            print("El equipo ya existe en la base de datos.")
            return False

        # Insertar en Equipo
        sql_equipo = "INSERT INTO Equipo (Nro_de_bien, Laboratorio, Status) VALUES (?, ?, ?)"
        result_equipo = self.execute_query(sql_equipo, (nro_bien, laboratorio_id, status), commit=True)
        if result_equipo is None:
            print("Error al insertar en Equipo.")
            return False

        # Insertar en Componente
        sql_componente = "INSERT INTO Componente (Nro_de_bien, Descripcion) VALUES (?, ?)"
        result_componente = self.execute_query(sql_componente, (nro_bien, descripcion_equipo), commit=True)
        if result_componente is None:
            print("Error al insertar en Componente.")
            return False

        print("Equipo y componente registrados exitosamente.")
        return True

    def obtener_tipos_equipo(self):
        """
        Obtiene la lista de tipos de equipo desde la tabla Componente (únicos).
        Retorna una lista de descripciones.
        """
        sql = "SELECT DISTINCT Descripcion FROM Componente"
        result = self.execute_query(sql)
        if result is None:
            return []
        return [r[0] for r in result]

    def buscar_equipo_por_nro_bien(self, nro_bien):
        """
        Busca un equipo por su número de bien y retorna toda su información relevante:
        nro_bien, laboratorio_id, laboratorio_nombre, sede_id, sede_nombre, status, descripcion_equipo.
        Retorna None si no existe.
        """
        query = """
        SELECT 
            e.Nro_de_bien,
            e.Laboratorio,
            l.Nombre as laboratorio_nombre,
            s.ID as sede_id,
            s.Nombre as sede_nombre,
            e.Status,
            c.Descripcion
        FROM Equipo e
        JOIN Laboratorio l ON e.Laboratorio = l.ID
        JOIN Sede s ON l.Sede = s.ID
        JOIN Componente c ON e.Nro_de_bien = c.Nro_de_bien
        WHERE e.Nro_de_bien = ?
        """
        result = self.execute_query(query, (nro_bien,), fetch_one=True)
        if not result:
            return None
        return {
            "nro_bien": result[0],
            "laboratorio_id": result[1],
            "laboratorio_nombre": result[2],
            "sede_id": result[3],
            "sede_nombre": result[4],
            "status": result[5],
            "descripcion_equipo": result[6]
        }

    def actualizar_equipo(self, nro_bien, laboratorio_id, status, descripcion_equipo):
        """
        Actualiza los datos del equipo y su tipo en la base de datos.
        Retorna True si fue exitoso, False si hubo error.
        """
        # Actualizar Equipo
        sql_equipo = "UPDATE Equipo SET Laboratorio = ?, Status = ? WHERE Nro_de_bien = ?"
        result_equipo = self.execute_query(sql_equipo, (laboratorio_id, status, nro_bien), commit=True)
        if result_equipo is None:
            print("Error al actualizar Equipo.")
            return False

        # Actualizar Componente
        sql_componente = "UPDATE Componente SET Descripcion = ? WHERE Nro_de_bien = ?"
        result_componente = self.execute_query(sql_componente, (descripcion_equipo, nro_bien), commit=True)
        if result_componente is None:
            print("Error al actualizar Componente.")
            return False

        print("Equipo y componente actualizados exitosamente.")
        return True

    def actualizar_equipo_con_nuevo_nro_bien(self, nro_bien_actual, nuevo_nro_bien, laboratorio_id, status, descripcion_equipo):
        """
        Actualiza los datos del equipo, incluyendo el cambio de número de bien (clave primaria).
        Actualiza tanto en Equipo como en Componente.
        Retorna True si fue exitoso, False si hubo error.
        """
        # Verificar si el nuevo número de bien ya existe (y no es el mismo registro)
        if str(nro_bien_actual) != str(nuevo_nro_bien):
            existe = self.execute_query(
                "SELECT Nro_de_bien FROM Equipo WHERE Nro_de_bien = ?", (nuevo_nro_bien,), fetch_one=True
            )
            if existe:
                print("Ya existe un equipo con ese nuevo número de bien.")
                return False

        # Actualizar SOLO el equipo seleccionado
        sql_equipo = "UPDATE Equipo SET Nro_de_bien = ?, Laboratorio = ?, Status = ? WHERE Nro_de_bien = ?"
        result_equipo = self.execute_query(sql_equipo, (nuevo_nro_bien, laboratorio_id, status, nro_bien_actual), commit=True)
        if result_equipo is None:
            print("Error al actualizar Equipo.")
            return False

        #Actualizar SOLO el componente seleccionado
        sql_componente = "UPDATE Componente SET Nro_de_bien = ?, Descripcion = ? WHERE Nro_de_bien = ?"
        result_componente = self.execute_query(sql_componente, (nuevo_nro_bien, descripcion_equipo, nro_bien_actual), commit=True)
        if result_componente is None:
            print("Error al actualizar Componente.")
            return False

        print("Equipo y componente actualizados exitosamente (incluyendo número de bien).")
        return True

    def existe_equipo(self, nro_bien, descripcion):
        """
        Verifica si existe un equipo con el número de bien y la descripción dada.
        Retorna (True, None) si existe y coincide, (False, mensaje_error) si no.
        """
        result = self.execute_query(
            "SELECT c.Descripcion FROM Equipo e JOIN Componente c ON e.Nro_de_bien = c.Nro_de_bien WHERE e.Nro_de_bien = ?",
            (nro_bien,), fetch_one=True
        )
        if not result:
            return False, f"No se encuentra {descripcion} con el número de bien {nro_bien} en el sistema."
        if result[0] != descripcion:
            return False, f"No se encuentra {descripcion} con el número de bien {nro_bien} en el sistema."
        return True, None

    def relacionar_equipos(self, computadora, teclado, monitor, raton):
        """
        Registra la relación de los equipos en la tabla Asignacion.
        Cada componente se relaciona con la computadora.
        Retorna True si todas las asignaciones fueron exitosas, False si hubo error.
        """
        # Relacionar cada componente con la computadora
        componentes = [teclado, monitor, raton]
        for componente in componentes:
            # Verifica si ya existe la relación para evitar duplicados
            existe = self.execute_query(
                "SELECT 1 FROM Asignacion WHERE Equipo = ? AND Componente = ?", (computadora, componente), fetch_one=True
            )
            if not existe:
                sql = "INSERT INTO Asignacion (Equipo, Componente) VALUES (?, ?)"
                result = self.execute_query(sql, (computadora, componente), commit=True)
                if result is None:
                    return False
        return True

    def registrar_asistencia_laboratorio_usr(self, laboratorio_id, tipo_uso, fecha, hora_inicio, hora_finalizacion, personas, admin_id):
        """
        Registra el uso del laboratorio y la asistencia de usuarios.
        - laboratorio_id: ID del laboratorio
        - tipo_uso: descripción del tipo de uso
        - fecha, hora_inicio, hora_finalizacion: strings
        - personas: lista de dicts con datos de cada persona
        """
        # Obtener el ID del tipo de uso
        tipo_uso_id = self.execute_query(
            "SELECT ID FROM Tipo_de_uso WHERE Descripcion = ?", (tipo_uso,), fetch_one=True
        )
        if not tipo_uso_id:
            print("Tipo de uso no encontrado.")
            return False
        tipo_uso_id = tipo_uso_id[0]

        # Insertar el uso del laboratorio
        uso_sql = """
            INSERT INTO Uso_laboratorio_usr (Laboratorio, Administrador, Tipo_de_uso, Fecha, Hora_inicio, Hora_finalizacion)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        # Para este ejemplo, Administrador se pone como NULL (o puedes pasar el ID si lo tienes)
        uso_result = self.execute_query(
            uso_sql, (laboratorio_id, admin_id, tipo_uso_id, fecha, hora_inicio, hora_finalizacion), commit=True
        )
        if uso_result is None:
            print("Error al registrar uso de laboratorio.")
            return False

        # Obtener el ID del uso recién creado
        uso_id = self.execute_query(
            "SELECT MAX(ID) FROM Uso_laboratorio_usr", fetch_one=True
        )[0]

        # Registrar cada persona en Usuario_laboratorio y Asistencia_usr
        for persona in personas:
            # Insertar en Persona si no existe
            persona_id = self.execute_query(
                "SELECT ID FROM Persona WHERE Cedula = ?", (persona['cedula'],), fetch_one=True
            )
            if not persona_id:
                persona_sql = """
                    INSERT INTO Persona (Nombre, Apellido, Cedula, Nro_telefono)
                    VALUES (?, ?, ?, ?)
                """
                self.execute_query(
                    persona_sql, (persona['nombre'], persona['apellido'], persona['cedula'], persona['telefono']), commit=True
                )
                persona_id = self.execute_query(
                    "SELECT ID FROM Persona WHERE Cedula = ?", (persona['cedula'],), fetch_one=True
                )
            persona_id = persona_id[0]

            # Insertar en Usuario_laboratorio si no existe
            usuario_lab_id = self.execute_query(
                "SELECT Persona FROM Usuario_laboratorio WHERE Persona = ?", (persona_id,), fetch_one=True
            )
            if not usuario_lab_id:
                usuario_lab_sql = """
                    INSERT INTO Usuario_laboratorio (Persona, Nombre_organizacion)
                    VALUES (?, ?)
                """
                self.execute_query(
                    usuario_lab_sql, (persona_id, persona['organizacion']), commit=True
                )

            # Insertar en Asistencia_usr
            asistencia_sql = """
                INSERT INTO Asistencia_usr (Uso_laboratorio_usr, Usuario_laboratorio, Equipo)
                VALUES (?, ?, ?)
            """
            self.execute_query(
                asistencia_sql, (uso_id, persona_id, persona['numero_bien']), commit=True
            )
        print("Asistencia registrada correctamente.")
        return True

    def registrar_falla_equipo_usr(self, asistencias, fallas):
        """
        Registra las fallas de equipos para las asistencias dadas.
        - asistencias: lista de IDs de Asistencia_usr
        - fallas: lista de dicts con datos de la falla (nro_bien, descripcion, hora_falla)
        """
        for asistencia_id, falla in zip(asistencias, fallas):
            falla_sql = """
                INSERT INTO Falla_equipo_usr (Asistencia_usr)
                VALUES (?)
            """
            self.execute_query(falla_sql, (asistencia_id,), commit=True)
            # Puedes agregar más campos si la tabla tiene más columnas
        print("Fallas de equipos registradas correctamente.")
        return True

    def registrar_falla_equipo_completa(self, asistencia_id, equipo_id, descripcion_falla, fecha_falla, hora_falla):
        """
        Registra una falla de equipo con descripción, fecha y hora en Falla_equipo,
        y la relaciona con la asistencia en Falla_equipo_usr.
        Retorna True si ambas inserciones fueron exitosas, False si hubo error.
        """
        # Insertar en Falla_equipo
        falla_sql = """
            INSERT INTO Falla_equipo (Equipo, Fecha_falla, Descripcion_falla, Hora_de_la_falla)
            VALUES (?, ?, ?, ?)
        """
        result_falla = self.execute_query(falla_sql, (equipo_id, fecha_falla, descripcion_falla, hora_falla), commit=True)
        if result_falla is None:
            print("Error al insertar en Falla_equipo.")
            return False

        # Obtener el ID recién creado de Falla_equipo
        falla_id = self.execute_query(
            "SELECT MAX(ID) FROM Falla_equipo", fetch_one=True
        )
        if not falla_id:
            print("No se pudo obtener el ID de la falla.")
            return False
        falla_id = falla_id[0]

        # Relacionar con Falla_equipo_usr
        relacion_sql = """
            INSERT INTO Falla_equipo_usr (ID, Asistencia_usr)
            VALUES (?, ?)
        """
        result_relacion = self.execute_query(relacion_sql, (falla_id, asistencia_id), commit=True)
        if result_relacion is None:
            print("Error al relacionar Falla_equipo con Falla_equipo_usr.")
            return False

        print("Falla registrada y relacionada correctamente.")
        return True

    def registrar_falla_equipo_estudiante(self, uso_laboratorio_estudiante_id, equipo_id, descripcion_falla, fecha_falla, hora_falla):
        """
        Registra una falla de equipo en Falla_equipo y la relaciona con Uso_laboratorio_estudiante en Falla_equipo_estudiante.
        Retorna True si ambas inserciones fueron exitosas, False si hubo error.
        """
        # Insertar en Falla_equipo
        falla_sql = """
            INSERT INTO Falla_equipo (Equipo, Fecha_falla, Descripcion_falla, Hora_de_la_falla)
            VALUES (?, ?, ?, ?)
        """
        result_falla = self.execute_query(falla_sql, (equipo_id, fecha_falla, descripcion_falla, hora_falla), commit=True)
        if result_falla is None:
            print("Error al insertar en Falla_equipo.")
            return False

        # Obtener el ID recién creado de Falla_equipo
        falla_id = self.execute_query(
            "SELECT MAX(ID) FROM Falla_equipo", fetch_one=True
        )
        if not falla_id:
            print("No se pudo obtener el ID de la falla.")
            return False
        falla_id = falla_id[0]

        # Relacionar con Falla_equipo_estudiante
        relacion_sql = """
            INSERT INTO Falla_equipo_estudiante (ID, Uso_laboratorio_estudiante)
            VALUES (?, ?)
        """
        result_relacion = self.execute_query(relacion_sql, (falla_id, uso_laboratorio_estudiante_id), commit=True)
        if result_relacion is None:
            print("Error al relacionar Falla_equipo con Falla_equipo_estudiante.")
            return False

        print("Falla de equipo de estudiante registrada y relacionada correctamente.")
        return True

    def obtener_tipos_uso(self):
        """
        Obtiene la lista de tipos de uso desde la tabla Tipo_de_uso.
        Retorna una lista de descripciones.
        """
        tipos = self.execute_query(
            "SELECT Descripcion FROM Tipo_de_uso", fetch_one=False
        )
        if tipos is None:
            return []
        return [t[0] for t in tipos]

    def consultar_asistencias_por_fecha(self, sede_nombre, laboratorio_nombre, fecha):
        """
        Consulta todas las asistencias para una sede, laboratorio y fecha específica.
        Retorna una lista de dicts, cada uno con hora_inicio, hora_finalizacion y lista de personas.
        El orden es de menor a mayor según la hora de inicio.
        """
        # Obtener IDs de sede y laboratorio
        sede = self.execute_query("SELECT ID FROM Sede WHERE Nombre = ?", (sede_nombre,), fetch_one=True)
        if not sede:
            return []
        sede_id = sede[0]
        lab = self.execute_query("SELECT ID FROM Laboratorio WHERE Nombre = ? AND Sede = ?", (laboratorio_nombre, sede_id), fetch_one=True)
        if not lab:
            return []
        lab_id = lab[0]

        # Obtener todos los usos de laboratorio para esa fecha, ordenados por hora_inicio ASC
        usos = self.execute_query(
            """
            SELECT uso.ID, uso.Tipo_de_uso, uso.Hora_inicio, uso.Hora_finalizacion,
                p.Nombre, p.Apellido
            FROM Uso_laboratorio_usr uso
            JOIN Administrador a ON uso.Administrador = a.Persona
            JOIN Persona p ON a.Persona = p.ID
            WHERE uso.Laboratorio = ? AND uso.Fecha = ?
            ORDER BY uso.Hora_inicio ASC
            """,
            (lab_id, fecha)
        )
        if not usos:
            return []

        bloques = []
        for uso in usos:
            uso_id, tipo_uso_id, hora_inicio, hora_finalizacion, admin_nombre, admin_apellido = uso
            tipo_uso = self.execute_query("SELECT Descripcion FROM Tipo_de_uso WHERE ID = ?", (tipo_uso_id,), fetch_one=True)
            tipo_uso = tipo_uso[0] if tipo_uso else ""

            # Obtener todas las asistencias asociadas a este uso
            asistencias = self.execute_query(
                """
                SELECT
                    p.Nombre,
                    p.Apellido,
                    p.Cedula,
                    p.Nro_telefono,
                    ul.Nombre_organizacion,
                    e.Nro_de_bien
                FROM Asistencia_usr a
                JOIN Usuario_laboratorio ul ON a.Usuario_laboratorio = ul.Persona
                JOIN Persona p ON ul.Persona = p.ID
                JOIN Equipo e ON a.Equipo = e.Nro_de_bien
                WHERE a.Uso_laboratorio_usr = ?
                """,
                (uso_id,)
            )
            personas = []
            for fila in asistencias:
                personas.append({
                    "Tipo de uso": tipo_uso,
                    "Nombre": fila[0],
                    "Apellido": fila[1],
                    "Cédula": fila[2],
                    "Organización": fila[4],
                    "Teléfono": fila[3],
                    "Número de bien": fila[5]
                })
            bloques.append({
                "hora_inicio": hora_inicio,
                "hora_finalizacion": hora_finalizacion,
                "tipo_uso": tipo_uso,
                "personas": personas,
                "admin_nombre": admin_nombre,
                "admin_apellido": admin_apellido
            })
        return bloques

    def consultar_equipo_con_componentes(self, nro_bien):
        """
        Consulta la relación de un equipo con sus componentes, incluyendo descripción, número de bien,
        sede, laboratorio y status.
        Retorna una lista de dicts con los datos.
        """
        query = """
        SELECT
            c.Descripcion,
            e.Nro_de_bien,
            s.Nombre as sede,
            l.Nombre as laboratorio,
            e.Status
        FROM Equipo e
        JOIN Laboratorio l ON e.Laboratorio = l.ID
        JOIN Sede s ON l.Sede = s.ID
        JOIN Componente c ON e.Nro_de_bien = c.Nro_de_bien
        WHERE e.Nro_de_bien = ?
        UNION
        SELECT
            c.Descripcion,
            c.Nro_de_bien,
            s.Nombre as sede,
            l.Nombre as laboratorio,
            eq.Status
        FROM Asignacion a
        JOIN Componente c ON a.Componente = c.Nro_de_bien
        JOIN Equipo eq ON c.Nro_de_bien = eq.Nro_de_bien
        JOIN Laboratorio l ON eq.Laboratorio = l.ID
        JOIN Sede s ON l.Sede = s.ID
        WHERE a.Equipo = ?
        """
        result = self.execute_query(query, (nro_bien, nro_bien))
        if not result:
            return []
        equipos = []
        for row in result:
            equipos.append({
                "Descripcion": row[0],
                "Nro_de_bien": row[1],
                "Sede": row[2],
                "Laboratorio": row[3],
                "Status": row[4]
            })
        return equipos
       

    def consultar_fallas_por_equipo(self, nro_bien):
        """
        Consulta las fallas registradas para un equipo por su número de bien.
        Retorna una lista de dicts con fecha, hora y descripción.
        """
        query = """
        SELECT Fecha_falla, Hora_de_la_falla, Descripcion_falla
        FROM Falla_equipo
        WHERE Equipo = ?
        ORDER BY Fecha_falla DESC, Hora_de_la_falla DESC
        """
        result = self.execute_query(query, (nro_bien,))
        if not result:
            return []
        fallas = []
        for row in result:
            fallas.append({
                "FechaHora": f"{row[0]} {row[1]}",
                "Descripcion": row[2],
                "Equipo": nro_bien
            })
        return fallas

    def obtener_laboratorio_id_por_nombre_y_sede(self, laboratorio_nombre, sede_id):
        """
        Obtiene el ID del laboratorio dado su nombre y el ID de la sede.
        Retorna el ID o None si no existe.
        """
        result = self.execute_query(
            "SELECT ID FROM Laboratorio WHERE Nombre = ? AND Sede = ?",
            (laboratorio_nombre, sede_id),
            fetch_one=True
        )
        if result:
            return result[0]
        return None

    def registrar_asistencia_estudiantes(self, administrador_id, laboratorio_id, fecha, cantidad):
        """
        Registra la asistencia de estudiantes en la tabla Uso_laboratorio_estudiante.
        Retorna True si fue exitoso, False si hubo error.
        """
        sql = """
            INSERT INTO Uso_laboratorio_estudiante (Administrador, Laboratorio, Fecha, Cantidad)
            VALUES (?, ?, ?, ?)
        """
        result = self.execute_query(sql, (administrador_id, laboratorio_id, fecha, cantidad), commit=True)
        return result is not None

    def obtener_estadisticas_actividades(self, sede_nombre, laboratorio_nombre, fecha_inicio, fecha_finalizacion):
        """
        Obtiene las estadísticas de actividades (tipos de uso) y la cantidad de personas atendidas
        en un intervalo de fechas para una sede y laboratorio específicos.
        Retorna una lista de dicts: {"nombre": actividad, "cantidad": cantidad}
        """
        # Obtener IDs de sede y laboratorio
        sede = self.execute_query("SELECT ID FROM Sede WHERE Nombre = ?", (sede_nombre,), fetch_one=True)
        if not sede:
            return [], 0
        sede_id = sede[0]
        lab = self.execute_query("SELECT ID FROM Laboratorio WHERE Nombre = ? AND Sede = ?", (laboratorio_nombre, sede_id), fetch_one=True)
        if not lab:
            return [], 0
        lab_id = lab[0]

        # Obtener todos los tipos de uso
        tipos_uso = self.execute_query("SELECT ID, Descripcion FROM Tipo_de_uso", fetch_one=False)
        if not tipos_uso:
            return [], 0

        estadisticas = []
        total_personas = 0

        for tipo_id, descripcion in tipos_uso:
            # Contar la cantidad de personas atendidas para este tipo de uso en el intervalo de fechas
            query = """
                SELECT COUNT(a.ID)
                FROM Uso_laboratorio_usr u
                LEFT JOIN Asistencia_usr a ON a.Uso_laboratorio_usr = u.ID
                WHERE u.Laboratorio = ?
                AND u.Tipo_de_uso = ?
                AND u.Fecha >= ? AND u.Fecha <= ?
            """
            result = self.execute_query(query, (lab_id, tipo_id, fecha_inicio, fecha_finalizacion), fetch_one=True)
            cantidad = result[0] if result else 0
            estadisticas.append({"nombre": descripcion, "cantidad": cantidad})
            total_personas += cantidad

        return estadisticas, total_personas
    
    def autenticar_usuario(self, username, password):
        """
        Verifica si existe un usuario con username y password.
        Retorna un diccionario con los datos si existe, o None si no.
        """
        query = """
        SELECT a.Persona AS Admin_id, u.Numero_de_ficha  AS Usuario_id, u.Username, u.Password, 
        p.Nombre, p.Apellido, t.Descripcion  AS Tipo_usuario
        FROM Usuario u
        JOIN Administrador a ON a.Usuario = u.Numero_de_ficha
        JOIN Persona p ON a.Persona = p.ID
        JOIN Tipo t ON a.Tipo = t.ID
        WHERE u.Username = ? AND u.Password = ?
        """
        result = self.execute_query(query, (username, password), fetch_one=True)
        if result:
            return {
                "Admin_id":    result[0], 
                "Usuario_id":  result[1],
                "Username":    result[2],
                "Password":    result[3],
                "Nombre":      result[4],
                "Apellido":    result[5],
                "Tipo_usuario":result[6],
            }
        return None