import customtkinter as ctk
from tkinter import messagebox


class VentanaRegistro:
    def __init__(self):
        # Crear la ventana principal
        self.ventana = ctk.CTk()
        self.ventana.title("Registro de Usuario")
        
        # Configuración del tamaño de la ventana
        self.ventana.geometry("1280x720")


        # Frame principal que contendrá todos los campos del formulario
        self.frame_formulario = ctk.CTkFrame(self.ventana)
        self.frame_formulario.place(relx=0.5, rely=0.5, anchor='center')  # Ubicar en el centro

        # Nombre de usuario
        self.label_usuario = ctk.CTkLabel(self.frame_formulario, text="Nombre de Usuario:")
        self.label_usuario.grid(row=0, column=0, sticky='w', pady=5)
        self.entry_usuario = ctk.CTkEntry(self.frame_formulario)
        self.entry_usuario.grid(row=0, column=1, pady=5)

        # Contraseña
        self.label_password = ctk.CTkLabel(self.frame_formulario, text="Contraseña:")
        self.label_password.grid(row=1, column=0, sticky='w', pady=5)
        self.entry_password = ctk.CTkEntry(self.frame_formulario, show="*")
        self.entry_password.grid(row=1, column=1, pady=5)

        # Nombre
        self.label_nombre = ctk.CTkLabel(self.frame_formulario, text="Nombre:")
        self.label_nombre.grid(row=2, column=0, sticky='w', pady=5)
        self.entry_nombre = ctk.CTkEntry(self.frame_formulario)
        self.entry_nombre.grid(row=2, column=1, pady=5)

        # Apellido
        self.label_apellido = ctk.CTkLabel(self.frame_formulario, text="Apellido:")
        self.label_apellido.grid(row=3, column=0, sticky='w', pady=5)
        self.entry_apellido = ctk.CTkEntry(self.frame_formulario)
        self.entry_apellido.grid(row=3, column=1, pady=5)

        # Validación para permitir solo números
        validate_numeric = self.ventana.register(self.solo_numeros)


        # Cédula
        self.label_cedula = ctk.CTkLabel(self.frame_formulario, text="Cédula:")
        self.label_cedula.grid(row=4, column=0, sticky='w', pady=5)
        self.entry_cedula = ctk.CTkEntry(self.frame_formulario, validate="key", validatecommand=(validate_numeric, '%S'))
        self.entry_cedula.grid(row=4, column=1, pady=5)

        # Número de teléfono
        self.label_telefono = ctk.CTkLabel(self.frame_formulario, text="Número de Teléfono:")
        self.label_telefono.grid(row=5, column=0, sticky='w', pady=5)
        self.entry_telefono = ctk.CTkEntry(self.frame_formulario, validate="key", validatecommand=(validate_numeric, '%S'))
        self.entry_telefono.grid(row=5, column=1, pady=5)

        # Número de ficha de trabajador
        self.label_ficha = ctk.CTkLabel(self.frame_formulario, text="Número de Ficha de Trabajador:")
        self.label_ficha.grid(row=6, column=0, sticky='w', pady=5)
        self.entry_ficha = ctk.CTkEntry(self.frame_formulario, validate="key", validatecommand=(validate_numeric, '%S'))
        self.entry_ficha.grid(row=6, column=1, pady=5)

        # Preguntas de seguridad
        self.label_preguntas_seguridad = ctk.CTkLabel(self.frame_formulario, text="Preguntas de Seguridad", font=("Arial", 12, "bold"))
        self.label_preguntas_seguridad.grid(row=7, column=0, columnspan=2, pady=10)

        # Respuesta a la primera pregunta de seguridad
        pregunta_1 = "¿Cuál es el nombre de tu mascota?"
        self.label_respuesta1 = ctk.CTkLabel(self.frame_formulario, text = pregunta_1)
        self.label_respuesta1.grid(row=8, column=0, sticky='w', pady=5)
        self.entry_respuesta1 = ctk.CTkEntry(self.frame_formulario)
        self.entry_respuesta1.grid(row=8, column=1, pady=5)

        # Respuesta a la segunda pregunta de seguridad
        pregunta_2 = "¿Cuál es tu color favorito?"
        self.label_respuesta2 = ctk.CTkLabel(self.frame_formulario, text = pregunta_2)
        self.label_respuesta2.grid(row=9, column=0, sticky='w', pady=5)
        self.entry_respuesta2 = ctk.CTkEntry(self.frame_formulario)
        self.entry_respuesta2.grid(row=9, column=1, pady=5)

        # Respuesta a la tercera pregunta de seguridad
        pregunta_3 = "¿En qué ciudad naciste?"
        self.label_respuesta3 = ctk.CTkLabel(self.frame_formulario, text = pregunta_3)
        self.label_respuesta3.grid(row=10, column=0, sticky='w', pady=5)
        self.entry_respuesta3 = ctk.CTkEntry(self.frame_formulario)
        self.entry_respuesta3.grid(row=10, column=1, pady=5)

        # Botón de registro
        self.boton_registro = ctk.CTkButton(self.frame_formulario, text="Registrar", command=self.registrar_usuario)
        self.boton_registro.grid(row=11, column=0, pady=20, sticky='e', padx=10)  # Ubicar en la columna 0

        # Botón "Atrás"
        self.boton_atras = ctk.CTkButton(self.frame_formulario, text="Atrás", command=self.volver_atras)
        self.boton_atras.grid(row=11, column=1, pady=20, sticky='w')  # Ubicar en la columna 1

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
            "Respuesta 1": self.entry_respuesta1.get(),
            "Respuesta 2": self.entry_respuesta2.get(),
            "Respuesta 3": self.entry_respuesta3.get(),
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
    
    def volver_atras(self):
        self.ventana.withdraw()
        self.ventana.quit()
        from ventana_login import VentanaLogin
        logeo = VentanaLogin()
        logeo.iniciar()

    def iniciar(self):
        """Inicia el bucle principal de la ventana."""
        self.ventana.mainloop()