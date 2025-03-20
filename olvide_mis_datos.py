import customtkinter as ctk
from tkinter import messagebox

class RecuperarDatosApp:
    def __init__(self):
        self.ventana = ctk.CTk()
        self.ventana.title("Recuperar Datos")
        self.ventana.geometry("1280x720")

        # Crear un frame para centrar el contenido
        self.frame = ctk.CTkFrame(self.ventana)
        self.frame.place(relx=0.5, rely=0.5, anchor='center')  # Centrar el frame

        # Label for numero de cedula
        self.label_cedula = ctk.CTkLabel(self.frame, text="Ingrese el número de cédula del usuario:")
        self.label_cedula.pack(pady=10)

        # Entry for numero de cedula with validation
        vcmd = (self.ventana.register(self.validate_numeric), '%P')
        self.entry_cedula = ctk.CTkEntry(self.frame, width=150, validate='key', validatecommand=vcmd)
        self.entry_cedula.pack(pady=10)

        # Botón Buscar
        self.boton_buscar = ctk.CTkButton(self.frame, text="Buscar", command=self.buscar_click)
        self.boton_buscar.pack(pady=10)

    def validate_numeric(self, value_if_allowed):
        if value_if_allowed.isdigit() or value_if_allowed == "":
            return True
        else:
            return False

    def buscar_click(self):
        # Aquí se debe buscar el usuario en la base de datos
        # y mostrar su usuario y contraseña en un messagebox
        usernarme = "Magleo"
        password = "1234"
        messagebox.showinfo(f"Resultado", "Usuario: "+usernarme+"\n\nContraseña: "+password)

    def iniciar(self):
        self.ventana.mainloop()

