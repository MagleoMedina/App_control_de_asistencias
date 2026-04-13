import  customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import sys
from db_manager import DBManager
import subprocess, re, ctypes
import platform
import tkinter as tk


def obtener_dimensiones_pantalla():
    
    system = platform.system()
    try:
        if system == "Windows":
            user32 = ctypes.windll.user32
            try:
                user32.SetProcessDPIAware()
            except Exception:
                pass
            return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        if system == "Linux":
            try:
                out = subprocess.check_output(['xrandr', '--query'], stderr=subprocess.DEVNULL).decode()
                m = re.search(r'current\s+(\d+)\s+x\s+(\d+)', out)
                if m:
                    return int(m.group(1)), int(m.group(2))
            except Exception:
                pass
        if system == "Darwin":
            try:
                out = subprocess.check_output(['system_profiler', 'SPDisplaysDataType'], stderr=subprocess.DEVNULL).decode()
                m = re.search(r'Resolution:\s*(\d+)\s*x\s*(\d+)', out)
                if m:
                    return int(m.group(1)), int(m.group(2))
            except Exception:
                pass
    except Exception:
        pass

    # Fallback: tkinter oculto (no muestra ventana)
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        root.destroy()
        return w, h
    except Exception:
        return 1366, 768

class VentanaLogin:
    def __init__(self):
        # Crear la ventana principal
        self.ventana = ctk.CTk()
        self.ventana.title("Login")

        #self.ventana.geometry("1400x720+10+10")

        # 0. Hacer la ventana totalmente transparente (invisible) mientras se configura
        self.ventana.attributes("-alpha", 0.0)

        system_os = platform.system()
        if system_os == "Linux":
            try:
                self.ventana.attributes("-zoomed", True)
            except Exception:
                self.ventana.state("zoomed")
        else:
            self.ventana.state("zoomed")
            
        # 2. Darle un instante a la ventana para que se dibuje maximizada
        self.ventana.update()
        
        # 3. Capturar el ancho, alto y posición exactos de la ventana ya maximizada
        max_w = self.ventana.winfo_width()
        max_h = self.ventana.winfo_height()
        max_x = self.ventana.winfo_x()
        max_y = self.ventana.winfo_y()
        
        # 4. Fijar esa geometría gigante para que no se encoja
        self.ventana.geometry(f"{max_w}x{max_h}+{max_x}+{max_y}")
        
        # 5. Finalmente, bloquear la ventana (deshabilita el botón maximizar)
        self.ventana.resizable(False, False)
        
        #6. Devolverle la opacidad al 100% después de un delay de 500 milisegundos
        self.ventana.after(500, lambda: self.ventana.attributes("-alpha", 1.0))

        # --- Establecer icono personalizado multiplataforma ---

        
        if hasattr(sys, '_MEIPASS'):
            icon_png_path = os.path.join(sys._MEIPASS, 'assets', 'LogoSALIU.png')
            icon_ico_path = os.path.join(sys._MEIPASS, 'assets', 'LogoSALIU.ico')
            path_ver = os.path.join(sys._MEIPASS, 'assets', 'ojo-abierto.png')
            path_ocultar = os.path.join(sys._MEIPASS, 'assets', 'ojo-cerrado.png')
        else:
            icon_png_path = os.path.join('assets', 'LogoSALIU.png')
            icon_ico_path = os.path.join('assets', 'LogoSALIU.ico')
            path_ver = os.path.join('assets', 'ojo-abierto.png')
            path_ocultar = os.path.join('assets', 'ojo-cerrado.png')
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

        ctk.set_appearance_mode("light")
        self.db = DBManager()  # Conexión a la BD
        self.db.set_parent(self.ventana) 
        
        self.img_ver = ctk.CTkImage(Image.open(path_ver), size=(20, 20))
        self.img_ocultar = ctk.CTkImage(Image.open(path_ocultar), size=(20, 20))

        if hasattr(sys, '_MEIPASS'):
            img_path3 = os.path.join(sys._MEIPASS, 'assets', 'login2.png')
        else:
            img_path3 = os.path.join('assets', 'login2.png')
        # Cargar imagen original
        imagen_login = Image.open(img_path3)

        # Obtener resolución real de la pantalla
        screen_w = self.ventana.winfo_screenwidth()
        screen_h = self.ventana.winfo_screenheight()

        # Calcular proporción ideal (ajuste al alto o ancho según pantalla)
        img_ratio = imagen_login.width / imagen_login.height
        screen_ratio = screen_w / screen_h

        if screen_ratio > img_ratio:
            # Pantalla más ancha → ajustar al ancho
            new_w = screen_w
            new_h = int(screen_w / img_ratio)
        else:
            # Pantalla más alta → ajustar al alto
            new_h = screen_h
            new_w = int(screen_h * img_ratio)

        # Escalar una sola vez
        imagen_escalada = imagen_login.resize((new_w, new_h), Image.LANCZOS)

        # Crear imagen CTk
        self.ctk_login = ctk.CTkImage(
            light_image=imagen_escalada,
            dark_image=imagen_escalada,
            size=(new_w, new_h)
        )

        # Colocar la imagen de fondo
        self.label_fondo = ctk.CTkLabel(self.ventana, image=self.ctk_login, text="")
        self.label_fondo.place(x=0, y=0, relwidth=1, relheight=1)


        # Configuración del contenedor principal
        self.frame_principal = ctk.CTkFrame(self.ventana,fg_color="gray99",border_width=3, border_color="DeepSkyBlue2",height=400)
        self.frame_principal.place(relx=0.5, rely=0.5, anchor='center')  # Centrar el frame

        # Etiqueta y campo de entrada para el nombre de usuario
        self.label_usuario = ctk.CTkLabel(self.frame_principal, text="  Usuario:",font=("Century Gothic", 14))
        self.label_usuario.grid(row=0, column=0, pady=10,padx=(6,5), sticky='w')
        self.entry_usuario = ctk.CTkEntry(self.frame_principal, width=200,placeholder_text="Nombre de Usuario",font=("Century Gothic", 14),corner_radius=10,border_color="light blue")
        self.entry_usuario.grid(row=1, column=0,padx=(15,5), sticky='w')

         # Etiqueta para la contraseña
        self.label_password = ctk.CTkLabel(self.frame_principal, text="   Contraseña:", font=("Century Gothic", 14))
        self.label_password.grid(row=2, column=0, pady=5,padx=5, sticky='w')

         # Campo de entrada para la contraseña con tamaño uniforme
        self.entry_password = ctk.CTkEntry(self.frame_principal, show="*", width=200,corner_radius=10,border_color="light blue")  # Ajusta el tamaño del campo
        self.entry_password.grid(row=3, column=0,columnspan=1, padx=(15,5), pady=5)
        
        # Agregar eventos para hover en usuario
        self.entry_usuario.bind("<Enter>", lambda event: self.on_hover(event, self.entry_usuario))
        self.entry_usuario.bind("<Leave>", lambda event: self.off_hover(event, self.entry_usuario))

        # Agregar eventos para hover en contraseña
        self.entry_password.bind("<Enter>", lambda event: self.on_hover(event, self.entry_password))
        self.entry_password.bind("<Leave>", lambda event: self.off_hover(event, self.entry_password))
        # Botón para mostrar/ocultar contraseña
        self.boton_mostrar_ocultar = ctk.CTkButton(
            self.frame_principal, 
            image=self.img_ver,
            text="",
            command=self.mostrar_ocultar_password,
            width=30,
            height=25,
            fg_color="transparent",
            hover_color="light gray",
            border_color="light blue",
            text_color="#ffffff",
            font=("Century Gothic", 14, "bold"),
            corner_radius=10,
            border_width=2
        )
        self.boton_mostrar_ocultar.grid(row=3, column=1, padx=(5, 15), pady=5, sticky="w") # Desplazado un poco a la derecha

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
        
        self.ventana.bind("<Return>", lambda event: self.ingresar())
    
    # Cambia el color cuando el mouse entra
    def on_hover(self, event, widget):
     widget.configure(border_color="light sky blue")

    def off_hover(self, event, widget):
     widget.configure(border_color="light blue")

    

    def mostrar_ocultar_password(self):
        """Función para mostrar u ocultar la contraseña con iconos de ojo."""
        if self.password_visible:
            # Estado: Ocultando contraseña
            self.entry_password.configure(show="*")
            self.boton_mostrar_ocultar.configure(image=self.img_ver) # Cambia a ojo abierto
        else:
            # Estado: Mostrando contraseña
            self.entry_password.configure(show="")
            self.boton_mostrar_ocultar.configure(image=self.img_ocultar) # Cambia a ojo tachado/cerrado
        
        self.password_visible = not self.password_visible

    def ingresar(self):
        """Función que se ejecuta al hacer clic en el botón 'Ingresar'."""
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()

        if not usuario or not password:
            messagebox.showwarning("Error", "Por favor, completa todos los campos.")
            return
        
        # Deshabilitamos el botón un momento para evitar doble clic accidental
        self.boton_ingresar.configure(state="disabled")

        # Consulta a la base de datos
        user_data = self.db.autenticar_usuario(usuario, password)

        if user_data:

            # Espera 300 ms antes de cerrar para que CTk termine sus callbacks pendientes
            self.ventana.after(300, self._abrir_main, user_data)

        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
            self.boton_ingresar.configure(state="normal")
    
    def iniciar(self):
        """Inicia el bucle principal de la ventana."""
        self.ventana.mainloop()
        
    def _abrir_main(self, user_data):
        """Función para abrir la ventana principal y cerrar la de login."""
        try:
            for task in self.ventana.tk.call('after', 'info'):
                try:
                    self.ventana.after_cancel(task)
                except Exception:
                    pass
        except Exception:
            pass

        # Evita errores de Tcl cuando se destruye una ventana que tiene grab activo
        try:
            self.ventana.grab_release()
        except Exception:
            pass

        try:
            self.ventana.unbind("<Return>")
        except Exception:
            pass

        try:
            self.ventana.destroy()
        except Exception:
            pass

        from Views.ventana_main import VentanaMainAdmin, VentanaMain
        if user_data["Tipo_usuario"].lower() == "administrador":
            app = VentanaMainAdmin(user_data)
        else:
            app = VentanaMain(user_data)
        app.iniciar()
    
   
    