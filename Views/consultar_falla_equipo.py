import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import ttk, messagebox
import tkinter as tk  # Importar tkinter para la validación
from Pdf.pdf import PDFGenerator
import os
from datetime import datetime  # Importar datetime para la fecha y hora actual

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
        self.buscar_button = ctk.CTkButton(self, text="Buscar", command=self.on_buscar_click)
        self.buscar_button.grid(row=1, column=2, padx=10, pady=10)
    
    def validate_numeric(self, char):
        return char.isdigit()
    
    def on_buscar_click(self):
        nro_bien = self.nro_bien_entry.get()
        if not nro_bien.strip():
            messagebox.showerror("Error", "El campo 'Nro de bien' no puede estar vacío.")
       
        #elif de que si el nro de bien no existe en la base de datos
        #     messagebox.showerror("Error", "El nro de bien no existe.")
       
        else:
            self.crear_pdf()
    
    def crear_pdf(self):
        # Read the HTML template
        html_template_path = os.path.join(os.path.dirname(__file__), "..", "Pdf", "consultar_falla_equipo.html")
        with open(html_template_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        # Ensure CSS file exists
        css_path = os.path.join(os.path.dirname(__file__), "..", "Pdf", "estilos.css")

        # Variables para el html
        nro_bien = self.nro_bien_entry.get()
      

        # Reemplazar en el html
        html_content = html_content.replace("{{nro_de_bien}}", nro_bien)
       

        # Generate the PDF with a dynamic filename
        current_datetime = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        pdf_filename = f"Falla_equipo_{current_datetime}.pdf"
        pdf_generator = PDFGenerator(pdf_filename)

        success = pdf_generator.generate_pdf(html_content, css_path=css_path)
        if success:
            messagebox.showinfo("Éxito", f"Reporte generado exitosamente: {pdf_filename}")
        else:
            messagebox.showerror("Error", "No se pudo generar el reporte")
