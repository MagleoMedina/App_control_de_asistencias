import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import ttk, messagebox
from Pdf.pdf import PDFGenerator
import os
from datetime import datetime  

class ModuloEstadistico(ctk.CTkFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # Título centrado
        self.title_label = ctk.CTkLabel(self, text="Generar Reporte estádistico", font=("Arial", 20))
        self.title_label.grid(row=1, column=3, columnspan=2, pady=10)
        
        # Labels y Entries
        self.sede_label = ctk.CTkLabel(self, text="Sede")
        self.sede_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        values_sede = ["Villa asia", "Atlantico"]#recuperar de la bd
        self.sede_entry =ctk.CTkComboBox(self, values=values_sede, state="readonly")
        self.sede_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        self.laboratorio_label = ctk.CTkLabel(self, text="Laboratorio")
        self.laboratorio_label.grid(row=2, column=2, padx=10, pady=5, sticky="e")
        values_lab= ["Villa asia", "Atlantico"]#recuperar de la bd
        self.laboratorio_entry = ctk.CTkComboBox(self, values=values_lab, state="readonly")
        self.laboratorio_entry.grid(row=2, column=3, padx=10, pady=5, sticky="w")
        
        self.fecha_inicio_label = ctk.CTkLabel(self, text="Fecha de inicio")
        self.fecha_inicio_label.grid(row=2, column=4, padx=10, pady=5, sticky="e")
        self.fecha_inicio_entry = DateEntry(self, date_pattern="dd/mm/yyyy",font=("Arial", 11, "bold"), foreground='#1abc9c', background='#34495e', borderwidth=2, relief='sunken', width=20)
        self.fecha_inicio_entry.grid(row=2, column=5, padx=10, pady=5, sticky="w")
        
        self.fecha_finalizacion_label = ctk.CTkLabel(self, text="Fecha de finalización")
        self.fecha_finalizacion_label.grid(row=2, column=6, padx=10, pady=5, sticky="e")
        self.fecha_finalizacion_entry = DateEntry(self, date_pattern="dd/mm/yyyy",font=("Arial", 11, "bold"), foreground='#1abc9c', background='#34495e', borderwidth=2, relief='sunken', width=20)
        self.fecha_finalizacion_entry.grid(row=2, column=7, padx=10, pady=5, sticky="w")
        
        # Botón Generar Reporte
        self.generar_reporte_button = ctk.CTkButton(self, text="Generar reporte", command=self.generar_reporte)
        self.generar_reporte_button.grid(row=3, column=3, columnspan=2, pady=20)

    def crear_pdf(self):
        # Read the HTML template
        html_template_path = os.path.join(os.path.dirname(__file__), "..", "Pdf", "modulo_estadistico.html")
        with open(html_template_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        # Ensure CSS file exists
        css_path = os.path.join(os.path.dirname(__file__), "..", "Pdf", "estilos.css")

        # Variables para el html
        sede = self.sede_entry.get()
        laboratorio = self.laboratorio_entry.get()  
        fecha_inicio = self.fecha_inicio_entry.get()
        fecha_finalizacion = self.fecha_finalizacion_entry.get()
        # Simulación de actividades
        actividades = [
            {"nombre": "Servicios de Internet", "cantidad": 5},
            {"nombre": "Atencion al usuario", "cantidad": 3},
            {"nombre": "Apoyo al estudiante en asesoría, con sus equipos, profesores, preparadores", "cantidad": 10},
            {"nombre": "Talleres de capacitación al personal administrativo y docente", "cantidad": 2},
            {"nombre": "Apoyo en actividades a otras instituciones", "cantidad": 3},
            {"nombre": "Atencion al usuario", "cantidad": 3},
            {"nombre": "Apoyo a instituciones externas", "cantidad": 5},
            {"nombre": "Apoyo a personas de la comunidad", "cantidad": 3},
            {"nombre": "Otro", "cantidad": 3},
        ]

        # Convertir la lista en filas HTML
        actividades_html = "".join(
            f"<tr><td>{actividad['nombre']}</td><td>{actividad['cantidad']}</td></tr>"
            for actividad in actividades
        )
        
        # Calcular el total
        total_cantidad = sum(actividad['cantidad'] for actividad in actividades)

        # Agregar la fila de total
        actividades_html += f"<tr><td><strong>Total</strong></td><td><strong>{total_cantidad}</strong></td></tr>"


        # Reemplazar en el html
        html_content = html_content.replace("{{sede}}", sede)
        html_content = html_content.replace("{{laboratorio}}", laboratorio)
        html_content = html_content.replace("{{fecha_inicio}}", fecha_inicio)
        html_content = html_content.replace("{{fecha_finalizacion}}", fecha_finalizacion)
        html_content = html_content.replace("{{actividades}}", actividades_html)
        html_content = html_content.replace("{{fecha_actual}}", datetime.now().strftime("%d/%m/%Y"))
        
        # Generate the PDF with a dynamic filename
        current_datetime = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        pdf_filename = f"Estadisticas_{sede}_{laboratorio}_{current_datetime}.pdf"
        pdf_generator = PDFGenerator(pdf_filename)

        success = pdf_generator.generate_pdf(html_content, css_path=css_path)
        if success:
            messagebox.showinfo("Éxito", f"Reporte generado exitosamente: {pdf_filename}")
        else:
            messagebox.showerror("Error", "No se pudo generar el reporte")

    def generar_reporte(self):
        if not self.sede_entry.get() or not self.laboratorio_entry.get() or not self.fecha_inicio_entry.get() or not self.fecha_finalizacion_entry.get():
            messagebox.showerror("Error", "Todos los campos deben estar llenos")
        
        elif self.fecha_inicio_entry.get() > datetime.now().strftime("%d/%m/%Y") or self.fecha_finalizacion_entry.get() > datetime.now().strftime("%d/%m/%Y"):
            messagebox.showerror("Error", "La fecha no puede ser mayor a la actual")
        
        # colocar un elif no existe reportes para esa fecha
        else:
            # Lógica para generar el reporte
            self.crear_pdf()