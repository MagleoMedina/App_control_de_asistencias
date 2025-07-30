import customtkinter as ctk
from tkinter import messagebox
from db_manager import DBManager

#Clase encargada de registrar nuevos usuarios
class GestionUsuarios(ctk.CTkFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # Título
        self.label_titulo = ctk.CTkLabel(self, text="Selecciona una opcion")
        self.label_titulo.grid(row=0, column=0, columnspan=4, pady=10)

        # Botón Crear
        self.boton_crear = ctk.CTkButton(self, text="Crear", command=self.crear_usuario)
        self.boton_crear.grid(row=1, column=0, padx=5, pady=5)

        # Botón Modificar
        self.boton_modificar = ctk.CTkButton(self, text="Modificar", command=self.modificar_usuario)
        self.boton_modificar.grid(row=1, column=1, padx=5, pady=5)

        # Botón Recuperar Credenciales
        self.boton_recuperar = ctk.CTkButton(self, text="Recuperar Credenciales", command=self.recuperar_credenciales)
        self.boton_recuperar.grid(row=1, column=2, padx=5, pady=5)

        # Botón Eliminar Credenciales
        self.boton_eliminar = ctk.CTkButton(self, text="Eliminar Credenciales", command=self.eliminar_usuario)
        self.boton_eliminar.grid(row=1, column=3, padx=5, pady=5)

    def limpiar_pantalla(self):
        for widget in self.winfo_children():
            if widget not in [self.label_titulo, self.boton_crear, self.boton_modificar, self.boton_recuperar, self.boton_eliminar]:
                widget.grid_forget()

    def crear_usuario(self):
        self.limpiar_pantalla()
        VentanaRegistro(self).grid(row=2, column=0, columnspan=4, pady=10)

    def modificar_usuario(self):
        self.limpiar_pantalla()
        ModificarDatos(self).grid(row=2, column=0, columnspan=4, pady=10)

    def recuperar_credenciales(self):
        self.limpiar_pantalla()
        RecuperarDatosApp(self).grid(row=2, column=0, columnspan=4, pady=10)

    def eliminar_usuario(self):
        self.limpiar_pantalla()
        EliminarUsuario(self).grid(row=2, column=0, columnspan=4, pady=10)
        

#Clase encargada de registrar nuevos usuarios
class VentanaRegistro(ctk.CTkFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.db = DBManager()

        # Nombre de usuario
        self.label_usuario = ctk.CTkLabel(self, text="Nombre de Usuario:")
        self.label_usuario.grid(row=0, column=0, sticky='w', pady=5)
        self.entry_usuario = ctk.CTkEntry(self)
        self.entry_usuario.grid(row=0, column=1, pady=5)

        # Contraseña
        self.label_password = ctk.CTkLabel(self, text="Contraseña:")
        self.label_password.grid(row=1, column=0, sticky='w', pady=5)
        self.entry_password = ctk.CTkEntry(self) #show ="*" para colocar *** al tipear
        self.entry_password.grid(row=1, column=1, pady=5)

        # Nombre
        self.label_nombre = ctk.CTkLabel(self, text="Nombre:")
        self.label_nombre.grid(row=2, column=0, sticky='w', pady=5)
        self.entry_nombre = ctk.CTkEntry(self)
        self.entry_nombre.grid(row=2, column=1, pady=5)

        # Apellido
        self.label_apellido = ctk.CTkLabel(self, text="Apellido:")
        self.label_apellido.grid(row=3, column=0, sticky='w', pady=5)
        self.entry_apellido = ctk.CTkEntry(self)
        self.entry_apellido.grid(row=3, column=1, pady=5)

        # Validación para permitir solo números
        validate_numeric = self.register(self.solo_numeros)

        # Cédula
        self.label_cedula = ctk.CTkLabel(self, text="Cédula:")
        self.label_cedula.grid(row=4, column=0, sticky='w', pady=5)
        self.entry_cedula = ctk.CTkEntry(self, validate="key", validatecommand=(validate_numeric, '%S'))
        self.entry_cedula.grid(row=4, column=1, pady=5)

        # Número de teléfono
        self.label_telefono = ctk.CTkLabel(self, text="Número de Teléfono:")
        self.label_telefono.grid(row=5, column=0, sticky='w', pady=5)
        self.entry_telefono = ctk.CTkEntry(self, validate="key", validatecommand=(validate_numeric,  '%S' ))
        self.entry_telefono.grid(row=5, column=1, pady=5)


        # Número de ficha de trabajador
        self.label_ficha = ctk.CTkLabel(self, text="Número de Ficha:")
        self.label_ficha.grid(row=6, column=0, sticky='w', pady=5)
        self.entry_ficha = ctk.CTkEntry(self, validate="key", validatecommand=(validate_numeric, '%S'))
        self.entry_ficha.grid(row=6, column=1, pady=5)

        # Tipo de usuario
        self.label_tipo_usuario = ctk.CTkLabel(self, text="Tipo de Usuario:")
        self.label_tipo_usuario.grid(row=7, column=0, sticky='w', pady=5)
        values = self.db.obtener_tipos_usuario() # Extrae los tipos desde la BD
        self.combo_tipo_usuario = ctk.CTkComboBox(self, values=values)
        self.combo_tipo_usuario.grid(row=7, column=1, pady=5)

        # Botón de registro
        self.boton_registro = ctk.CTkButton(self, text="Registrar", command=self.registrar_usuario)
        self.boton_registro.grid(row=8, column=0, columnspan=2, pady=20)  # Centrar el botón

    def registrar_usuario(self):
        """Función que se ejecuta al hacer clic en 'Registrar'."""
        datos = {
            "Nombre de usuario": self.entry_usuario.get(),
            "Contraseña": self.entry_password.get(),
            "Nombre": self.entry_nombre.get(),
            "Apellido": self.entry_apellido.get(),
            "Cédula": self.entry_cedula.get(),
            "Teléfono": self.entry_telefono.get(),
            "Número de ficha": self.entry_ficha.get(),
            "Tipo de usuario": self.combo_tipo_usuario.get(),
        }

        # Verificar si algún campo está vacío
        campos_vacios = [campo for campo, valor in datos.items() if not valor]
        if campos_vacios:
            messagebox.showwarning("Error", "Por favor, completa todos los campos.")
        else:
            # Lógica de registro en la base de datos
            resultado = self.db.registrar_usuario(
                datos["Nombre de usuario"],
                datos["Contraseña"],
                datos["Nombre"],
                datos["Apellido"],
                datos["Cédula"],
                datos["Teléfono"],
                datos["Número de ficha"],
                datos["Tipo de usuario"]
            )
            if resultado:
                messagebox.showinfo("Registro exitoso", "Usuario registrado exitosamente.")
            else:
                messagebox.showerror("Error", "No se pudo registrar el usuario. Verifica los datos o si ya existe.")

    def solo_numeros(self, char):
        """Validación para aceptar solo caracteres numéricos."""
        return char.isdigit()   

    def iniciar(self):
        """Inicia el bucle principal de la ventana."""
        self.ventana.mainloop()

#Clase encargada de modificar los datos de un usuario
class ModificarDatos(ctk.CTkFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # Label for numero de cedula
        self.label_cedula = ctk.CTkLabel(self, text="Ingrese el número de cédula del usuario:")
        self.label_cedula.grid(row=0, column=0, pady=10)

        # Entry for numero de cedula with validation
        vcmd = (self.register(self.validate_numeric), '%S')
        self.entry_cedula = ctk.CTkEntry(self, validate='key', validatecommand=vcmd)
        self.entry_cedula.grid(row=0, column=1, padx=10, pady=10)

        # Botón Buscar
        self.boton_buscar = ctk.CTkButton(self, text="Buscar", command=self.buscar_click)
        self.boton_buscar.grid(row=0, column=2, padx=10, pady=10)

        # Botón Habilitar (initially hidden)
        self.boton_habilitar = ctk.CTkButton(self, text="Habilitar", command=self.toggle_habilitar)
        self.boton_habilitar.grid(row=0, column=3, padx=10, pady=10)
        self.boton_habilitar.grid_remove()

        # User data fields (initially hidden)
        self.label_usuario = ctk.CTkLabel(self, text="Nombre de usuario:")
        self.label_usuario.grid(row=1, column=0, pady=5)
        self.label_usuario.grid_remove()
        self.entry_usuario = ctk.CTkEntry(self, state='readonly')
        self.entry_usuario.grid(row=1, column=1, pady=5)
        self.entry_usuario.grid_remove()

        self.label_password = ctk.CTkLabel(self, text="Contraseña:")
        self.label_password.grid(row=2, column=0, pady=5)
        self.label_password.grid_remove()
        self.entry_password = ctk.CTkEntry(self, state='readonly')
        self.entry_password.grid(row=2, column=1, pady=5)
        self.entry_password.grid_remove()

        self.label_nombre = ctk.CTkLabel(self, text="Nombre:")
        self.label_nombre.grid(row=3, column=0, pady=5)
        self.label_nombre.grid_remove()
        self.entry_nombre = ctk.CTkEntry(self, state='readonly')
        self.entry_nombre.grid(row=3, column=1, pady=5)
        self.entry_nombre.grid_remove()

        self.label_apellido = ctk.CTkLabel(self, text="Apellido:")
        self.label_apellido.grid(row=4, column=0, pady=5)
        self.label_apellido.grid_remove()
        self.entry_apellido = ctk.CTkEntry(self, state='readonly')
        self.entry_apellido.grid(row=4, column=1, pady=5)
        self.entry_apellido.grid_remove()

        self.label_cedula = ctk.CTkLabel(self, text="Cédula:")
        self.label_cedula.grid(row=5, column=0, pady=5)
        self.label_cedula.grid_remove()
        self.entry_cedula = ctk.CTkEntry(self, state='readonly')
        self.entry_cedula.grid(row=5, column=1, pady=5)
        self.entry_cedula.grid_remove()

        self.label_telefono = ctk.CTkLabel(self, text="Número de Teléfono:")
        self.label_telefono.grid(row=6, column=0, pady=5)
        self.label_telefono.grid_remove()
        self.entry_telefono = ctk.CTkEntry(self, state='readonly')
        self.entry_telefono.grid(row=6, column=1, pady=5)
        self.entry_telefono.grid_remove()

        self.label_ficha = ctk.CTkLabel(self, text="Número de ficha:")
        self.label_ficha.grid(row=7, column=0, pady=5)
        self.label_ficha.grid_remove()
        self.entry_ficha = ctk.CTkEntry(self, state='readonly')
        self.entry_ficha.grid(row=7, column=1, pady=5)
        self.entry_ficha.grid_remove()

        self.label_tipo_usuario = ctk.CTkLabel(self, text="Tipo de usuario:")
        self.label_tipo_usuario.grid(row=8, column=0, pady=5)
        self.label_tipo_usuario.grid_remove()
        values = ["Administrador", "Asistente"]
        self.combo_tipo_usuario = ctk.CTkComboBox(self, values=values, state='readonly')
        self.combo_tipo_usuario.grid(row=8, column=1, pady=5)
        self.combo_tipo_usuario.grid_remove()

        # Botón Actualizar (initially hidden)
        self.boton_actualizar = ctk.CTkButton(self, text="Actualizar", command=self.actualizar_usuario)
        self.boton_actualizar.grid(row=9, column=0, columnspan=3, pady=20)
        self.boton_actualizar.grid_remove()

    def validate_numeric(self, value_if_allowed):
        if value_if_allowed.isdigit() or value_if_allowed == "":
            return True
        else:
            return False

    def buscar_click(self):
        # Validar si el campo de cédula está vacío
        #if not self.entry_cedula.get():
        #    messagebox.showwarning("Error", "Por favor, ingrese el número de cédula.")
        #    return

        # Aquí se debe buscar el usuario en la base de datos
        # Si el usuario es encontrado, mostrar el botón Habilitar
        self.boton_habilitar.grid()
        self.mostrar_elementos()

    def mostrar_elementos(self):
        # Mostrar los campos de datos del usuario y el botón Actualizar
        self.label_usuario.grid()
        self.entry_usuario.grid()
        self.label_password.grid()
        self.entry_password.grid()
        self.label_nombre.grid()
        self.entry_nombre.grid()
        self.label_apellido.grid()
        self.entry_apellido.grid()
        self.label_cedula.grid()
        self.entry_cedula.grid()
        self.label_telefono.grid()
        self.entry_telefono.grid()
        self.label_ficha.grid()
        self.entry_ficha.grid()
        self.label_tipo_usuario.grid()
        self.combo_tipo_usuario.grid()
        self.boton_actualizar.grid()

    def toggle_habilitar(self):
        # Toggle the state of the entries and the button text
        if self.entry_usuario.cget('state') == 'readonly':
            self.entry_usuario.configure(state='normal')
            self.entry_password.configure(state='normal')
            self.entry_nombre.configure(state='normal')
            self.entry_apellido.configure(state='normal')
            self.entry_cedula.configure(state='normal')
            self.entry_telefono.configure(state='normal')
            self.entry_ficha.configure(state='normal')
            self.combo_tipo_usuario.configure(state='normal')
            self.boton_habilitar.configure(text="Deshabilitar")
        else:
            self.entry_usuario.configure(state='readonly')
            self.entry_password.configure(state='readonly')
            self.entry_nombre.configure(state='readonly')
            self.entry_apellido.configure(state='readonly')
            self.entry_cedula.configure(state='readonly')
            self.entry_telefono.configure(state='readonly')
            self.entry_ficha.configure(state='readonly')
            self.combo_tipo_usuario.configure(state='readonly')
            self.boton_habilitar.configure(text="Habilitar")

    def actualizar_usuario(self):
        # Validar si algún campo está vacío
        if not self.entry_usuario.get() or not self.entry_password.get() or not self.entry_nombre.get() or not self.entry_apellido.get() or not self.entry_cedula.get() or not self.entry_telefono.get() or not self.entry_ficha.get() or not self.combo_tipo_usuario.get():
            messagebox.showwarning("Error", "Por favor, completa todos los campos.")
            return

        # Aquí se debe agregar la lógica para actualizar los datos del usuario
        pass

#Clase encargada de recuperar los datos de un usuario
class RecuperarDatosApp(ctk.CTkFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # Label for numero de cedula
        self.label_cedula = ctk.CTkLabel(self, text="Ingrese el número de cédula del usuario:")
        self.label_cedula.pack(pady=10)

        # Entry for numero de cedula with validation
        vcmd = (self.register(self.validate_numeric), '%P')
        self.entry_cedula = ctk.CTkEntry(self, width=150, validate='key', validatecommand=vcmd)
        self.entry_cedula.pack(pady=10)

        # Botón Buscar
        self.boton_buscar = ctk.CTkButton(self, text="Buscar", command=self.buscar_click)
        self.boton_buscar.pack(pady=10)

    def validate_numeric(self, value_if_allowed):
        if value_if_allowed.isdigit() or value_if_allowed == "":
            return True
        else:
            return False

    def buscar_click(self):
        numero_cedula = self.entry_cedula.get()
        if not numero_cedula:
            messagebox.showwarning("Error", "Por favor, ingrese el número de cédula.")
            return
            
        # Aquí se debe buscar el usuario en la base de datos
        # y mostrar su usuario y contraseña en un messagebox
        usernarme = "Magleo"
        password = "1234"
        messagebox.showinfo(f"Resultado", "Usuario: "+usernarme+"\n\nContraseña: "+password)

    def iniciar(self):
        self.ventana.mainloop()

class EliminarUsuario(RecuperarDatosApp):
    def __init__(self, parent=None):
        super().__init__(parent)

    def buscar_click(self):
        numero_cedula = self.entry_cedula.get()
        if not numero_cedula:
            messagebox.showwarning("Error", "Por favor, ingrese el número de cédula.")
            return

        respuesta = messagebox.askyesno("Confirmación", f"¿Estás seguro que deseas eliminar a {numero_cedula}?")
        if respuesta:
            # Aquí se debe eliminar el usuario en la base de datos
            messagebox.showinfo("Resultado", "Usuario eliminado exitosamente.")
        else:
            messagebox.showinfo("Resultado", "Eliminación cancelada.")
