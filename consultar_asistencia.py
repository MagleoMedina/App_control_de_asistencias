import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import ttk, messagebox

class ConsultarAsistencia(ctk.CTkFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # Título centrado
        self.title_label = ctk.CTkLabel(self, text="Consultar Asistencia", font=("Arial", 20))
        self.title_label.grid(row=1, column=3, columnspan=2, pady=10)
        
        # Labels y Entries
        self.sede_label = ctk.CTkLabel(self, text="Sede")
        self.sede_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        values_sede = ["Villa asia", "Atlantico"]#recuperar de la bd
        self.sede_entry = ctk.CTkComboBox(self, values=values_sede, state="readonly")
        self.sede_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        self.laboratorio_label = ctk.CTkLabel(self, text="Laboratorio")
        self.laboratorio_label.grid(row=2, column=2, padx=10, pady=5, sticky="e")
        values_lab= ["Villa asia", "Atlantico"]#recuperar de la bd
        self.laboratorio_entry = ctk.CTkComboBox(self, values=values_lab, state="readonly")
        self.laboratorio_entry.grid(row=2, column=3, padx=10, pady=5, sticky="w")
        
        self.fecha = ctk.CTkLabel(self, text="Fecha")
        self.fecha.grid(row=2, column=4, padx=10, pady=5, sticky="e")
        self.fecha_entry = DateEntry(self, date_pattern="dd/mm/yyyy")
        self.fecha_entry.grid(row=2, column=5, padx=10, pady=5, sticky="w")

        # Botón Generar Reporte
        self.generar_reporte_btn = ctk.CTkButton(self, text="Generar reporte", command=self.validar_campos)
        self.generar_reporte_btn.grid(row=3, column=3, columnspan=2, pady=20)

    def validar_campos(self):
        if not self.sede_entry.get() or not self.laboratorio_entry.get() or not self.fecha_entry.get():
            messagebox.showerror("Error", "Todos los campos deben estar llenos")
        else:
            # Lógica para generar el reporte
            pass


