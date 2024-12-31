import customtkinter as ctk
from tkinter import messagebox
from carga_asistencia import CargaAsistencia
from carga_asistencia_estudiantes import AnalizadorPDF

class VentanaMain:
    def __init__(self):
        # Crear una instancia de la ventana principal
        self.ventana = ctk.CTk()
        self.ventana.geometry("1280x720")
        self.ventana.title("SASE")

        # Configuración del grid principal
        self.ventana.grid_columnconfigure(1, weight=1)
        self.ventana.grid_rowconfigure(0, weight=1)

        # Panel de Navegación
        self.nav_frame = ctk.CTkFrame(self.ventana, width=200, fg_color="gray20")
        self.nav_frame.grid(row=0, column=0, rowspan=2, sticky="nsw", padx=10, pady=10)

        self.nav_label = ctk.CTkLabel(self.nav_frame, text="SASE", font=("Arial", 20, "bold"), text_color="white")
        self.nav_label.pack(pady=10)

        # Botones del Panel de Navegación
        botones_nav = [
            ("Carga de Asistencia", "📝", self.carga_asistencia),
            ("Carga de Asistencia Estudiantes", "👨‍🎓", self.carga_asistencia_estudiantes),
            ("Consultar Asistencia", "🔍", self.consultar_asistencia),
            ("Consultar Falla de Computador", "💻", self.consultar_falla),
            ("Módulo Estadístico", "📊", self.modulo_estadistico),
            ("Cerrar Sesión", "🚪", self.cerrar)
        ]

        for texto, icono, command in botones_nav:
            boton = ctk.CTkButton(self.nav_frame, text=f"{icono} {texto}", width=180, command=command)
            boton.pack(pady=5)
        
        username = "Magleo"  # Aquí se debe recuperar la info del usuario que se logueó
        self.nav_label_user = ctk.CTkLabel(self.nav_frame, text="Bienvenido "+ username, font=("Arial", 20, "bold"), text_color="white")
        self.nav_label_user.pack(pady=10)


        # Frame principal para mostrar las vistas
        self.main_frame = ctk.CTkFrame(self.ventana, fg_color="gray20")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
       
    def limpiar_frame(self):
        # Limpiar el frame antes de mostrar el formulario de asistencia
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def carga_asistencia(self):
        self.limpiar_frame()
        app = CargaAsistencia(self.main_frame)
        app.pack(fill="both", expand=True)

    def carga_asistencia_estudiantes(self):
        self.limpiar_frame()
        app = AnalizadorPDF(self.main_frame)
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
        ventana_login