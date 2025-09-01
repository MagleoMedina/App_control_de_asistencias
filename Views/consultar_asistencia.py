import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import ttk, messagebox
from Pdf.pdf import PDFGenerator
import os
from datetime import datetime  # Added import for datetime
from db_manager import DBManager  

class ConsultarAsistencia(ctk.CTkFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

         # Instanciar DBManager
        self.db_manager = DBManager()

        # Obtener sedes de la base de datos
        self.sedes = self.db_manager.obtener_sedes()
        sede_names = [s[1] for s in self.sedes] if self.sedes else []

        
        # Título centrado
        self.title_label = ctk.CTkLabel(self, text="Consultar Asistencia", font=("Arial", 20))
        self.title_label.grid(row=1, column=3, columnspan=2, pady=10)
        
        # Labels y Entries
        self.sede_label = ctk.CTkLabel(self, text="Sede")
        self.sede_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.sede_entry = ctk.CTkComboBox(self, values=sede_names, state="readonly",command=self.on_sede_selected)
        self.sede_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Inicializar laboratorios según la sede seleccionada
        self.laboratorios = []
        self.lab_names = []
        
        self.laboratorio_label = ctk.CTkLabel(self, text="Laboratorio")
        self.laboratorio_label.grid(row=2, column=2, padx=10, pady=5, sticky="e")
        self.laboratorio_entry = ctk.CTkComboBox(self, values=[], state="readonly")
        self.laboratorio_entry.grid(row=2, column=3, padx=10, pady=5, sticky="w")

        # Si hay sedes, selecciona la primera y actualiza laboratorios
        if sede_names:
            # Selecciona la primera sede por defecto
            self.sede_entry.set(sede_names[0])
            # Busca el índice de la sede seleccionada
            selected_sede = self.sede_entry.get()
            for idx, sede in enumerate(self.sedes):
                if sede[1] == selected_sede:
                    break
            self.on_sede_selected()
        
        self.fecha = ctk.CTkLabel(self, text="Fecha")
        self.fecha.grid(row=2, column=4, padx=10, pady=5, sticky="e")
        self.fecha_entry = DateEntry(self, date_pattern="dd/mm/yyyy",font=("Arial", 11, "bold"), foreground='#1abc9c', background='#34495e', borderwidth=2, relief='sunken', width=20)
        self.fecha_entry.grid(row=2, column=5, padx=10, pady=5, sticky="w")

        # Botón Generar Reporte
        self.generar_reporte_btn = ctk.CTkButton(self, text="Generar reporte", command=self.validar_campos)
        self.generar_reporte_btn.grid(row=3, column=3, columnspan=2, pady=20)

    def update_laboratorios(self):
        selected_sede_name = self.sede_entry.get()
        sede_id = None
        for s in self.sedes:
            if s[1] == selected_sede_name:
                sede_id = s[0]
                break
        if sede_id is not None:
            self.laboratorios = self.db_manager.obtener_laboratorios_por_sede(sede_id)
        else:
            self.laboratorios = []
        self.lab_names = [l[1] for l in self.laboratorios] if self.laboratorios else []

    def on_sede_selected(self, event=None):
        self.update_laboratorios()
        self.laboratorio_entry.set("")
        self.laboratorio_entry.configure(values=self.lab_names)
        if self.lab_names:
            self.laboratorio_entry.set(self.lab_names[0])
        else:
            self.laboratorio_entry.set("")

    def crear_pdf(self):
        # Read the HTML template
        html_template_path = os.path.join(os.path.dirname(__file__), "..", "Pdf", "consultar_asistencia.html")
        with open(html_template_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        
        # Ensure CSS file exists
        css_path = os.path.join(os.path.dirname(__file__), "..", "Pdf", "estilos.css")

        #Variables para el html
        sede = self.sede_entry.get()
        laboratorio = self.laboratorio_entry.get()  
        fecha = self.fecha_entry.get()
        # Datos de ejemplo extraídos de una BD (simulación)
        datos = [
            {"Tipo de uso": "Apoyo al estudiante en asesorías con sus equipos, profesores, preparadores", "Nombre": "Carlos", "Apellido": "Pérez", "Cédula": "12345678", "Organización": "UNEG", "Teléfono": "0412-3456789", "Número de bien": "00123"},
            {"Tipo de uso": "Talleres de capacitación al personal administrativo y docente", "Nombre": "Ana", "Apellido": "Gómez", "Cédula": "87654321", "Organización": "UNEG", "Teléfono": "0414-9876543", "Número de bien": "00456"},
        ]

        # Generar las filas de la tabla en HTML con un contador para "No"
        tabla_consulta_asistencia = "".join(
            f"<tr><td style='width: 40px'>{i+1}</td><td style='width: 100px'>{fila['Tipo de uso']}</td><td>{fila['Nombre']}</td>"
            f"<td>{fila['Apellido']}</td><td>{fila['Cédula']}</td><td>{fila['Organización']}</td>"
            f"<td>{fila['Teléfono']}</td><td>{fila['Número de bien']}</td></tr>"
            for i, fila in enumerate(datos)
        )

        #Reemplazar en el html
        html_content = html_content.replace("{{sede}}", sede)
        html_content = html_content.replace("{{laboratorio}}", laboratorio)
        html_content = html_content.replace("{{fecha}}", fecha)
        html_content = html_content.replace("{{fecha_actual}}", datetime.now().strftime("%d/%m/%Y"))
        html_content = html_content.replace("{{tabla_consulta_asistencia}}", tabla_consulta_asistencia)
        

        # Generate the PDF with a dynamic filename
        current_datetime = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        pdf_filename = f"Asistencia_{current_datetime}.pdf"
        pdf_generator = PDFGenerator(pdf_filename)

        success = pdf_generator.generate_pdf(html_content, css_path=css_path)
        if success:
            messagebox.showinfo("Éxito", f"Reporte generado exitosamente: {pdf_filename}")
        else:
            messagebox.showerror("Error", "No se pudo generar el reporte")

    def validar_campos(self):
        if not self.sede_entry.get() or not self.laboratorio_entry.get() or not self.fecha_entry.get():
            messagebox.showerror("Error", "Todos los campos deben estar llenos")
        
        elif self.fecha_entry.get() > datetime.now().strftime("%d/%m/%Y"):
            messagebox.showerror("Error", "La fecha no puede ser mayor a la actual")
        
        # colocar un elif no existe reportes para esa fecha
        else:
            # Lógica para generar el reporte
            self.crear_pdf()


