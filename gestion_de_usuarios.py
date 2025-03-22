import customtkinter as ctk
from tkinter import messagebox

#Clase encargada de registrar nuevos usuarios
class VentanaRegistro(ctk.CTkFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

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
        values = ["Administrador", "Asistente"]# Esta data debe de recuperarse de la BD de la tabla Tipo
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
            # Mostrar un mensaje de confirmación con los datos ingresados
            messagebox.showinfo("Registro exitoso", "Usuario registrado exitosamente.")
        
    def solo_numeros(self, char):
        """Validación para aceptar solo caracteres numéricos."""
        return char.isdigit()   

    def iniciar(self):
        """Inicia el bucle principal de la ventana."""
        self.ventana.mainloop()

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
        # Aquí se debe buscar el usuario en la base de datos
        # y mostrar su usuario y contraseña en un messagebox
        usernarme = "Magleo"
        password = "1234"
        messagebox.showinfo(f"Resultado", "Usuario: "+usernarme+"\n\nContraseña: "+password)

    def iniciar(self):
        self.ventana.mainloop()
