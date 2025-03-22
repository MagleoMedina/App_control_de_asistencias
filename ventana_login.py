import customtkinter as ctk
from tkinter import messagebox

class VentanaLogin:
    def __init__(self):
        # Crear la ventana principal
        self.ventana = ctk.CTk()
        self.ventana.title("Login")
        self.ventana.geometry("1280x720")

        # Configuración del contenedor principal
        self.frame_principal = ctk.CTkFrame(self.ventana)
        self.frame_principal.place(relx=0.5, rely=0.5, anchor='center')  # Centrar el frame

        # Etiqueta y campo de entrada para el nombre de usuario
        self.label_usuario = ctk.CTkLabel(self.frame_principal, text="Usuario:")
        self.label_usuario.grid(row=0, column=0, pady=5, sticky='w')
        self.entry_usuario = ctk.CTkEntry(self.frame_principal, width=120)
        self.entry_usuario.grid(row=0, column=1, pady=5, sticky='w')

        # Etiqueta para la contraseña
        self.label_password = ctk.CTkLabel(self.frame_principal, text="Contraseña:")
        self.label_password.grid(row=1, column=0, pady=5, sticky='w')

        # Frame para la contraseña y el botón de mostrar/ocultar
        self.frame_password = ctk.CTkFrame(self.frame_principal)
        self.frame_password.grid(row=1, column=1, pady=5, sticky='w')  # Alineado a la izquierda

        # Campo de entrada para la contraseña con tamaño uniforme
        self.entry_password = ctk.CTkEntry(self.frame_password, show="*", width=120)  # Ajusta el tamaño del campo
        self.entry_password.pack(side=ctk.LEFT)

        # Botón para mostrar/ocultar contraseña
        self.boton_mostrar_ocultar = ctk.CTkButton(self.frame_password, text="mostrar", command=self.mostrar_ocultar_password)
        self.boton_mostrar_ocultar.pack(side=ctk.LEFT, padx=(25, 0))  # Desplazado un poco a la derecha

        # Frame para colocar los botones lado a lado
        self.frame_botones = ctk.CTkFrame(self.frame_principal)
        self.frame_botones.grid(row=2, column=0, columnspan=2, pady=15)  # Ajustado a dos columnas

        # Botón para ingresar
        self.boton_ingresar = ctk.CTkButton(self.frame_botones, text="Ingresar", command=self.ingresar)
        self.boton_ingresar.grid(row=0, column=0, padx=10)

        # Variable para controlar la visibilidad de la contraseña
        self.password_visible = False

    def mostrar_ocultar_password(self):
        """Función para mostrar u ocultar la contraseña."""
        if self.password_visible:
            self.entry_password.configure(show="*")  # Ocultar la contraseña
            self.boton_mostrar_ocultar.configure(text="mostrar")  # Cambiar el símbolo a 'ocultar'
        else:
            self.entry_password.configure(show="")  # Mostrar la contraseña
            self.boton_mostrar_ocultar.configure(text="ocultar")  # Cambiar el símbolo a 'mostrar'
        self.password_visible = not self.password_visible  # Cambiar el estado

    def ingresar(self):
        """Función que se ejecuta al hacer clic en el botón 'Ingresar'."""
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()

        if usuario and password:
            self.ventana.withdraw()  # Terminate the mainloop  
            self.ventana.quit()         
            from ventana_main import VentanaMain
            main = VentanaMain()
            main.iniciar()
        else:
            messagebox.showwarning("Error", "Por favor, completa todos los campos.")

    
    def iniciar(self):
        """Inicia el bucle principal de la ventana."""
        self.ventana.mainloop()

