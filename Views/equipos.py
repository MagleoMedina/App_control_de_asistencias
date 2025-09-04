import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import ttk, messagebox
import tkinter as tk  # Importar tkinter para la validación
from Pdf.pdf import PDFGenerator
import os
from datetime import datetime  # Importar datetime para la fecha y hora actual
from db_manager import DBManager

class Equipos(ctk.CTkFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = DBManager()  # Instancia de DBManager

        # Cambiar el color del fondo a blanco
        self.configure(fg_color="white")
        
        # Título centrado
        self.title_label = ctk.CTkLabel(self, text="Gestion de Equipos", font=("Century Gothic", 20, "bold"),text_color="navy")
        self.title_label.grid(row=0, column=0, columnspan=5, pady=10, sticky="nsew")
        
        # Botón "Consultar Falla de Equipo"
        self.consultar_falla_button = ctk.CTkButton(self, text="Consultar Equipo", command=self.consultar_falla_equipo,width=120,
        height=28,
        fg_color="dodger blue",
        hover_color="deep sky blue",  # Color cuando pasas el mouse
        border_color="#ffffff",  # Color del borde
        border_width=2,  # Grosor del borde
        text_color="#ffffff",
        font=("Century Gothic", 14, "bold"),
        corner_radius=10)
        self.consultar_falla_button.grid(row=1, column=0, padx=10, pady=10)

        # Botón "Agregar Equipo"
        self.agregar_equipo_button = ctk.CTkButton(self, text="Agregar Equipo", command=self.agregar_equipo,width=120,
        height=28,
        fg_color="dodger blue",
        hover_color="deep sky blue",  # Color cuando pasas el mouse
        border_color="#ffffff",  # Color del borde
        border_width=2,  # Grosor del borde
        text_color="#ffffff",
        font=("Century Gothic", 14, "bold"),
        corner_radius=10)
        self.agregar_equipo_button.grid(row=1, column=1, padx=10, pady=10)

        # Botón "Modificar Equipo"
        self.modificar_equipo_button = ctk.CTkButton(self, text="Modificar Equipo", command=self.modificar_equipo,width=120,
        height=28,
        fg_color="dodger blue",
        hover_color="deep sky blue",  # Color cuando pasas el mouse
        border_color="#ffffff",  # Color del borde
        border_width=2,  # Grosor del borde
        text_color="#ffffff",
        font=("Century Gothic", 14, "bold"),
        corner_radius=10)
        self.modificar_equipo_button.grid(row=1, column=2, padx=10, pady=10)

        # Botón "Relacionar Equipos"
        self.relacionar_equipos_button = ctk.CTkButton(self, text="Relacionar Equipos", command=self.relacionar_equipos,width=120,
        height=28,
        fg_color="dodger blue",
        hover_color="deep sky blue",  # Color cuando pasas el mouse
        border_color="#ffffff",  # Color del borde
        border_width=2,  # Grosor del borde
        text_color="#ffffff",
        font=("Century Gothic", 14, "bold"),
        corner_radius=10)
        self.relacionar_equipos_button.grid(row=1, column=3, padx=10, pady=10)

    def clear_frame(self):
        # Remove all widgets except the buttons
        for widget in self.winfo_children():
            if widget not in [
                self.title_label,
                self.consultar_falla_button,
                self.agregar_equipo_button,
                self.modificar_equipo_button,
                self.relacionar_equipos_button,
            ]:
                widget.destroy()

    def consultar_falla_equipo(self):
        self.clear_frame()
        consultar_falla_frame = ConsultarFallaEquipo(self)
        consultar_falla_frame.grid(row=2, column=0, columnspan=4, pady=10)

    def agregar_equipo(self):
        self.clear_frame()
        agregar_equipo_frame = AgregarEquipo(self, self.db_manager)
        agregar_equipo_frame.grid(row=2, column=0, columnspan=4, pady=10)

    def modificar_equipo(self):
        self.clear_frame()
        modificar_equipo_frame = ModificarEquipo(self, self.db_manager)
        modificar_equipo_frame.grid(row=2, column=0, columnspan=4, pady=10)

    def relacionar_equipos(self):
        self.clear_frame()
        relacionar_equipos_frame = RelacionarEquipos(self)
        relacionar_equipos_frame.grid(row=2, column=0, columnspan=4, pady=10)

class ConsultarFallaEquipo(ctk.CTkFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = DBManager()  # Instanciar DBManager

        # Cambiar el color del fondo a navy
        self.configure(fg_color="navy")

        # Título centrado
        self.title_label = ctk.CTkLabel(self, text="Consultar equipo", font=("Century Gothic", 14, "bold"),text_color="white")
        self.title_label.grid(row=0, column=1, columnspan=2, pady=10)
        
        # Label "Nro de bien"
        self.nro_bien_label = ctk.CTkLabel(self, text="Nro de bien",font=("Century Gothic", 14, "bold"),text_color="white")
        self.nro_bien_label.grid(row=1, column=1, padx=10, pady=5)
        
        # Entry para "Nro de bien"
        self.nro_bien_entry = ctk.CTkEntry(self)
        self.nro_bien_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Validación para que solo se puedan tipear números
        self.nro_bien_entry.configure(validate="key", validatecommand=(self.register(self.validate_numeric), "%S"))
        
        # Botón "Buscar"
        self.buscar_button = ctk.CTkButton(self, text="Buscar", command=self.on_buscar_click, fg_color="dodger blue",
        hover_color="deep sky blue",  # Color cuando pasas el mouse
        border_color="#ffffff",  # Color del borde
        border_width=2,  # Grosor del borde
        text_color="#ffffff",
        font=("Century Gothic", 14, "bold"),
        corner_radius=10)
        self.buscar_button.grid(row=2, column=2, padx=10, pady=10)
    
    def validate_numeric(self, char):
        return char.isdigit()
    
    def on_buscar_click(self):
        nro_bien = self.nro_bien_entry.get()
        if not nro_bien.strip():
            messagebox.showerror("Error", "El campo 'Nro de bien' no puede estar vacío.")
            return

        # Verifica si el equipo existe
        equipo_data = self.db_manager.buscar_equipo_por_nro_bien(nro_bien)
        if not equipo_data:
            messagebox.showerror("Error", "El nro de bien no existe.")
            return

        self.crear_pdf(nro_bien)

    def crear_pdf(self, nro_bien=None):
        # Read the HTML template
        html_template_path = os.path.join(os.path.dirname(__file__), "..", "Pdf", "consultar_falla_equipo.html")
        with open(html_template_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        css_path = os.path.join(os.path.dirname(__file__), "..", "Pdf", "estilos.css")

        # Recuperar datos reales de la base de datos
        equipos = self.db_manager.consultar_equipo_con_componentes(nro_bien)
        fallos = self.db_manager.consultar_fallas_por_equipo(nro_bien)

        # Generar la tabla en HTML
        tabla_equipos = "".join(
            f"<tr><td>{e['Descripcion']}</td><td>{e['Nro_de_bien']}</td><td>{e['Sede']}</td>"
            f"<td>{e['Laboratorio']}</td><td>{e['Status']}</td></tr>"
            for e in equipos
        )

        # Generar la lista de fallos en HTML solo si hay fallos
        if fallos:
            lista_fallos = "".join(
                f"<p>El equipo <strong>{f['Equipo']}</strong> falló el <strong>{f['FechaHora']}</strong>. "
                f"Descripción de la falla: <strong>{f['Descripcion']}</strong></p>"
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
    def __init__(self, parent=None, db_manager=None):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = db_manager

        # Cambiar el color del fondo a navy
        self.configure(fg_color="navy")

        # Obtener sedes de la base de datos
        self.sedes = self.db_manager.obtener_sedes()
        sede_names = [s[1] for s in self.sedes] if self.sedes else []

        # Label and Dropdown for "Sede"
        self.sede_label = ctk.CTkLabel(self, text="Sede",font=("Century Gothic", 12, "bold"),text_color="white")
        self.sede_label.grid(row=0, column=0, padx=10, pady=5)
        self.sede_dropdown = ctk.CTkComboBox(self, values=sede_names, command=self.on_sede_selected) 
        self.sede_dropdown.grid(row=0, column=1, padx=10, pady=5)

        # Inicializar laboratorios según la sede seleccionada (si existe)
        self.laboratorios = []

        # Crear el ComboBox de laboratorio con valores vacíos
        self.laboratorio_label = ctk.CTkLabel(self, text="Laboratorio", font=("Century Gothic", 12, "bold"),text_color="white")
        self.laboratorio_label.grid(row=1, column=0, padx=10, pady=5)
        self.laboratorio_dropdown = ctk.CTkComboBox(self, values=[], state="readonly")
        self.laboratorio_dropdown.grid(row=1, column=1, padx=10, pady=5)

        # Si hay sedes, selecciona la primera y actualiza laboratorios
        if sede_names:
            # Selecciona la primera sede por defecto
            self.sede_dropdown.set(sede_names[0])
            # Busca el índice de la sede seleccionada
            selected_sede = self.sede_dropdown.get()
            for idx, sede in enumerate(self.sedes):
                if sede[1] == selected_sede:
                    break
            self.on_sede_selected()

        #Values para la lista de equipos
        self.tipos_equipo = ["Computadora", "Teclado", "Ratón", "Monitor"]

        # Label and Dropdown for "Equipo"
        self.equipo_label = ctk.CTkLabel(self, text="Equipo",font=("Century Gothic", 12, "bold"),text_color="white")
        self.equipo_label.grid(row=2, column=0, padx=10, pady=5)
        self.equipo_dropdown = ctk.CTkComboBox(self, values=self.tipos_equipo, state="readonly")
        self.equipo_dropdown.grid(row=2, column=1, padx=10, pady=5)

        # Label and Dropdown for "Status"
        self.status_label = ctk.CTkLabel(self, text="Status",font=("Century Gothic", 12, "bold"),text_color="white")
        self.status_label.grid(row=3, column=0, padx=10, pady=5)
        values_status = ["Operativo", "No operativo"]
        self.status_dropdown = ctk.CTkComboBox(self, values=values_status, state="readonly")
        self.status_dropdown.grid(row=3, column=1, padx=10, pady=5)

        # Label and Entry for "Número de bien"
        self.nro_bien_label = ctk.CTkLabel(self, text="Número de bien", font=("Century Gothic", 12, "bold"),text_color="white")
        self.nro_bien_label.grid(row=4, column=0, padx=10, pady=5)
        self.nro_bien_entry = ctk.CTkEntry(self)
        self.nro_bien_entry.grid(row=4, column=1, padx=10, pady=5)

        # Add validation for numeric input
        self.nro_bien_entry.configure(validate="key", validatecommand=(self.register(self.validate_numeric), "%S"))

        # Botón "Guardar"
        self.guardar_button = ctk.CTkButton(self, text="Guardar", command=self.guardar_datos,fg_color="dodger blue",
        hover_color="deep sky blue",  # Color cuando pasas el mouse
        border_color="#ffffff",  # Color del borde
        border_width=2,  # Grosor del borde
        text_color="#ffffff",
        font=("Century Gothic", 14, "bold"),
        corner_radius=10)
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

        # Obtener el ID del laboratorio seleccionado
        laboratorio_id = None
        for l in self.laboratorios:
            if l[1] == laboratorio:
                laboratorio_id = l[0]
                break
        if laboratorio_id is None:
            messagebox.showerror("Error", "Laboratorio no válido.")
            return

        # Guardar en la base de datos
        exito = self.db_manager.agregar_equipo(nro_bien, laboratorio_id, status, equipo)
        if exito:
            messagebox.showinfo("Éxito", "Equipo guardado correctamente.")
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "No se pudo guardar el equipo. Puede que ya exista.")

    def limpiar_campos(self):
        # Limpiar todos los campos de entrada y restablecer los dropdowns
        if self.sede_dropdown.cget("values"):
            self.sede_dropdown.set(self.sede_dropdown.cget("values")[0])
            self.on_sede_selected()
        if self.lab_names:
            self.laboratorio_dropdown.set(self.lab_names[0])
        else:
            self.laboratorio_dropdown.set("")
       
        self.equipo_dropdown.set("")
        self.status_dropdown.set("")
        self.nro_bien_entry.delete(0, tk.END)

    def update_laboratorios(self):
        selected_sede_name = self.sede_dropdown.get()
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
        self.laboratorio_dropdown.set("")
        self.laboratorio_dropdown.configure(values=self.lab_names)
        if self.lab_names:
            self.laboratorio_dropdown.set(self.lab_names[0])
        else:
            self.laboratorio_dropdown.set("")

class ModificarEquipo(ctk.CTkFrame):
    def __init__(self, parent=None, db_manager=None):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = db_manager

        # Cambiar el color del fondo a navy
        self.configure(fg_color="navy")

        # Label "Número de bien del equipo"
        self.nro_bien_label = ctk.CTkLabel(self, text="Número de bien del equipo",font=("Century Gothic", 14, "bold"),text_color="white")
        self.nro_bien_label.grid(row=0, column=0, padx=10, pady=5)

        # Entry for "Número de bien del equipo"
        self.nro_bien_entry = ctk.CTkEntry(self)
        self.nro_bien_entry.grid(row=0, column=1, padx=10, pady=5)

        # Add validation for numeric input
        self.nro_bien_entry.configure(validate="key", validatecommand=(self.register(self.validate_numeric), "%S"))

        # Button "Buscar"
        self.buscar_button = ctk.CTkButton(self, text="Buscar", command=self.buscar_equipo, fg_color="dodger blue",
        hover_color="deep sky blue",  # Color cuando pasas el mouse
        border_color="#ffffff",  # Color del borde
        border_width=2,  # Grosor del borde
        text_color="#ffffff",
        font=("Century Gothic", 14, "bold"),
        corner_radius=10)
        self.buscar_button.grid(row=0, column=2, padx=10, pady=5)

        # Placeholders for dynamic widgets
        self.sede_label = None
        self.sede_dropdown = None
        self.laboratorio_label = None
        self.laboratorio_dropdown = None
        self.equipo_label = None
        self.equipo_dropdown = None
        self.status_label = None
        self.status_dropdown = None
        self.nuevo_nro_bien_label = None
        self.nuevo_nro_bien_entry = None
        self.actualizar_button = None

    def validate_numeric(self, char):
        return char.isdigit()

    def buscar_equipo(self):
        nro_bien = self.nro_bien_entry.get()
        if not nro_bien.strip():
            messagebox.showerror("Error", "El campo 'Número de bien del equipo' no puede estar vacío.")
            return

        equipo_data = self.db_manager.buscar_equipo_por_nro_bien(nro_bien)
        if not equipo_data:
            messagebox.showerror("Error", "No se encontró un equipo con ese número de bien.")
            return

        self.display_fields(equipo_data)

    def display_fields(self, equipo_data):
        # Limpiar widgets previos si existen
        for widget in [self.sede_label, self.sede_dropdown, self.laboratorio_label, self.laboratorio_dropdown,
                       self.equipo_label, self.equipo_dropdown, self.status_label, self.status_dropdown,
                       self.nuevo_nro_bien_label, self.nuevo_nro_bien_entry, self.actualizar_button]:
            if widget:
                widget.destroy()

        # Obtener sedes y laboratorios
        self.sedes = self.db_manager.obtener_sedes()
        sede_names = [s[1] for s in self.sedes] if self.sedes else []

        # Sede
        self.sede_label = ctk.CTkLabel(self, text="Sede", font=("Century Gothic", 14, "bold"),text_color="white")
        self.sede_label.grid(row=1, column=0, padx=10, pady=5)
        self.sede_dropdown = ctk.CTkComboBox(self, values=sede_names, state="readonly", command=self.on_sede_selected)
        self.sede_dropdown.grid(row=1, column=1, padx=10, pady=5)
        self.sede_dropdown.set(equipo_data["sede_nombre"])

        # Laboratorios para la sede seleccionada
        self.update_laboratorios()
        self.laboratorio_label = ctk.CTkLabel(self, text="Laboratorio",font=("Century Gothic", 14, "bold"),text_color="white")
        self.laboratorio_label.grid(row=2, column=0, padx=10, pady=5)
        self.laboratorio_dropdown = ctk.CTkComboBox(self, values=self.lab_names, state="readonly")
        self.laboratorio_dropdown.grid(row=2, column=1, padx=10, pady=5)
        self.laboratorio_dropdown.set(equipo_data["laboratorio_nombre"])

        # Tipos de equipo
        tipos_por_defecto = ["Computadora", "Teclado", "Ratón", "Monitor"]
        self.tipos_equipo = self.db_manager.obtener_tipos_equipo()
        # Unir los tipos de la base de datos con los por defecto, sin duplicados
        tipos_set = set(self.tipos_equipo) | set(tipos_por_defecto)
        self.tipos_equipo = list(tipos_set)

        self.equipo_label = ctk.CTkLabel(self, text="Equipo",font=("Century Gothic", 14, "bold"),text_color="white")
        self.equipo_label.grid(row=3, column=0, padx=10, pady=5)
        self.equipo_dropdown = ctk.CTkComboBox(self, values=self.tipos_equipo, state="readonly")
        self.equipo_dropdown.grid(row=3, column=1, padx=10, pady=5)
        self.equipo_dropdown.set(equipo_data["descripcion_equipo"])

        # Status
        self.status_label = ctk.CTkLabel(self, text="Status",font=("Century Gothic", 14, "bold"),text_color="white")
        self.status_label.grid(row=4, column=0, padx=10, pady=5)
        values_status = ["Operativo", "No operativo"]
        self.status_dropdown = ctk.CTkComboBox(self, values=values_status, state="readonly")
        self.status_dropdown.grid(row=4, column=1, padx=10, pady=5)
        self.status_dropdown.set(equipo_data["status"])

        # Número de bien
        self.nuevo_nro_bien_label = ctk.CTkLabel(self, text="Nuevo número de bien",font=("Century Gothic", 14, "bold"),text_color="white")
        self.nuevo_nro_bien_label.grid(row=5, column=0, padx=10, pady=5)
        self.nuevo_nro_bien_entry = ctk.CTkEntry(self)
        self.nuevo_nro_bien_entry.grid(row=5, column=1, padx=10, pady=5)
        self.nuevo_nro_bien_entry.insert(0, str(equipo_data["nro_bien"]))
        

        # Botón Actualizar
        if not self.actualizar_button:
            self.actualizar_button = ctk.CTkButton(self, text="Actualizar", command=self.actualizar_datos, fg_color="dodger blue",
            hover_color="deep sky blue",  # Color cuando pasas el mouse
            border_color="#ffffff",  # Color del borde
            border_width=2,  # Grosor del borde
            text_color="#ffffff",
            font=("Century Gothic", 14, "bold"),
            corner_radius=10)
            self.actualizar_button.grid(row=6, column=0, columnspan=2, pady=10)

    def update_laboratorios(self):
        selected_sede_name = self.sede_dropdown.get()
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
        self.laboratorio_dropdown.configure(values=self.lab_names)
        if self.lab_names:
            self.laboratorio_dropdown.set(self.lab_names[0])
        else:
            self.laboratorio_dropdown.set("")

    def actualizar_datos(self):
        # Recoger datos de los campos
        nro_bien_actual = self.nro_bien_entry.get()
        sede = self.sede_dropdown.get()
        laboratorio = self.laboratorio_dropdown.get()
        equipo = self.equipo_dropdown.get()
        status = self.status_dropdown.get()
        nuevo_nro_bien = self.nuevo_nro_bien_entry.get()

        # Validar que no estén vacíos
        if not sede or not laboratorio or not equipo or not status or not nro_bien_actual.strip() or not nuevo_nro_bien.strip():
            messagebox.showerror("Error", "Todos los campos deben estar llenos.")
            return

        # Obtener el ID del laboratorio seleccionado
        laboratorio_id = None
        for l in self.laboratorios:
            if l[1] == laboratorio:
                laboratorio_id = l[0]
                break
        if laboratorio_id is None:
            messagebox.showerror("Error", "Laboratorio no válido.")
            return

        # Actualizar en la base de datos (incluyendo posible cambio de nro de bien)
        exito = self.db_manager.actualizar_equipo_con_nuevo_nro_bien(
            nro_bien_actual, nuevo_nro_bien, laboratorio_id, status, equipo
        )
        if exito:
            messagebox.showinfo("Éxito", "Datos del equipo actualizados correctamente.")
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el equipo. Puede que el nuevo número de bien ya exista.")

    def limpiar_campos(self):
        # Limpiar el campo de búsqueda y destruir widgets dinámicos
        self.nro_bien_entry.delete(0, tk.END)
        for widget in [self.sede_label, self.sede_dropdown, self.laboratorio_label, self.laboratorio_dropdown,
                       self.equipo_label, self.equipo_dropdown, self.status_label, self.status_dropdown,
                       self.nuevo_nro_bien_label, self.nuevo_nro_bien_entry, self.actualizar_button]:
            if widget:
                widget.destroy()
        self.sede_label = None
        self.sede_dropdown = None
        self.laboratorio_label = None
        self.laboratorio_dropdown = None
        self.equipo_label = None
        self.equipo_dropdown = None
        self.status_label = None
        self.status_dropdown = None
        self.nuevo_nro_bien_label = None
        self.nuevo_nro_bien_entry = None
        self.actualizar_button = None

class RelacionarEquipos(ctk.CTkFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = DBManager()  # Instanciar DBManager

         # Cambiar el color del fondo a navy
        self.configure(fg_color="navy")

        # Title
        self.title_label = ctk.CTkLabel(self, text="Ingresa los números de bien a relacionar", font=("Century Gothic", 20, "bold"),text_color="white")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Label and Entry for "Computadora"
        self.computadora_label = ctk.CTkLabel(self, text="Computadora",font=("Century Gothic", 12, "bold"),text_color="white")
        self.computadora_label.grid(row=1, column=0, padx=10, pady=5)
        self.computadora_entry = ctk.CTkEntry(self)
        self.computadora_entry.grid(row=1, column=1, padx=10, pady=5)
        self.computadora_entry.configure(validate="key", validatecommand=(self.register(self.validate_numeric), "%S"))

        # Label and Entry for "Teclado"
        self.teclado_label = ctk.CTkLabel(self, text="Teclado",font=("Century Gothic", 12, "bold"),text_color="white")
        self.teclado_label.grid(row=2, column=0, padx=10, pady=5)
        self.teclado_entry = ctk.CTkEntry(self)
        self.teclado_entry.grid(row=2, column=1, padx=10, pady=5)
        self.teclado_entry.configure(validate="key", validatecommand=(self.register(self.validate_numeric), "%S"))

        # Label and Entry for "Monitor"
        self.monitor_label = ctk.CTkLabel(self, text="Monitor",font=("Century Gothic", 12, "bold"),text_color="white")
        self.monitor_label.grid(row=3, column=0, padx=10, pady=5)
        self.monitor_entry = ctk.CTkEntry(self)
        self.monitor_entry.grid(row=3, column=1, padx=10, pady=5)
        self.monitor_entry.configure(validate="key", validatecommand=(self.register(self.validate_numeric), "%S"))

        # Label and Entry for "Ratón"
        self.raton_label = ctk.CTkLabel(self, text="Ratón",font=("Century Gothic", 12, "bold"),text_color="white")
        self.raton_label.grid(row=4, column=0, padx=10, pady=5)
        self.raton_entry = ctk.CTkEntry(self)
        self.raton_entry.grid(row=4, column=1, padx=10, pady=5)
        self.raton_entry.configure(validate="key", validatecommand=(self.register(self.validate_numeric), "%S"))

        # Button "Relacionar"
        self.relacionar_button = ctk.CTkButton(self, text="Relacionar", command=self.relacionar_equipos, fg_color="dodger blue",
        hover_color="deep sky blue",  # Color cuando pasas el mouse
        border_color="#ffffff",  # Color del borde
        border_width=2,  # Grosor del borde
        text_color="#ffffff",
        font=("Century Gothic", 14, "bold"),
        corner_radius=10)
        self.relacionar_button.grid(row=5, column=0, columnspan=2, pady=10)

    def validate_numeric(self, char):
        return char.isdigit()

    def relacionar_equipos(self):
        computadora = self.computadora_entry.get()
        teclado = self.teclado_entry.get()
        monitor = self.monitor_entry.get()
        raton = self.raton_entry.get()

        # Validar que no estén vacíos
        if not computadora.strip() or not teclado.strip() or not monitor.strip() or not raton.strip():
            messagebox.showerror("Error", "Todos los campos deben estar llenos.")
            return

        # Verificar existencia y tipo de cada número de bien
        errores = []
        checks = [
            (computadora, "Computadora"),
            (teclado, "Teclado"),
            (monitor, "Monitor"),
            (raton, "Ratón"),
        ]
        for nro, tipo in checks:
            existe, msg = self.db_manager.existe_equipo(nro, tipo)
            if not existe:
                errores.append(msg)

        if errores:
            messagebox.showerror("Error", "\n".join(errores))
            return

        # Registrar la relación en la base de datos
        exito = self.db_manager.relacionar_equipos(computadora, teclado, monitor, raton)
        if exito:
            messagebox.showinfo(
                "Éxito",
                f"Equipos relacionados:\nComputadora: {computadora}\nTeclado: {teclado}\nMonitor: {monitor}\nRatón: {raton}"
            )
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "No se pudo registrar la relación de equipos.")

    def limpiar_campos(self):
        # Limpiar todos los campos de entrada
        self.computadora_entry.delete(0, tk.END)
        self.teclado_entry.delete(0, tk.END)
        self.monitor_entry.delete(0, tk.END)
        self.raton_entry.delete(0, tk.END)
        self.limpiar_campos()
        
    def limpiar_campos(self):
        # Limpiar todos los campos de entrada
        self.computadora_entry.delete(0, tk.END)
        self.teclado_entry.delete(0, tk.END)
        self.monitor_entry.delete(0, tk.END)
        self.raton_entry.delete(0, tk.END)

