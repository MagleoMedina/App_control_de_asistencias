import platform
import sys
import os
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Necesario para manejar imágenes
from Views.carga_asistencia import CargaAsistencia
from Views.carga_asistencia_estudiantes import CargaAsistenciaEstudiantes
from Views.consultar_asistencia import ConsultarAsistencia
from Views.modulo_estadistico import ModuloEstadistico
from Views.equipos import Equipos
from Views.gestion_de_usuarios import GestionUsuarios
from Views.eliminar_datos import EliminarDatos
from db_manager import DBManager

class VentanaMain:
    def __init__(self, user_data):
        self.user_data = user_data
        self.db = DBManager()
        # Crear una instancia de la ventana principal
        self.ventana = ctk.CTk()
        self.ventana.geometry("1400x720+10+10")
        self.ventana.title("SALIU")
        ctk.set_appearance_mode("light")
        
        # --- Establecer icono personalizado multiplataforma ---
        if hasattr(sys, '_MEIPASS'):
            icon_png_path = os.path.join(sys._MEIPASS, 'assets', 'LogoSALIU.png')
            icon_ico_path = os.path.join(sys._MEIPASS, 'assets', 'LogoSALIU.ico')
            bg_path = os.path.join(sys._MEIPASS, 'assets', 'gradiente.png')
        else:
            icon_png_path = os.path.join('assets', 'LogoSALIU.png')
            icon_ico_path = os.path.join('assets', 'LogoSALIU.ico')
            bg_path = os.path.join('assets', 'gradiente.png')
        system = platform.system()
        if system == "Windows" and os.path.exists(icon_ico_path):
            try:
                self.ventana.iconbitmap(icon_ico_path)
            except Exception as e:
                print(f"Advertencia: No se pudo establecer el icono .ico: {e}")
        elif system == "Linux" and os.path.exists(icon_png_path):
            try:
                # Usar PhotoImage para icono en Linux
                icon_img = tk.PhotoImage(file=icon_png_path)
                self.ventana.iconphoto(True, icon_img)
            except Exception as e:
                print(f"Advertencia: No se pudo establecer el icono .png: {e}")
        else:
            print(f"Advertencia: No se encontró el icono en la ruta: {icon_png_path} o {icon_ico_path}")
        
        # Gradiente
        self.bg_image_original = Image.open(bg_path)
        
        # Crear el label vacío inicialmente
        self.bg_label = tk.Label(self.ventana)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.ventana.bind("<Configure>", self.redimensionar_fondo)

        # Definir colores del gradiente (azul claro a blanco)
        self.color1 = "#4B9CD3"  # Azul claro
        self.color2 = "#FFFFFF"  # Blanco
        
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
        if hasattr(sys, '_MEIPASS'):
            img_path = os.path.join(sys._MEIPASS, 'assets', 'logo_uneg.png')
        else:
            img_path = os.path.join('assets','logo_uneg.png')
        imagen_logo = Image.open(img_path)
        tamaño_imagen = (42, 42)
        imagen_redimensionada = imagen_logo.resize(tamaño_imagen)

        try:
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
        except Exception as e:
            print(f"Advertencia: no se pudo mostrar logo UNEG: {e}")
            self.label_imagen = ctk.CTkLabel(
                self.header_frame,
                text="UNEG",
                font=("Century Gothic", 20, "bold"),
                text_color="navy"
            )

        self.label_imagen.grid(row=0, column=0, padx=10, pady=5, sticky="w")  # Posición izquierda


        # Label del encabezado - pady reducido para disminuir espacio vertical
        self.Uneg_label = ctk.CTkLabel(
            self.header_frame, 
            text="  UNEG", 
            font=("Century Gothic", 20, "bold"),text_color="navy",
        )
        self.Uneg_label.grid(row=0, column=1)  

        self.nombre_sistema = ctk.CTkLabel(
            self.header_frame, 
            text="Sistema de Administración de los Laboratorios de Informática UNEG", 
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

        try:
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
        except Exception as e:
            print(f"Advertencia: no se pudo mostrar logo CL: {e}")
            self.label_imagen2 = ctk.CTkLabel(
                self.header_frame,
                text="CL",
                font=("Century Gothic", 20, "bold"),
                text_color="navy"
            )

        self.label_imagen2.grid(row=0, column=4, padx=10, pady=5, sticky="e")

        # Panel de Navegación
        self.nav_frame = ctk.CTkFrame(self.ventana, width=200, fg_color="gray99")
        self.nav_frame.grid(row=1, column=0, rowspan=2, sticky="nsw", padx=10, pady=10)
        
        self.nav_label = ctk.CTkLabel(self.nav_frame, text="SALIU", font=("Century Gothic", 20, "bold"), text_color="Blue2")
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
         
    def redimensionar_fondo(self, event=None):
        # Evitar procesar eventos que no sean de la ventana principal
        if event and event.widget != self.ventana:
            return

        # Obtener el nuevo tamaño de la ventana
        nuevo_ancho = self.ventana.winfo_width()
        nuevo_alto = self.ventana.winfo_height()

        # Solo redimensionar si el tamaño es válido (mayor a 1x1)
        if nuevo_ancho > 1 and nuevo_alto > 1:
            # Redimensionar la imagen original al nuevo tamaño
            imagen_redimensionada = self.bg_image_original.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
            
            # Convertir a formato Tkinter
            self.bg_image_tk = ImageTk.PhotoImage(imagen_redimensionada)
            
            # Actualizar el label
            self.bg_label.configure(image=self.bg_image_tk)
            
    def limpiar_frame(self):
        # Limpiar el frame antes de mostrar el formulario de asistencia
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def carga_asistencia(self):
        self.limpiar_frame()
        app = CargaAsistencia(self.main_frame, user_data=self.user_data, db_manager=self.db)
        app.pack(fill="both", expand=True)

    def carga_asistencia_estudiantes(self):
        self.limpiar_frame()
        app = CargaAsistenciaEstudiantes(self.main_frame, user_data=self.user_data, db_manager=self.db)
        app.pack(fill="both", expand=True)

    def consultar_asistencia(self):
        self.limpiar_frame()
        app = ConsultarAsistencia(self.main_frame, db_manager=self.db)
        app.pack(fill="both", expand=True)

    def gestion_equipos(self):
        self.limpiar_frame()
        app = Equipos(self.main_frame, db_manager=self.db)
        app.pack(fill="both", expand=True)

    def modulo_estadistico(self):
        self.limpiar_frame()
        app = ModuloEstadistico(self.main_frame, db_manager=self.db)
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
        # 1. Crear ventana toplevel robusta
        about_win = ctk.CTkToplevel(self.ventana)
        about_win.overrideredirect(True)
        about_win.attributes("-topmost", True)
        about_win.configure(fg_color="dodger blue") 

        # 2. Contenedor principal cuadrado
        main_container = ctk.CTkFrame(
            about_win, 
            fg_color="white", 
            corner_radius=0
        )
        main_container.pack(fill="both", expand=True, padx=2, pady=2)

        # Título de la App
        ctk.CTkLabel(
            main_container, 
            text="SALIU v1.0", 
            font=("Century Gothic", 22, "bold"), 
            text_color="navy"
        ).pack(pady=(25, 10))

        # ÁREA DE CONTENIDO
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30)

        # Nombre completo del sistema
        ctk.CTkLabel(
            content_frame, 
            text="Sistema de Administración de los Laboratorios\nde Informática UNEG", 
            font=("Century Gothic", 15, "bold"),
            text_color="dodger blue",
            justify="center"
        ).pack(pady=(0, 15))

        # Descripción original
        desc_text = (
            "SALIU es una solución tecnológica integral diseñada para optimizar la gestión, "
            "control y monitoreo de los Laboratorios de Informática de la UNEG. El sistema automatiza "
            "el registro de usuarios, el control de inventario de equipos y la generación de métricas "
            "estadísticas en tiempo real."
        )
        ctk.CTkLabel(
            content_frame, text=desc_text, font=("Century Gothic", 12),
            wraplength=400, justify="center", text_color="gray25"
        ).pack(pady=(0, 15))

        # Equipo de trabajo
        equipo_text = (
            "DESARROLLADO POR:\n\n"
            "• Daniela Espinoza\n"
            "• Franmari Garcia\n"
            "• Magleo Medina\n"
            "• Benjamín Travieso"
        )
        ctk.CTkLabel(
            content_frame, text=equipo_text, font=("Century Gothic", 12, "bold"),
            text_color="navy", justify="center"
        ).pack(pady=(0, 15)) # Distancia hacia asesores

        # Asesores
        asesores_text = (
            "Asesor Académico: Kelvin Carima\n"
            "Asesor Comunitario: Joel Uricare"
        )
        # pady=(0, 25) le da "un poco más" de aire antes del footer
        self.label_asesores = ctk.CTkLabel(
            content_frame, text=asesores_text, font=("Century Gothic", 12, "bold"),
            text_color="dodger blue", justify="center"
        )
        self.label_asesores.pack(pady=(0, 25)) 

        # Footer Institucional
        info_extra = (
            "Universidad Nacional Experimental de Guayana (UNEG) - 2026\n"
            "Tecnologías: Python, CustomTkinter & SQLite (Turso Cloud)"
        )
        self.label_footer = ctk.CTkLabel(
            content_frame, text=info_extra, font=("Century Gothic", 11),
            text_color="gray50", justify="center"
        )
        # Reducimos a 0 el espacio inferior para que el botón suba
        self.label_footer.pack(pady=(0, 0))

        # 3. Botón de cierre redondeado
        btn_cerrar = ctk.CTkButton(
            main_container, 
            text="Entendido", 
            text_color="white",
            command=about_win.destroy,
            fg_color="dodger blue",
            hover_color="deep sky blue",
            font=("Century Gothic", 14, "bold"),
            corner_radius=20,
            width=140,
            height=35
        )
        # pady=(10, 20) lo separa 10px del footer y deja 20px al borde de la ventana
        btn_cerrar.pack(pady=(10, 20))

        # --- Lógica de Centrado y Tamaño ---
        about_win.update_idletasks()
        ancho, alto = 480, 480 # Reduje el alto de 640 a 620 para compactar todo
        
        v_width = self.ventana.winfo_width()
        v_height = self.ventana.winfo_height()
        v_x = self.ventana.winfo_x()
        v_y = self.ventana.winfo_y()
        
        pos_x = v_x + (v_width // 2) - (ancho // 2)
        pos_y = v_y + (v_height // 2) - (alto // 2)
        
        about_win.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")

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
        app = GestionUsuarios(self.main_frame, db_manager=self.db)
        app.pack(fill="both", expand=True)
        app.pack(fill="both", expand=True)
        
    def eliminar_datos(self):
        confirm = messagebox.askyesno(
            "Advertencia",
            "¿Está seguro de que desea eliminar todos los datos?\nEsta acción no se puede deshacer."
        )
        if confirm:
            EliminarDatos(self.ventana, self.user_data, db_manager=self.db)