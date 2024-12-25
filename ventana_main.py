import customtkinter as ctk
from tkinter import messagebox
from carga_asistencia import CargaAsistencia  
from carga_asistencia_estudiantes import AnalizadorPDF  # Import the new class

class VentanaMain:
    def __init__(self):
        # Crear una instancia de la ventana principal
        self.ventana = ctk.CTk()
        self.ventana.geometry("1280x720")
        self.ventana.title("SASE")

        # Crear un frame principal que ocupa toda la ventana
        self.main_frame = ctk.CTkFrame(self.ventana, fg_color="gray20")  # Fondo gris oscuro
        self.main_frame.pack(fill="both", expand=True)  # Usa todo el espacio disponible

        # Label con el nombre de usuario
        username = "Magleo"  # Aquí se debe recuperar la info del usuario que se logueó
        label = ctk.CTkLabel(self.main_frame, text="Bienvenido " + username, font=("Arial", 18))
        label.pack(pady=20)

        # Crear un frame para los botones en una fila horizontal
        frame_botones = ctk.CTkFrame(self.main_frame, fg_color="transparent")  # Fondo transparente
        frame_botones.pack(pady=20)

        # Botones de opciones en fila horizontal
        boton_carga_asistencia = ctk.CTkButton(frame_botones, text="Carga de Asistencia", width=25, command=self.carga_asistencia)
        boton_carga_asistencia.pack(side=ctk.LEFT, padx=10)
        
        boton_carga_asistencia_estudiantes = ctk.CTkButton(frame_botones, text="Carga de Asistencia estudiantes", width=25, command=self.carga_asistencia_estudiantes)
        boton_carga_asistencia_estudiantes.pack(side=ctk.LEFT, padx=10)

        boton_consultar_asistencia = ctk.CTkButton(frame_botones, text="Consultar Asistencia", width=25, command=self.consultar_asistencia)
        boton_consultar_asistencia.pack(side=ctk.LEFT, padx=10)

        boton_consultar_falla = ctk.CTkButton(frame_botones, text="Consultar Falla de Computador", width=25, command=self.consultar_falla)
        boton_consultar_falla.pack(side=ctk.LEFT, padx=10)

        boton_modulo_estadistico = ctk.CTkButton(frame_botones, text="Módulo Estadístico", width=25, command=self.modulo_estadistico)
        boton_modulo_estadistico.pack(side=ctk.LEFT, padx=10)

        # Botón para cerrar la sesión
        boton_cerrar = ctk.CTkButton(self.main_frame, text="Cerrar sesion", command=self.cerrar)
        boton_cerrar.pack(pady=10)

        # Frame para mostrar el formulario de asistencia
        self.frame_formulario = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_formulario.pack(fill="both", expand=True, pady=20)

    def limpiar_frame(self):
        # Limpiar el frame antes de mostrar el formulario de asistencia
        for widget in self.frame_formulario.winfo_children():
            widget.destroy()

    def carga_asistencia(self):
        self.limpiar_frame()
        app = CargaAsistencia(self.frame_formulario)
        app.pack(fill="both", expand=True)

    def carga_asistencia_estudiantes(self):
        self.limpiar_frame()
        app = AnalizadorPDF(self.frame_formulario)
        app.pack(fill="both", expand=True)

    def consultar_asistencia(self):
        self.limpiar_frame()
        messagebox.showinfo("Consultar Asistencia", "Funcionalidad en desarrollo")

    def consultar_falla(self):
        self.limpiar_frame()
        messagebox.showinfo("Consultar Falla de Computador", "Funcionalidad en desarrollo")

    def modulo_estadistico(self):
        self.limpiar_frame()
        messagebox.showinfo("Módulo Estadístico", "Funcionalidad en desarrollo")

    def iniciar(self):
        self.ventana.mainloop()

    def cerrar(self):
        # Cerrar la ventana y volver al login 
        self.ventana.withdraw()
        self.ventana.quit()
        from ventana_login import VentanaLogin
        ventana_login = VentanaLogin()
        ventana_login.iniciar()
