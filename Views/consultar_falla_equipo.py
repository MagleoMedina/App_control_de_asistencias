import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import ttk, messagebox
import tkinter as tk  # Importar tkinter para la validación

class ConsultarFallaEquipo(ctk.CTkFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # Título centrado
        self.title_label = ctk.CTkLabel(self, text="Consultar falla", font=("Arial", 20))
        self.title_label.grid(row=0, column=3, columnspan=3, pady=10)
        
        # Label "Nro de bien"
        self.nro_bien_label = ctk.CTkLabel(self, text="Nro de bien")
        self.nro_bien_label.grid(row=1, column=0, padx=10, pady=10)
        
        # Entry para "Nro de bien"
        self.nro_bien_entry = ctk.CTkEntry(self)
        self.nro_bien_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Validación para que solo se puedan tipear números
        self.nro_bien_entry.configure(validate="key", validatecommand=(self.register(self.validate_numeric), "%S"))
        
        # Botón "Buscar"
        self.buscar_button = ctk.CTkButton(self, text="Buscar")
        self.buscar_button.grid(row=1, column=2, padx=10, pady=10)
    
    def validate_numeric(self, char):
        return char.isdigit()
