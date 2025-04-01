import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import ttk, messagebox
import tkinter as tk  # Importar tkinter para la validación
from Pdf.pdf import PDFGenerator
import os
from datetime import datetime  # Importar datetime para la fecha y hora actual


class Equipos(ctk.CTkFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # Título centrado
        self.title_label = ctk.CTkLabel(self, text="Gestion de Equipos", font=("Arial", 20))
        self.title_label.grid(row=0, column=3, columnspan=3, pady=10)
        
        # Botón "Consultar Falla de Equipo"
        self.consultar_falla_button = ctk.CTkButton(self, text="Consultar Equipo", command=self.consultar_falla_equipo)
        self.consultar_falla_button.grid(row=1, column=0, padx=10, pady=10)

        # Botón "Agregar Equipo"
        self.agregar_equipo_button = ctk.CTkButton(self, text="Agregar Equipo", command=self.agregar_equipo)
        self.agregar_equipo_button.grid(row=1, column=1, padx=10, pady=10)

        # Botón "Modificar Equipo"
        self.modificar_equipo_button = ctk.CTkButton(self, text="Modificar Equipo", command=self.modificar_equipo)
        self.modificar_equipo_button.grid(row=1, column=2, padx=10, pady=10)

        # Botón "Eliminar Equipo"
        self.eliminar_equipo_button = ctk.CTkButton(self, text="Eliminar Equipo", command=self.eliminar_equipo)
        self.eliminar_equipo_button.grid(row=1, column=3, padx=10, pady=10)

        # Botón "Relacionar Equipos"
        self.relacionar_equipos_button = ctk.CTkButton(self, text="Relacionar Equipos", command=self.relacionar_equipos)
        self.relacionar_equipos_button.grid(row=1, column=4, padx=10, pady=10)

    def clear_frame(self):
        # Remove all widgets except the buttons
        for widget in self.winfo_children():
            if widget not in [
                self.title_label,
                self.consultar_falla_button,
                self.agregar_equipo_button,
                self.modificar_equipo_button,
                self.eliminar_equipo_button,
                self.relacionar_equipos_button,
            ]:
                widget.destroy()

    def consultar_falla_equipo(self):
        self.clear_frame()
        consultar_falla_frame = ConsultarFallaEquipo(self)
        consultar_falla_frame.grid(row=2, column=0, columnspan=4, pady=10)

    def agregar_equipo(self):
        self.clear_frame()
        agregar_equipo_frame = AgregarEquipo(self)
        agregar_equipo_frame.grid(row=2, column=0, columnspan=4, pady=10)

    def modificar_equipo(self):
        self.clear_frame()
        modificar_equipo_frame = ModificarEquipo(self)
        modificar_equipo_frame.grid(row=2, column=0, columnspan=4, pady=10)

    def eliminar_equipo(self):
        self.clear_frame()
        eliminar_equipo_frame = EliminarEquipo(self)
        eliminar_equipo_frame.grid(row=2, column=0, columnspan=4, pady=10)

    def relacionar_equipos(self):
        self.clear_frame()
        relacionar_equipos_frame = RelacionarEquipos(self)
        relacionar_equipos_frame.grid(row=2, column=0, columnspan=4, pady=10)

class ConsultarFallaEquipo(ctk.CTkFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # Título centrado
        self.title_label = ctk.CTkLabel(self, text="Consultar equipo", font=("Arial", 20))
        self.title_label.grid(row=0, column=1, columnspan=2, pady=10)
        
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

        # Lista de equipos con datos
        equipos = [
            {"Equipo": "Computadora", "Número de bien": "12345", "Sede": "Sede Central", "Laboratorio": "Lab 101", "Status": "Operativo"},
            {"Equipo": "Teclado", "Número de bien": "67890", "Sede": "Sede Central", "Laboratorio": "Lab 102", "Status": "En reparación"},
            {"Equipo": "Ratón", "Número de bien": "54321", "Sede": "Sede Norte", "Laboratorio": "Lab 103", "Status": "Operativo"},
            {"Equipo": "Monitor", "Número de bien": "98765", "Sede": "Sede Sur", "Laboratorio": "Lab 104", "Status": "Dañado"},
        ]

        # Lista de fallos registrados
        fallos = [
            {"Equipo": "12345", "FechaHora": "2025-03-31 14:30", "Descripción": "Fallo en el disco duro"},
            {"Equipo": "98765", "FechaHora": "2025-03-30 10:15", "Descripción": "Pantalla rota"},
        ]

        # Generar la tabla en HTML
        tabla_equipos = "".join(
            f"<tr><td>{e['Equipo']}</td><td>{e['Número de bien']}</td><td>{e['Sede']}</td>"
            f"<td>{e['Laboratorio']}</td><td>{e['Status']}</td></tr>"
            for e in equipos
        )

        # Generar la lista de fallos en HTML solo si hay fallos
        if fallos:
            lista_fallos = "".join(
                f"<p>El equipo <strong>{f['Equipo']}</strong> falló el <strong>{f['FechaHora']}</strong>. "
                f"Descripción de la falla: <strong>{f['Descripción']}</strong></p>"
                for f in fallos
            )
        else:
            lista_fallos = "<p>No se han registrado fallos en estos equipos.</p>"

        # Reemplazar en el html
        html_content = html_content.replace("{{nro_de_bien}}", nro_bien)
        html_content = html_content.replace("{{lista_fallos}}", lista_fallos)
        html_content = html_content.replace("{{tabla_equipos}}", tabla_equipos)
        html_content = html_content.replace("{{fecha_actual}}", datetime.now().strftime("%d/%m/%Y"))


       

        # Generate the PDF with a dynamic filename
        current_datetime = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        pdf_filename = f"Consulta_Equipo_{current_datetime}.pdf"
        pdf_generator = PDFGenerator(pdf_filename)

        success = pdf_generator.generate_pdf(html_content, css_path=css_path)
        if success:
            messagebox.showinfo("Éxito", f"Reporte generado exitosamente: {pdf_filename}")
        else:
            messagebox.showerror("Error", "No se pudo generar el reporte")

class AgregarEquipo(ctk.CTkFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # Label and Dropdown for "Sede"
        self.sede_label = ctk.CTkLabel(self, text="Sede")
        self.sede_label.grid(row=0, column=0, padx=10, pady=5)
        values_sede = ["a", "b", "c"]
        self.sede_dropdown = ctk.CTkComboBox(self, values=values_sede, state="readonly")
        self.sede_dropdown.grid(row=0, column=1, padx=10, pady=5)

        # Label and Dropdown for "Laboratorio"
        self.laboratorio_label = ctk.CTkLabel(self, text="Laboratorio")
        self.laboratorio_label.grid(row=1, column=0, padx=10, pady=5)
        values_lab = ["a", "b", "c"]
        self.laboratorio_dropdown = ctk.CTkComboBox(self, values=values_lab, state="readonly")
        self.laboratorio_dropdown.grid(row=1, column=1, padx=10, pady=5)

        # Label and Dropdown for "Equipo"
        self.equipo_label = ctk.CTkLabel(self, text="Equipo")
        self.equipo_label.grid(row=2, column=0, padx=10, pady=5)
        values_equipo = ["Computadora", "Teclado", "Ratón", "Monitor"]
        self.equipo_dropdown = ctk.CTkComboBox(self, values=values_equipo, state="readonly")
        self.equipo_dropdown.grid(row=2, column=1, padx=10, pady=5)

        # Label and Dropdown for "Status"
        self.status_label = ctk.CTkLabel(self, text="Status")
        self.status_label.grid(row=3, column=0, padx=10, pady=5)
        values_status = ["Operativo", "No operativo"]
        self.status_dropdown = ctk.CTkComboBox(self, values=values_status, state="readonly")
        self.status_dropdown.grid(row=3, column=1, padx=10, pady=5)

        # Label and Entry for "Número de bien"
        self.nro_bien_label = ctk.CTkLabel(self, text="Número de bien")
        self.nro_bien_label.grid(row=4, column=0, padx=10, pady=5)
        self.nro_bien_entry = ctk.CTkEntry(self)
        self.nro_bien_entry.grid(row=4, column=1, padx=10, pady=5)

        # Add validation for numeric input
        self.nro_bien_entry.configure(validate="key", validatecommand=(self.register(self.validate_numeric), "%S"))

        # Botón "Guardar"
        self.guardar_button = ctk.CTkButton(self, text="Guardar", command=self.guardar_datos)
        self.guardar_button.grid(row=5, column=0, columnspan=2, pady=10)

    def validate_numeric(self, char):
        return char.isdigit()

    def guardar_datos(self):
        # Obtener valores de los campos
        sede = self.sede_dropdown.get()
        laboratorio = self.laboratorio_dropdown.get()
        equipo = self.equipo_dropdown.get()
        status = self.status_dropdown.get()
        nro_bien = self.nro_bien_entry.get()

        # Validar que los campos no estén vacíos
        if not sede or not laboratorio or not equipo or not status or not nro_bien.strip():
            messagebox.showerror("Error", "Todos los campos deben estar llenos.")
            return

        # Aquí se puede agregar la lógica para guardar los datos
        messagebox.showinfo("Éxito", "Datos guardados correctamente.")

class ModificarEquipo(ctk.CTkFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # Label "Número de bien del equipo"
        self.nro_bien_label = ctk.CTkLabel(self, text="Número de bien del equipo")
        self.nro_bien_label.grid(row=0, column=0, padx=10, pady=5)

        # Entry for "Número de bien del equipo"
        self.nro_bien_entry = ctk.CTkEntry(self)
        self.nro_bien_entry.grid(row=0, column=1, padx=10, pady=5)

        # Add validation for numeric input
        self.nro_bien_entry.configure(validate="key", validatecommand=(self.register(self.validate_numeric), "%S"))

        # Button "Buscar"
        self.buscar_button = ctk.CTkButton(self, text="Buscar", command=self.buscar_equipo)
        self.buscar_button.grid(row=0, column=2, padx=10, pady=5)

        # Placeholder for "Actualizar" button
        self.actualizar_button = None

    def validate_numeric(self, char):
        return char.isdigit()

    def buscar_equipo(self):
        nro_bien = self.nro_bien_entry.get()
        if not nro_bien.strip():
            messagebox.showerror("Error", "El campo 'Número de bien del equipo' no puede estar vacío.")
        else:
            # Display additional elements
            self.display_fields()

    def display_fields(self):
        # Label and Dropdown for "Sede"
        self.sede_label = ctk.CTkLabel(self, text="Sede")
        self.sede_label.grid(row=1, column=0, padx=10, pady=5)
        values_sede = ["a", "b", "c"]
        self.sede_dropdown = ctk.CTkComboBox(self, values=values_sede, state="readonly")
        self.sede_dropdown.grid(row=1, column=1, padx=10, pady=5)

        # Label and Dropdown for "Laboratorio"
        self.laboratorio_label = ctk.CTkLabel(self, text="Laboratorio")
        self.laboratorio_label.grid(row=2, column=0, padx=10, pady=5)
        values_lab = ["a", "b", "c"]
        self.laboratorio_dropdown = ctk.CTkComboBox(self, values=values_lab, state="readonly")
        self.laboratorio_dropdown.grid(row=2, column=1, padx=10, pady=5)

        # Label and Dropdown for "Equipo"
        self.equipo_label = ctk.CTkLabel(self, text="Equipo")
        self.equipo_label.grid(row=3, column=0, padx=10, pady=5)
        values_equipo = ["Computadora", "Teclado", "Ratón", "Monitor"]
        self.equipo_dropdown = ctk.CTkComboBox(self, values=values_equipo, state="readonly")
        self.equipo_dropdown.grid(row=3, column=1, padx=10, pady=5)

        # Label and Dropdown for "Status"
        self.status_label = ctk.CTkLabel(self, text="Status")
        self.status_label.grid(row=4, column=0, padx=10, pady=5)
        values_status = ["Operativo", "No operativo"]
        self.status_dropdown = ctk.CTkComboBox(self, values=values_status, state="readonly")
        self.status_dropdown.grid(row=4, column=1, padx=10, pady=5)

        # Label and Entry for "Número de bien"
        self.nro_bien_label = ctk.CTkLabel(self, text="Nuevo número de bien")
        self.nro_bien_label.grid(row=5, column=0, padx=10, pady=5)
        self.nro_bien_entry = ctk.CTkEntry(self)
        self.nro_bien_entry.grid(row=5, column=1, padx=10, pady=5)

        self.nro_bien_entry.configure(validate="key", validatecommand=(self.register(self.validate_numeric), "%S"))

        # Button "Actualizar"
        if not self.actualizar_button:
            self.actualizar_button = ctk.CTkButton(self, text="Actualizar", command=self.actualizar_datos)
            self.actualizar_button.grid(row=6, column=0, columnspan=2, pady=10)

    def actualizar_datos(self):
        # Collect data from fields
        sede = self.sede_dropdown.get()
        laboratorio = self.laboratorio_dropdown.get()
        equipo = self.equipo_dropdown.get()
        status = self.status_dropdown.get()
        nro_bien = self.nro_bien_entry.get()

        # Validate that no fields are empty
        if not sede or not laboratorio or not equipo or not status or not nro_bien.strip():
            messagebox.showerror("Error", "Todos los campos deben estar llenos.")
            return

        # Logic to handle the updated data
        messagebox.showinfo("Éxito", f"Datos actualizados:\nSede: {sede}\nLaboratorio: {laboratorio}\nEquipo: {equipo}\nStatus: {status}\nNúmero de bien: {nro_bien}")

class EliminarEquipo(ctk.CTkFrame):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # Label "Ingrese el número de bien del equipo"
        self.nro_bien_label = ctk.CTkLabel(self, text="Ingrese el número de bien del equipo")
        self.nro_bien_label.grid(row=0, column=0, padx=10, pady=5)

        # Entry for "Número de bien"
        self.nro_bien_entry = ctk.CTkEntry(self)
        self.nro_bien_entry.grid(row=0, column=1, padx=10, pady=5)

        # Add validation for numeric input
        self.nro_bien_entry.configure(validate="key", validatecommand=(self.register(self.validate_numeric), "%S"))

        # Button "Eliminar"
        self.eliminar_button = ctk.CTkButton(self, text="Eliminar", command=self.eliminar_equipo)
        self.eliminar_button.grid(row=0, column=2, padx=10, pady=5)

    def validate_numeric(self, char):
        return char.isdigit()

    def eliminar_equipo(self):
        nro_bien = self.nro_bien_entry.get()
        if not nro_bien.strip():
            messagebox.showerror("Error", "El campo 'Número de bien del equipo' no puede estar vacío.")
        else:
            # Confirmation dialog
            confirm = messagebox.askyesno("Confirmación", f"¿Está seguro que desea eliminar el equipo {nro_bien}?")
            if confirm:
                # Success message
                messagebox.showinfo("Éxito", f"El equipo con número de bien {nro_bien} se ha eliminado exitosamente.")
            else:
                messagebox.showinfo("Cancelado", "Operación cancelada.") 

class RelacionarEquipos(ctk.CTkFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # Title
        self.title_label = ctk.CTkLabel(self, text="Ingresa los números de bien a relacionar", font=("Arial", 20))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Label and Entry for "Computadora"
        self.computadora_label = ctk.CTkLabel(self, text="Computadora")
        self.computadora_label.grid(row=1, column=0, padx=10, pady=5)
        self.computadora_entry = ctk.CTkEntry(self)
        self.computadora_entry.grid(row=1, column=1, padx=10, pady=5)
        self.computadora_entry.configure(validate="key", validatecommand=(self.register(self.validate_numeric), "%S"))

        # Label and Entry for "Teclado"
        self.teclado_label = ctk.CTkLabel(self, text="Teclado")
        self.teclado_label.grid(row=2, column=0, padx=10, pady=5)
        self.teclado_entry = ctk.CTkEntry(self)
        self.teclado_entry.grid(row=2, column=1, padx=10, pady=5)
        self.teclado_entry.configure(validate="key", validatecommand=(self.register(self.validate_numeric), "%S"))

        # Label and Entry for "Monitor"
        self.monitor_label = ctk.CTkLabel(self, text="Monitor")
        self.monitor_label.grid(row=3, column=0, padx=10, pady=5)
        self.monitor_entry = ctk.CTkEntry(self)
        self.monitor_entry.grid(row=3, column=1, padx=10, pady=5)
        self.monitor_entry.configure(validate="key", validatecommand=(self.register(self.validate_numeric), "%S"))

        # Label and Entry for "Ratón"
        self.raton_label = ctk.CTkLabel(self, text="Ratón")
        self.raton_label.grid(row=4, column=0, padx=10, pady=5)
        self.raton_entry = ctk.CTkEntry(self)
        self.raton_entry.grid(row=4, column=1, padx=10, pady=5)
        self.raton_entry.configure(validate="key", validatecommand=(self.register(self.validate_numeric), "%S"))

        # Button "Relacionar"
        self.relacionar_button = ctk.CTkButton(self, text="Relacionar", command=self.relacionar_equipos)
        self.relacionar_button.grid(row=5, column=0, columnspan=2, pady=10)

    def validate_numeric(self, char):
        return char.isdigit()

    def relacionar_equipos(self):
        # Collect data from entries
        computadora = self.computadora_entry.get()
        teclado = self.teclado_entry.get()
        monitor = self.monitor_entry.get()
        raton = self.raton_entry.get()

        # Validate that no fields are empty
        if not computadora.strip() or not teclado.strip() or not monitor.strip() or not raton.strip():
            messagebox.showerror("Error", "Todos los campos deben estar llenos.")
            return

        # Logic to handle the collected data
        messagebox.showinfo(
            "Éxito",
            f"Equipos relacionados:\nComputadora: {computadora}\nTeclado: {teclado}\nMonitor: {monitor}\nRatón: {raton}"
        )

