import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image  # Necesario para manejar imágenes
from Views.carga_asistencia import CargaAsistencia
from Views.carga_asistencia_estudiantes import CargaAsistenciaEstudiantes
from Views.consultar_asistencia import ConsultarAsistencia
from Views.modulo_estadistico import ModuloEstadistico
from Views.equipos import Equipos
from Views.gestion_de_usuarios import GestionUsuarios
from Views.eliminar_datos import EliminarDatos

class VentanaMain:
    def __init__(self, user_data):
        self.user_data = user_data
        # Crear una instancia de la ventana principal
        self.ventana = ctk.CTk()
        self.ventana.geometry("1280x720+10+10")
        self.ventana.title("SALU")
        ctk.set_appearance_mode("light")
    
        
        # Crear un Canvas para el gradiente
        self.canvas = tk.Canvas(self.ventana, highlightthickness=0)
        self.canvas.place(relwidth=1, relheight=1)  # Cubre toda la ventana

        # Definir colores del gradiente (azul claro a blanco)
        self.color1 = "#4B9CD3"  # Azul claro
        self.color2 = "#FFFFFF"  # Blanco
        
        # Dibujar gradiente inicial
        self.dibujar_gradiente()
        
        # Vincular el evento de redimensionamiento
        self.ventana.bind("<Configure>", lambda e: self.dibujar_gradiente())
        
        # Configuración del contenedor principal, donde estan los logos
        self.header_frame = ctk.CTkFrame(self.ventana, height=50, fg_color="gray99")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Configuración del grid principal
        self.ventana.grid_columnconfigure(0, weight=0)  # Columna 0 (nav_frame) - ancho fijo
        self.ventana.grid_columnconfigure(1, weight=1)  # Columna 1 (main_frame) - se expande
        self.ventana.grid_rowconfigure(1, weight=1)     # Fila 1 (nav_frame + main_frame) - se expande
       
        # Frame superior (encabezado) 
        self.header_frame = ctk.CTkFrame(
            self.ventana, 
            height=50, 
            fg_color="gray99", 
        )
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.header_frame.grid_propagate(False) 
        
        # Configuración del grid del header_frame para que el logo derecho quede fijo
        self.header_frame.grid_columnconfigure(0, weight=0)  # Logo UNEG (ancho fijo)
        self.header_frame.grid_columnconfigure(1, weight=0)  # Label "UNEG" (ancho fijo)
        self.header_frame.grid_columnconfigure(2, weight=1)  
        self.header_frame.grid_columnconfigure(3, weight=0)  
        self.header_frame.grid_columnconfigure(4, weight=0)  # Logo CL 


        # Cargar la imagen LOGO DE LA UNEG usando una ruta compatible con PyInstaller
        import os, sys
        if hasattr(sys, '_MEIPASS'):
            img_path = os.path.join(sys._MEIPASS, 'assets', 'logo_uneg.png')
        else:
            img_path = os.path.join('assets','logo_uneg.png')
        imagen_logo = Image.open(img_path)
        tamaño_imagen = (42, 42)
        imagen_redimensionada = imagen_logo.resize(tamaño_imagen)

        self.logo_ctk = ctk.CTkImage(
            light_image=imagen_redimensionada,
            dark_image=imagen_redimensionada,  
            size=tamaño_imagen
        )

        self.label_imagen = ctk.CTkLabel(
            self.header_frame,
            image=self.logo_ctk,
            text=""  # Texto vacío para que solo muestre la imagen
        )
        self.label_imagen.grid(row=0, column=0, padx=10, pady=5,sticky="w")  # Posición izquierda


        # Label del encabezado - pady reducido para disminuir espacio vertical
        self.Uneg_label = ctk.CTkLabel(
            self.header_frame, 
            text="  UNEG", 
            font=("Century Gothic", 20, "bold"),text_color="navy",
        )
        self.Uneg_label.grid(row=0, column=1)  

        self.nombre_sistema = ctk.CTkLabel(
            self.header_frame, 
            text="Sistema de Administración de Laboratorios UNEG", 
            font=("Century Gothic", 20, "bold"),text_color="navy",
        )
        self.nombre_sistema.grid(row=0, column=2)  


         # Cargar la imagen LOGO CL usando una ruta compatible con PyInstaller
        if hasattr(sys, '_MEIPASS'):
            img_path2 = os.path.join(sys._MEIPASS, 'assets', 'CL.png')
        else:
            img_path2 = os.path.join('assets', 'CL.png')
        imagen_logo2 = Image.open(img_path2)
        tamaño_imagen2 = (43, 43) 
        imagen_redimensionada2 = imagen_logo2.resize(tamaño_imagen2)

        self.logo2_ctk = ctk.CTkImage(
            light_image=imagen_redimensionada2,
            dark_image=imagen_redimensionada2,  
            size=tamaño_imagen2
        )

        self.label_imagen2 = ctk.CTkLabel(
            self.header_frame,
            image=self.logo2_ctk,
            text=" "  # Texto vacío para que solo muestre la imagen
        )
        self.label_imagen2.grid(row=0, column=4, padx=10, pady=5, sticky="e")

        # Panel de Navegación
        self.nav_frame = ctk.CTkFrame(self.ventana, width=200, fg_color="gray99")
        self.nav_frame.grid(row=1, column=0, rowspan=2, sticky="nsw", padx=10, pady=10)
        
        self.nav_label = ctk.CTkLabel(self.nav_frame, text="SALU", font=("Century Gothic", 20, "bold"), text_color="Blue2")
        self.nav_label.pack(pady=10)

        # Botones del Panel de Navegación
        self.botones_nav = []
        botones_nav = [
            ("Carga de Asistencia", "📝", self.carga_asistencia),
            ("Carga de Asistencia \n Estudiantes", "👨‍🎓", self.carga_asistencia_estudiantes),
            ("Consultar Asistencia", "🔍", self.consultar_asistencia),
            ("Gestion de Equipos", "💻", self.gestion_equipos),
            ("Módulo Estadístico", "📊", self.modulo_estadistico),
            ("Cerrar Sesión", "🚪", self.cerrar)
        ]

        for texto, icono, command in botones_nav:
            boton = ctk.CTkButton(self.nav_frame, text=f"{icono} {texto}", width=200,height=40, command=command, fg_color="dodger blue",
            hover_color="deep sky blue",  # Color cuando pasas el mouse
            border_color="#ffffff",  # Color del borde
            border_width=2,  # Grosor del borde
            text_color="#ffffff" ,font=("Century Gothic", 14,"bold"),corner_radius=10)
            boton.pack(pady=5)
            self.botones_nav.append(boton)
        
        username = f"{self.user_data['Username']}"
        self.nav_label_user = ctk.CTkLabel(self.nav_frame, text="Bienvenido "+ username, font=("Century Gothic", 20, "bold"), text_color="Blue2")
        self.nav_label_user.pack(pady=10)

        # Botón de ayuda al final del sidebar
        self.boton_about = ctk.CTkButton(self.nav_frame, text="?", width=50, height=40, fg_color="dodger blue",
            hover_color="deep sky blue", border_color="#ffffff", border_width=2, text_color="#ffffff",
            font=("Century Gothic", 18, "bold"), corner_radius=10, command=self.show_about_window)
        self.boton_about.place(x=10, rely=1.0, anchor="sw")

        # Frame principal para mostrar las vistas
        self.main_frame = ctk.CTkFrame(self.ventana, fg_color="gray99")
        self.main_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    def dibujar_gradiente(self):
            """Dibuja el gradiente adaptándose al tamaño actual de la ventana."""
            # Obtener dimensiones actuales
            width = self.ventana.winfo_width()
            height = self.ventana.winfo_height()
            
            # Limpiar el Canvas antes de redibujar
            self.canvas.delete("all")
            
            # Crear gradiente vertical
            for i in range(height):
                ratio = i / height
                r = int(int(self.color1[1:3], 16) * (1 - ratio) + int(int(self.color2[1:3], 16) * ratio))
                g = int(int(self.color1[3:5], 16) * (1 - ratio) + int(int(self.color2[3:5], 16) * ratio))
                b = int(int(self.color1[5:7], 16) * (1 - ratio) + int(int(self.color2[5:7], 16) * ratio))
                color = f"#{r:02x}{g:02x}{b:02x}"
                self.canvas.create_line(0, i, width, i, fill=color, width=1)
         
    def limpiar_frame(self):
        # Limpiar el frame antes de mostrar el formulario de asistencia
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def carga_asistencia(self):
        self.limpiar_frame()
        app = CargaAsistencia(self.main_frame, user_data=self.user_data)
        app.pack(fill="both", expand=True)

    def carga_asistencia_estudiantes(self):
        self.limpiar_frame()
        app = CargaAsistenciaEstudiantes(self.main_frame, user_data=self.user_data)
        app.pack(fill="both", expand=True)

    def consultar_asistencia(self):
        self.limpiar_frame()
        app = ConsultarAsistencia(self.main_frame)
        app.pack(fill="both", expand=True)

    def gestion_equipos(self):
        self.limpiar_frame()
        app = Equipos(self.main_frame)
        app.pack(fill="both", expand=True)

    def modulo_estadistico(self):
        self.limpiar_frame()
        app = ModuloEstadistico(self.main_frame)
        app.pack(fill="both", expand=True)

    def iniciar(self):
        self.ventana.mainloop()

    def cerrar(self):
        # Deshabilitar botones para evitar más clics
        for boton in self.botones_nav:
            try:
                boton.configure(state="disabled")
            except Exception:
                pass

        # Espera 100 ms antes de cerrar para que CTk termine sus after
        self.ventana.after(100, self._abrir_login)

    def _abrir_login(self):
        """Cierra la ventana principal y vuelve al login."""
        try:
            # Cancelar afters pendientes
            for task in self.ventana.tk.call('after', 'info'):
                try:
                    self.ventana.after_cancel(task)
                except Exception:
                    pass
        except Exception:
            pass

        # Quitar bindings que siguen vivos (como el <Configure>)
        try:
            self.ventana.unbind("<Configure>")
        except Exception:
            pass

        # Destruir ventana principal
        if self.ventana.winfo_exists():
            try:
                self.ventana.destroy()
            except Exception:
                pass

        # Importar login y mostrarlo
        from Views.ventana_login import VentanaLogin
        app = VentanaLogin()
        app.iniciar()


    def show_about_window(self):
        # Crear ventana toplevel
        about_win = ctk.CTkToplevel(self.ventana)
        about_win.overrideredirect(True)
        text = "pq presionas el boton sin saber para que sirve tu te imaginas que hubieras borrado la base de datos entera con este boton bersiales no ya retiro la carrera de una vez, Felicidades la base de datos ha sido borrada satisfactoriamente :O"
        label = ctk.CTkLabel(about_win, text=text, font=("Century Gothic", 14), wraplength=350, justify="center")
        label.pack(pady=(20, 10), fill="both", expand=True)
        btn_cerrar = ctk.CTkButton(about_win, text="Cerrar", command=about_win.destroy)
        btn_cerrar.pack(expand=True)
        about_win.update_idletasks()
        ancho = about_win.winfo_width()
        alto = about_win.winfo_height()
        screen_width = self.ventana.winfo_screenwidth()
        screen_height = self.ventana.winfo_screenheight()
        x = (screen_width // 2) - (ancho // 2)
        y = (screen_height // 2) - (alto // 2)
        about_win.geometry(f"{ancho}x{alto}+{x}+{y}")


class VentanaMainAdmin(VentanaMain):
    def __init__(self, user_data):
        super().__init__(user_data)
        # Añadir botón adicional para gestión de usuarios
        boton_gestion_usuarios = ctk.CTkButton(self.nav_frame, text="📊 Gestión de usuarios", width=200,height=40, command=self.gestion_usuarios, fg_color="dodger blue",
            hover_color="deep sky blue",  # Color cuando pasas el mouse
            border_color="#ffffff",  # Color del borde
            border_width=2,  # Grosor del borde
            text_color="#ffffff" ,font=("Century Gothic", 14,"bold"),corner_radius=10)
        boton_gestion_usuarios.pack(pady=5)
        self.botones_nav.append(boton_gestion_usuarios)
        
        # Botón para limpiar la bd
        boton_eliminar_bd = ctk.CTkButton(self.nav_frame, text="🗑️ Limpiar datos", width=200,height=40, command=self.eliminar_datos, fg_color="red",
            hover_color="#FF315E",  # Color cuando pasas el mouse
            border_color="#ffffff",  # Color del borde
            border_width=2,  # Grosor del borde
            text_color="#ffffff" ,font=("Century Gothic", 14,"bold"),corner_radius=10)
        boton_eliminar_bd.pack(pady=5)
        self.botones_nav.append(boton_eliminar_bd)

    def gestion_usuarios(self):
        self.limpiar_frame()
        app = GestionUsuarios(self.main_frame)
        app.pack(fill="both", expand=True)
        app.pack(fill="both", expand=True)
        
    def eliminar_datos(self):
        confirm = messagebox.askyesno(
            "Advertencia",
            "¿Está seguro de que desea eliminar todos los datos?\nEsta acción no se puede deshacer."
        )
        if confirm:
            EliminarDatos(self.ventana, self.user_data) 