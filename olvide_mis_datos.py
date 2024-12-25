import customtkinter as ctk
from tkinter import messagebox

class RecuperarDatosApp:
    def __init__(self):
        self.ventana = ctk.CTk()
        self.ventana.title("Recuperar Datos")

        self.ventana.geometry("1280x720")


        # Botón en la esquina superior izquierda
        self.atras = ctk.CTkButton(self.ventana, text="Atrás", command=self.atras_click)
        self.atras.place(x=10, y=10)

        # Crear un frame para centrar el contenido
        self.frame = ctk.CTkFrame(self.ventana)
        self.frame.place(relx=0.5, rely=0.5, anchor='center')  # Centrar el frame

        # Variable para almacenar la selección
        self.seleccion = ctk.StringVar(value="")  # Inicialmente ninguna opción seleccionada

        # Frame para los radiobuttons
        self.frame_opciones = ctk.CTkFrame(self.frame)
        self.frame_opciones.pack(pady=10)

        # Lista de opciones
        opciones = ["Olvidé mi usuario", "Olvidé mi contraseña"]
        for opcion in opciones:
            ctk.CTkRadioButton(self.frame_opciones, text=opcion, variable=self.seleccion, value=opcion, command=self.mostrar_opcion).pack(side='left', padx=20)

        # Entry for numero de cedula
        self.label_cedula = ctk.CTkLabel(self.frame, text="Ingrese su número de cédula:")
        vcmd = (self.ventana.register(self.validate_numeric), '%P')
        self.entry_cedula = ctk.CTkEntry(self.frame, width=30, validate='key', validatecommand=vcmd)

        # Entries for username and security questions
        self.label_username = ctk.CTkLabel(self.frame, text="Ingrese su username:")
        self.entry_username = ctk.CTkEntry(self.frame, width=30)
        self.label_pregunta1 = ctk.CTkLabel(self.frame, text="Pregunta de seguridad 1:")
        self.entry_pregunta1 = ctk.CTkEntry(self.frame, width=30)
        self.label_pregunta2 = ctk.CTkLabel(self.frame, text="Pregunta de seguridad 2:")
        self.entry_pregunta2 = ctk.CTkEntry(self.frame, width=30)
        self.label_pregunta3 = ctk.CTkLabel(self.frame, text="Pregunta de seguridad 3:")
        self.entry_pregunta3 = ctk.CTkEntry(self.frame, width=30)

        # Crear un frame para los botones
        self.frame_botones = ctk.CTkFrame(self.frame)

        # Add a button to submit the selection
        self.boton_enviar = ctk.CTkButton(self.frame_botones, text="Enviar", command=self.enviar_seleccion)
        #self.boton_cancelar = ctk.CTkButton(self.frame_botones, text="Cancelar", command=self.ventana.quit)

    def mostrar_opcion(self):
        seleccion = self.seleccion.get()
        if seleccion == "Olvidé mi usuario":
            self.label_cedula.pack(pady=10)
            self.entry_cedula.pack(pady=10)
            self.hide_password_recovery_fields()
            self.frame_botones.pack(pady=5)
            self.boton_enviar.pack(side='left', padx=10)
           # self.boton_cancelar.pack(side='right', padx=10)
        elif seleccion == "Olvidé mi contraseña":
            self.label_username.pack(pady=10)
            self.entry_username.pack(pady=10)
            self.label_pregunta1.pack(pady=10)
            self.entry_pregunta1.pack(pady=10)
            self.label_pregunta2.pack(pady=10)
            self.entry_pregunta2.pack(pady=10)
            self.label_pregunta3.pack(pady=10)
            self.entry_pregunta3.pack(pady=10)
            self.hide_user_recovery_fields()
            self.frame_botones.pack(pady=5)
            self.boton_enviar.pack(side='left', padx=10)
           # self.boton_cancelar.pack(side='right', padx=10)
        else:
            self.hide_user_recovery_fields()
            self.hide_password_recovery_fields()
            self.frame_botones.pack_forget()
            self.boton_enviar.pack_forget()
           # self.boton_cancelar.pack_forget()

    def hide_user_recovery_fields(self):
        self.label_cedula.pack_forget()
        self.entry_cedula.pack_forget()

    def hide_password_recovery_fields(self):
        self.label_username.pack_forget()
        self.entry_username.pack_forget()
        self.label_pregunta1.pack_forget()
        self.entry_pregunta1.pack_forget()
        self.label_pregunta2.pack_forget()
        self.entry_pregunta2.pack_forget()
        self.label_pregunta3.pack_forget()
        self.entry_pregunta3.pack_forget()

    def enviar_seleccion(self):
        seleccion = self.seleccion.get()
        if seleccion == "Olvidé mi usuario":
            numero_cedula = self.entry_cedula.get()
            # Aquí se debería implementar la lógica para obtener el username basado en el número de cédula
            # Por ahora, simplemente mostramos un mensaje de ejemplo
            username = "usuario_ejemplo"  # Este valor debería ser obtenido de una base de datos o similar
            messagebox.showinfo("Resultado", f"Su username es: {username}")
        elif seleccion == "Olvidé mi contraseña":
            username = self.entry_username.get()
            pregunta1 = self.entry_pregunta1.get()
            pregunta2 = self.entry_pregunta2.get()
            pregunta3 = self.entry_pregunta3.get()
            # Aquí se debería implementar la lógica para verificar las respuestas de seguridad
            # Por ahora, simplemente mostramos un mensaje de ejemplo
            messagebox.showinfo("Resultado", "Las respuestas de seguridad han sido verificadas.")
        else:
            pass

    def validate_numeric(self, value_if_allowed):
        if value_if_allowed.isdigit() or value_if_allowed == "":
            return True
        else:
            return False

    def atras_click(self):
        from ventana_login import VentanaLogin
        self.ventana.withdraw()
        self.ventana.quit()
        app = VentanaLogin()
        app.iniciar()        

    def iniciar(self):
        self.ventana.mainloop()

