import customtkinter as ctk
from tkinter import messagebox
from db_manager import DBManager

class VentanaLogin:
    def __init__(self):
        # Crear la ventana principal
        self.ventana = ctk.CTk()
        self.ventana.title("Login")
        self.ventana.geometry("1280x720+10+10")
        ctk.set_appearance_mode("light")
        self.db = DBManager()  # Conexión a la BD
        self.db.set_parent(self.ventana) 
        
        # Configuración del contenedor principal
        self.frame_principal = ctk.CTkFrame(self.ventana,fg_color="gray99",border_width=3, border_color="DeepSkyBlue2",height=400)
        self.frame_principal.place(relx=0.5, rely=0.5, anchor='center')  # Centrar el frame

        # Etiqueta y campo de entrada para el nombre de usuario
        self.label_usuario = ctk.CTkLabel(self.frame_principal, text="  Usuario:",font=("Century Gothic", 14))
        self.label_usuario.grid(row=0, column=0, pady=10,padx=5, sticky='w')
        self.entry_usuario = ctk.CTkEntry(self.frame_principal, width=200,placeholder_text="Nombre de Usuario",font=("Century Gothic", 14),corner_radius=10,border_color="light blue")
        self.entry_usuario.grid(row=1, column=0,padx=5, sticky='w')

         # Etiqueta para la contraseña
        self.label_password = ctk.CTkLabel(self.frame_principal, text="   Contraseña:", font=("Century Gothic", 14))
        self.label_password.grid(row=2, column=0, pady=5,padx=5, sticky='w')

         # Campo de entrada para la contraseña con tamaño uniforme
        self.entry_password = ctk.CTkEntry(self.frame_principal, show="*", width=200,corner_radius=10,border_color="light blue")  # Ajusta el tamaño del campo
        self.entry_password.grid(row=3, column=0,columnspan=1, padx=5, pady=5)
        
        # Agregar eventos para hover en usuario
        self.entry_usuario.bind("<Enter>", lambda event: self.on_hover(event, self.entry_usuario))
        self.entry_usuario.bind("<Leave>", lambda event: self.off_hover(event, self.entry_usuario))

        # Agregar eventos para hover en contraseña
        self.entry_password.bind("<Enter>", lambda event: self.on_hover(event, self.entry_password))
        self.entry_password.bind("<Leave>", lambda event: self.off_hover(event, self.entry_password))
        # Botón para mostrar/ocultar contraseña
        self.boton_mostrar_ocultar = ctk.CTkButton(self.frame_principal, text="mostrar", command=self.mostrar_ocultar_password,width=70,  # Color de fondo del botón
        fg_color="dodger blue",
        hover_color="deep sky blue",  # Color cuando pasas el mouse
        border_color="#ffffff",  # Color del borde
        border_width=2,  # Grosor del borde
        text_color="#ffffff" ,font=("Century Gothic", 14,"bold"),corner_radius=20 )
        self.boton_mostrar_ocultar.grid(row=3, column=1, padx=5, pady=5)  # Desplazado un poco a la derecha

        # Frame para colocar los botones lado a lado
        self.frame_botones = ctk.CTkFrame(self.frame_principal,fg_color="gray99")
        self.frame_botones.grid(row=5, column=0, columnspan=2, pady=15)  # Ajustado a dos columnas

        # Botón para ingresar
        self.boton_ingresar = ctk.CTkButton(self.frame_botones, text="Ingresar", command=self.ingresar,fg_color="dodger blue",
        hover_color="deep sky blue",  # Color cuando pasas el mouse
        border_color="#ffffff",  # Color del borde
        border_width=2,  # Grosor del borde
        text_color="#ffffff" ,font=("Century Gothic", 14,"bold"),corner_radius=20)
        self.boton_ingresar.grid(row=0, column=0, padx=10)

        # Variable para controlar la visibilidad de la contraseña
        self.password_visible = False
    
    # Cambia el color cuando el mouse entra
    def on_hover(self, event, widget):
     widget.configure(border_color="light sky blue")

    def off_hover(self, event, widget):
     widget.configure(border_color="light blue")

    

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

        if not usuario or not password:
            messagebox.showwarning("Error", "Por favor, completa todos los campos.")
            return

        # Consulta a la base de datos
        user_data = self.db.autenticar_usuario(usuario, password)

        if user_data:
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            
            for task in self.ventana.tk.call('after', 'info'):
                try:
                    self.ventana.after_cancel(task)
                except Exception:
                    pass

            self.ventana.destroy()  
            
            # Se importa aquí para evitar dependencias circulares
            from Views.ventana_main import VentanaMainAdmin, VentanaMain

            if user_data["Tipo_usuario"].lower() == "administrador":
                app = VentanaMainAdmin(user_data)
            else:
                app = VentanaMain(user_data)

            app.iniciar()

        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
    
    def iniciar(self):
        """Inicia el bucle principal de la ventana."""
        self.ventana.mainloop()