import customtkinter as ctk
from tkinter import messagebox
from db_manager import DBManager

class EliminarDatos(ctk.CTkToplevel):
    def __init__(self, parent, user_data):
        super().__init__(parent)
        self.title("Confirmar eliminación")
        self.geometry("400x200")
        self.parent = parent
        self.user_data = user_data
        self.db = DBManager()
        self.db.set_parent(self.parent) 
        
        ancho, alto = 400, 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (ancho // 2)
        y = (screen_height // 2) - (alto // 2)

        self.geometry(f"{ancho}x{alto}+{x}+{y}")

        # Que la ventana quede encima y bloquee la principal
        self.transient(parent)
        self.grab_set()
        self.focus_set()

        self.label = ctk.CTkLabel(self, text="Ingrese su contraseña para confirmar:", font=("Arial", 14))
        self.label.pack(pady=20)

        self.entry_pass = ctk.CTkEntry(self, show="*")
        self.entry_pass.pack(pady=10)

        self.btn_confirm = ctk.CTkButton(self, text="Confirmar", command=self.confirmar)
        self.btn_confirm.pack(pady=10)

    def confirmar(self):
        password = self.entry_pass.get()
        username = self.user_data["Username"]

        # Validar en BD que sigue siendo admin y contraseña es correcta
        user = self.db.autenticar_usuario(username, password)
        if not user or user["Tipo_usuario"].lower() != "administrador":
            messagebox.showerror("Error", "Contraseña incorrecta, no se puede eliminar los datos.")
            return

        if self.db.limpiar_datos():
            messagebox.showinfo("Éxito", "Datos eliminados correctamente.")
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudieron eliminar los datos.")