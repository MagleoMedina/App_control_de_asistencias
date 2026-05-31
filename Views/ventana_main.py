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
from Views.sede import GestionSedeLaboratorios
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

        self.color1 = "#4B9CD3"  # Azul claro
        self.color2 = "#FFFFFF"  # Blanco

        self.header_frame = ctk.CTkFrame(self.ventana, height=50, fg_color="gray99")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.ventana.grid_columnconfigure(0, weight=0)  # Columna 0 (nav_frame) - ancho fijo
        self.ventana.grid_columnconfigure(1, weight=1)  # Columna 1 (main_frame) - se expande
        self.ventana.grid_rowconfigure(1, weight=1)     # Fila 1 (nav_frame + main_frame) - se expande
        
        self.header_frame = ctk.CTkFrame(
            self.ventana, 
            height=50, 
            fg_color="gray99", 
        )
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.header_frame.grid_propagate(False) 
        
        self.header_frame.grid_columnconfigure(0, weight=0)  # Logo UNEG (ancho fijo)
        self.header_frame.grid_columnconfigure(1, weight=0)  # Label "UNEG" (ancho fijo)
        self.header_frame.grid_columnconfigure(2, weight=1)  
        self.header_frame.grid_columnconfigure(3, weight=0)  
        self.header_frame.grid_columnconfigure(4, weight=0)  # Logo CL 

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

        self.nav_frame = ctk.CTkFrame(self.ventana, width=200, fg_color="gray99")
        self.nav_frame.grid(row=1, column=0, rowspan=2, sticky="nsw", padx=10, pady=10)
        
        self.nav_label = ctk.CTkLabel(self.nav_frame, text="SALIU", font=("Century Gothic", 20, "bold"), text_color="Blue2")
        self.nav_label.pack(pady=10)

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

        self.boton_about = ctk.CTkButton(self.nav_frame, text="Acerca de", width=50, height=40, fg_color="dodger blue",
            hover_color="deep sky blue", border_color="#ffffff", border_width=2, text_color="#ffffff",
            font=("Century Gothic", 12, "bold"), corner_radius=10, command=self.show_about_window)
        self.boton_about.place(x=10, rely=1.0, anchor="sw")


        self.main_frame = ctk.CTkFrame(self.ventana, fg_color="gray99")
        self.main_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
         
    def redimensionar_fondo(self, event=None):

        if event and event.widget != self.ventana:
            return


        nuevo_ancho = self.ventana.winfo_width()
        nuevo_alto = self.ventana.winfo_height()


        if nuevo_ancho > 1 and nuevo_alto > 1:
  
            imagen_redimensionada = self.bg_image_original.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
            

            self.bg_image_tk = ImageTk.PhotoImage(imagen_redimensionada)
            

            self.bg_label.configure(image=self.bg_image_tk)
            
    def limpiar_frame(self):

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

        for boton in self.botones_nav:
            try:
                boton.configure(state="disabled")
            except Exception:
                pass

        self.ventana.after(100, self._abrir_login)

    def _abrir_login(self):
        """Cierra la ventana principal y vuelve al login."""
        try:
            for task in self.ventana.tk.call('after', 'info'):
                try:
                    self.ventana.after_cancel(task)
                except Exception:
                    pass
        except Exception:
            pass

        try:
            self.ventana.unbind("<Configure>")
        except Exception:
            pass

        if self.ventana.winfo_exists():
            try:
                self.ventana.destroy()
            except Exception:
                pass

        from Views.ventana_login import VentanaLogin
        app = VentanaLogin()
        app.iniciar()


    def show_about_window(self):
        about_win = ctk.CTkToplevel(self.ventana)
        about_win.title("Acerca de SALIU")
        about_win.transient(self.ventana)
        about_win.resizable(False, False)
        

        about_win.update_idletasks()
        about_win.grab_set()

        about_win.configure(fg_color="#f1f5f8")
        about_win.grid_columnconfigure(0, weight=1)
        about_win.grid_rowconfigure(0, weight=1)

        content_frame = ctk.CTkFrame(about_win, fg_color="#ffffff", corner_radius=20)
        content_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        content_frame.grid_propagate(False)
        content_frame.grid_columnconfigure(0, weight=1)

        current_row = 0

        if hasattr(sys, '_MEIPASS'):
            logo_path = os.path.join(sys._MEIPASS, 'assets', 'LogoSALIU.png')
        else:
            logo_path = os.path.join('assets', 'LogoSALIU.png')

        if os.path.exists(logo_path):
            try:
                logo_image = Image.open(logo_path)
                logo_image = logo_image.resize((80, 80), Image.LANCZOS)
                self.about_logo_image = ImageTk.PhotoImage(logo_image)
                logo_label = ctk.CTkLabel(content_frame, image=self.about_logo_image, text="")
                logo_label.grid(row=current_row, column=0, pady=(15, 10), sticky="n")
                current_row += 1
            except Exception:
                pass

        header_label = ctk.CTkLabel(
            content_frame,
            text="ACERCA DE SALIU",
            font=("Century Gothic", 18, "bold"),
            text_color="#1f4e79"
        )
        header_label.grid(row=current_row, column=0, pady=(0, 10), sticky="n")
        current_row += 1

        description_label = ctk.CTkLabel(
            content_frame,
            text="SALIU es un sistema de gestión de asistencia y laboratorios diseñado para registrar usos, administrar sedes y laboratorios, y generar reportes estadísticos.",
            font=("Century Gothic", 12),
            wraplength=440,
            justify="center",
            text_color="#2f4f6f"
        )
        description_label.grid(row=current_row, column=0, pady=(0, 15), padx=20, sticky="ew")
        current_row += 1

        features_label = ctk.CTkLabel(
            content_frame,
            text="Funciones principales:\n• Registro de asistencias\n• Gestión de sedes y laboratorios\n• Generación de reportes estadísticos",
            font=("Century Gothic", 11),
            wraplength=440,
            justify="left",
            text_color="#3b536b"
        )
        features_label.grid(row=current_row, column=0, pady=(0, 15), padx=40, sticky="w")
        current_row += 1

        system_info = (
            f"Versión: 1.0\n"
            f"Plataforma: {platform.system()} {platform.release()}\n"
            f"Python: {platform.python_version()}"
        )
        info_label = ctk.CTkLabel(
            content_frame,
            text=system_info,
            font=("Century Gothic", 11),
            wraplength=440,
            justify="center",
            text_color="#3b536b"
        )
        info_label.grid(row=current_row, column=0, pady=(0, 15), sticky="ew")
        current_row += 1

        desarrolladores_texto = (
            "Desarrollado por:\n"
            "Magleo Medina  •  Franmari Garcia\n"
            "Daniela Espinoza  •  Benjamin Travieso\n\n"
            "Universidad Nacional Experimental de Guayana (UNEG)"
        )
        credits_label = ctk.CTkLabel(
            content_frame,
            text=desarrolladores_texto,
            font=("Century Gothic", 11, "bold"),
            wraplength=440,
            justify="center",
            text_color="#1f4e79"
        )
        credits_label.grid(row=current_row, column=0, pady=(0, 15), sticky="ew")
        current_row += 1

        close_button = ctk.CTkButton(
            content_frame,
            text="Cerrar",
            width=120,
            command=about_win.destroy,
            fg_color="dodger blue",
            hover_color="deep sky blue",
            text_color="#ffffff",
            font=("Century Gothic", 12, "bold"),
            corner_radius=12
        )
        close_button.grid(row=current_row, column=0, pady=(10, 0), sticky="n")

        about_width = 540
        about_height = 560
        about_win.minsize(about_width, about_height)

        screen_width = self.ventana.winfo_screenwidth()
        screen_height = self.ventana.winfo_screenheight()
        x = (screen_width // 2) - (about_width // 2)
        y = (screen_height // 2) - (about_height // 2)
        about_win.geometry(f"{about_width}x{about_height}+{x}+{y}")
        
        about_win.lift()
        


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

        boton_sede = ctk.CTkButton(self.nav_frame, text="📊 Sedes", width=200,height=40, command=self.sede, fg_color="dodger blue",
            hover_color="deep sky blue",  # Color cuando pasas el mouse
            border_color="#ffffff",  # Color del borde
            border_width=2,  # Grosor del borde
            text_color="#ffffff" ,font=("Century Gothic", 14,"bold"),corner_radius=10)
        boton_sede.pack(pady=5)
        self.botones_nav.append(boton_sede)
        
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

    def sede(self):
        self.limpiar_frame()
        app = GestionSedeLaboratorios(self.main_frame, db_manager=self.db)
        app.pack(fill="both", expand=True)