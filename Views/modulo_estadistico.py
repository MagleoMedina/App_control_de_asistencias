import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import ttk, messagebox
from Pdf.pdf import PDFGenerator
import os
from datetime import datetime  
from db_manager import DBManager

class ModuloEstadistico(ctk.CTkFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # Título centrado
        self.title_label = ctk.CTkLabel(self, text="Generar Reporte estádistico", font=("Arial", 20))
        self.title_label.grid(row=1, column=3, columnspan=2, pady=10)

        # Instanciar DBManager
        self.db_manager = DBManager()
        self.db_manager.set_parent(self.parent)

         # Obtener sedes de la base de datos
        self.sedes = self.db_manager.obtener_sedes()
        sede_names = [s[1] for s in self.sedes] if self.sedes else []
        
        # Labels y Entries
        self.sede_label = ctk.CTkLabel(self, text="Sede")
        self.sede_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.sede_entry =ctk.CTkComboBox(self, values=sede_names, state="readonly", command=self.on_sede_selected)
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

        # Obtener actividades reales desde la base de datos
        actividades, total_cantidad = self.db_manager.obtener_estadisticas_actividades(
            sede, laboratorio, fecha_inicio, fecha_finalizacion
        )

         # Obtener cantidad de estudiantes atendidos en el rango de fechas
        # Sede y laboratorio ya validados arriba
        sede_id = None
        lab_id = None
        for s in self.sedes:
            if s[1] == sede:
                sede_id = s[0]
                break
        if sede_id is not None:
            for l in self.laboratorios:
                if l[1] == laboratorio:
                    lab_id = l[0]
                    break

        estudiantes_atendidos = 0
        if sede_id is not None and lab_id is not None:
            query = """
                SELECT SUM(Cantidad)
                FROM Uso_laboratorio_estudiante
                WHERE Laboratorio = ?
                AND Fecha >= ? AND Fecha <= ?
            """
            result = self.db_manager.execute_query(query, (lab_id, fecha_inicio, fecha_finalizacion), fetch_one=True)
            estudiantes_atendidos = result[0] if result and result[0] is not None else 0

        # Insertar "Estudiantes atendidos" antes de "Otro"
        actividades_mod = []
        otro_idx = None
        for idx, actividad in enumerate(actividades):
            if actividad["nombre"].strip().lower() == "otro":
                otro_idx = idx
                break
        if otro_idx is not None:
            actividades_mod = actividades[:otro_idx] + [{"nombre": "Estudiantes atendidos", "cantidad": estudiantes_atendidos}] + actividades[otro_idx:]
        else:
            actividades_mod = actividades + [{"nombre": "Estudiantes atendidos", "cantidad": estudiantes_atendidos}]

        # Convertir la lista en filas HTML (solo una vez)
        actividades_html = "".join(
            f"<tr><td>{actividad['nombre']}</td><td>{actividad['cantidad']}</td></tr>"
            for actividad in actividades_mod
        )
        actividades_html += f"<tr><td><strong>Total</strong></td><td><strong>{total_cantidad + estudiantes_atendidos}</strong></td></tr>"

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