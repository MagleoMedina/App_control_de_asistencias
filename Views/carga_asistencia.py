import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import ttk, Canvas, Scrollbar, messagebox
from db_manager import DBManager  # Importar DBManager
import datetime

class TimeInput(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.hour_var = ctk.StringVar(value="00")
        self.hour_entry = ctk.CTkEntry(self, width=40, textvariable=self.hour_var, justify="center")
        self.hour_entry.pack(side="left", padx=2)
        ctk.CTkLabel(self, text=":").pack(side="left")
        self.minute_var = ctk.StringVar(value="00")
        self.minute_entry = ctk.CTkEntry(self, width=40, textvariable=self.minute_var, justify="center")
        self.minute_entry.pack(side="left", padx=2)

    def get_time(self):
        return f"{self.hour_var.get()}:{self.minute_var.get()}"

class CargaAsistencia(ctk.CTkFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # Instanciar DBManager
        self.db_manager = DBManager()

        # Obtener sedes de la base de datos
        self.sedes = self.db_manager.obtener_sedes()
        sede_names = [s[1] for s in self.sedes] if self.sedes else []

        # Color para el canvas y el scrollBar_frame
        color= "#333333"
        
        # Crear un Canvas para permitir el desplazamiento
        self.canvas = Canvas(self, highlightthickness=0, bg= color) #Poner color del fondo xd bg="color"
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color=color) #Poner del mismo color del canvas para que no se vea la separacion fg_color="color"
        
        # Configuración del Scroll
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

       # Ubicar el Canvas y la Scrollbar en la ventana
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Habilitar scroll con la rueda del mouse solo en el área de desplazamiento
        self.scrollable_frame.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel))
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel))

        # Deshabilitar scroll cuando el cursor salga del área desplazable
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))


        # Expandir y permitir redimensionar
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
                 
        # Add title
        self.label_titulo = ctk.CTkLabel(self.scrollable_frame, text="Carga de asistencia", font=("Arial", 24))
        self.label_titulo.grid(row=0, column=0, columnspan=6, pady=20)
        
        # Dropdown list and Label for "Sede"
        self.entry_sede = ctk.CTkComboBox(self.scrollable_frame, values= sede_names,command=self.on_sede_selected)
        self.entry_sede.grid(row=1, column=1, padx=10, pady=10)
        self.label_sede = ctk.CTkLabel(self.scrollable_frame, text="Sede")
        self.label_sede.grid(row=1, column=0, padx=10, pady=10)

        # Inicializar laboratorios según la sede seleccionada
        self.laboratorios = []
        self.lab_names = []

        # Crear el ComboBox de laboratorio con valores vacíos
        self.label_laboratorio = ctk.CTkLabel(self.scrollable_frame, text="Laboratorio")
        self.label_laboratorio.grid(row=1, column=2, padx=10, pady=10)
        self.entry_laboratorio = ctk.CTkComboBox(self.scrollable_frame, values=[], state="readonly")
        self.entry_laboratorio.grid(row=1, column=3, padx=10, pady=10)

        # Si hay sedes, selecciona la primera y actualiza laboratorios
        if sede_names:
            # Selecciona la primera sede por defecto
            self.entry_sede.set(sede_names[0])
            # Busca el índice de la sede seleccionada
            selected_sede = self.entry_sede.get()
            for idx, sede in enumerate(self.sedes):
                if sede[1] == selected_sede:
                    break
            self.on_sede_selected()

        # DateEntry y Label para "Fecha"
        self.entry_fecha = DateEntry(self.scrollable_frame,date_pattern="dd/mm/yyyy",font=("Arial", 11, "bold"), foreground='#1abc9c', background='#34495e', borderwidth=2, relief='sunken', width=20)
        #self.entry_fecha.configure(font=("Arial", 11, "bold"), foreground='#1abc9c', background='#34495e', borderwidth=2, relief='sunken', width=20)
        self.entry_fecha.grid(row=1, column=5, padx=10, pady=10)
        
        self.label_fecha = ctk.CTkLabel(self.scrollable_frame, text="Fecha")
        self.label_fecha.grid(row=1, column=4, padx=10, pady=10)
        
        # Dropdown lists for "Hora de inicio"
        self.label_hora_inicio = ctk.CTkLabel(self.scrollable_frame, text="Hora de inicio")
        self.label_hora_inicio.grid(row=3, column=0, padx=10, pady=10)
        self.time_inicio = TimeInput(self.scrollable_frame)
        self.time_inicio.grid(row=3, column=1, columnspan=2, padx=5, pady=10)

        # Dropdown lists for "Hora de finalización"
        self.label_hora_finalizacion = ctk.CTkLabel(self.scrollable_frame, text="Hora de finalización")
        self.label_hora_finalizacion.grid(row=3, column=3, padx=10, pady=10)
        self.time_finalizacion = TimeInput(self.scrollable_frame)
        self.time_finalizacion.grid(row=3, column=4, columnspan=2, padx=5, pady=10)

        # Add title
        self.label_titulo = ctk.CTkLabel(self.scrollable_frame, text="Datos de persona", font=("Arial", 24))
        self.label_titulo.grid(row=5, column=0, columnspan=6, pady=20)
        
        # Add labels and entries for personal data
        self.label_tipo_usuario = ctk.CTkLabel(self.scrollable_frame, text="Tipo de uso")
        self.label_tipo_usuario.grid(row=6, column=0, padx=10, pady=10)
        
        # Recuperar tipos de uso de la BD
        tipos_uso = self.db_manager.obtener_tipos_uso()
        self.entry_tipo_uso = ctk.CTkComboBox(self.scrollable_frame, values=tipos_uso)
        self.entry_tipo_uso.grid(row=6, column=1, padx=10, pady=10)
        
        self.label_nombre = ctk.CTkLabel(self.scrollable_frame, text="Nombre")
        self.label_nombre.grid(row=6, column=2, padx=10, pady=10)
        self.entry_nombre = ctk.CTkEntry(self.scrollable_frame)
        self.entry_nombre.grid(row=6, column=3, padx=10, pady=10)
        
        self.label_apellido = ctk.CTkLabel(self.scrollable_frame, text="Apellido")
        self.label_apellido.grid(row=6, column=4, padx=10, pady=10)
        self.entry_apellido = ctk.CTkEntry(self.scrollable_frame)
        self.entry_apellido.grid(row=6, column=5, padx=10, pady=10)
        
        self.label_cedula = ctk.CTkLabel(self.scrollable_frame, text="Cedula")
        self.label_cedula.grid(row=9, column=0, padx=10, pady=10)
        vcmd = (self.register(self._validate_numeric), '%P')
        self.entry_cedula = ctk.CTkEntry(self.scrollable_frame, validate="key", validatecommand=vcmd)
        self.entry_cedula.grid(row=9, column=1, padx=10, pady=10)

        # Entry y Label para "Organización"
        self.label_organizacion = ctk.CTkLabel(self.scrollable_frame, text="Organización")
        self.label_organizacion.grid(row=9, column=2, padx=10, pady=10)
        self.entry_organizacion = ctk.CTkEntry(self.scrollable_frame)
        self.entry_organizacion.grid(row=9, column=3, padx=10, pady=10)
        
        self.label_telefono = ctk.CTkLabel(self.scrollable_frame, text="Telefono")
        self.label_telefono.grid(row=9, column=4, padx=10, pady=10)
        self.entry_telefono = ctk.CTkEntry(self.scrollable_frame, validate="key", validatecommand=vcmd)
        self.entry_telefono.grid(row=9, column=5, padx=10, pady=10)

        self.label_numero_bien = ctk.CTkLabel(self.scrollable_frame, text="Numero de bien")
        self.label_numero_bien.grid(row=10, column=2, padx=10, pady=10)
        self.entry_numero_bien = ctk.CTkEntry(self.scrollable_frame, validate="key", validatecommand=vcmd)
        self.entry_numero_bien.grid(row=10, column=3, padx=10, pady=10)
        
        self.button_añadir_persona = ctk.CTkButton(self.scrollable_frame, text="Añadir persona", command=self.añadir_persona)
        self.button_añadir_persona.grid(row=12, column=2, columnspan=2, pady=20)
        
        # Initialize counter
        self.counter = 1
       
        # Create a style
        style = ttk.Style()
        style.configure("Custom.Treeview", 
                        background="#D3D3D3",  # Background color
                        foreground="black",   # Text color
                        rowheight=25,         # Row height
                        fieldbackground="#D3D3D3")  # Field background color
        style.map('Custom.Treeview', background=[('selected', '#347083')])  # Selected row color

        # Create table to display added persons
        self.tree = ttk.Treeview(self.scrollable_frame, columns=("no", "tipo_usuario", "nombre", "apellido", "cedula", "organizacion", "telefono", "numero_bien"), show='headings', style="Custom.Treeview")
        self.tree.heading("no", text="No")
        self.tree.heading("tipo_usuario", text="Tipo de uso")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("apellido", text="Apellido")
        self.tree.heading("cedula", text="Cedula")
        self.tree.heading("organizacion", text="Organización")
        self.tree.heading("telefono", text="Telefono")
        self.tree.heading("numero_bien", text="Numero de bien")
        
        # Set column widths
        self.tree.column("no", width=50)
        self.tree.column("tipo_usuario", width=100)
        self.tree.column("nombre", width=100)
        self.tree.column("apellido", width=100)
        self.tree.column("cedula", width=100)
        self.tree.column("organizacion", width=100)
        self.tree.column("telefono", width=100)
        self.tree.column("numero_bien", width=100)
        
        self.tree.grid(row=13, column=0, columnspan=6, pady=20)
        
        # Bind double-click event to the table
        self.tree.bind("<Double-1>", self.on_double_click)

        # Add label and radio buttons for "Fallo alguna computadora?"
        self.label_fallo_computadora = ctk.CTkLabel(self.scrollable_frame, text="Fallo alguna computadora?")
        self.label_fallo_computadora.grid(row=14, column=0, padx=10, pady=10)
        
        self.radio_var = ctk.StringVar(value="")
        self.radio_si = ctk.CTkRadioButton(self.scrollable_frame, text="si", variable=self.radio_var, value="si", command=self.on_fallo_computadora_change)
        self.radio_si.grid(row=14, column=1, padx=10, pady=10)
        
        self.radio_no = ctk.CTkRadioButton(self.scrollable_frame, text="no", variable=self.radio_var, value="no", command=self.on_fallo_computadora_change)
        self.radio_no.grid(row=14, column=2, padx=10, pady=10)
        
        # Labels and entries for "numero de bien" and "Descripcion de la falla"
        self.label_numero_bien_falla = ctk.CTkLabel(self.scrollable_frame, text="Numero de bien")
        self.entry_numero_bien_falla = ctk.CTkEntry(self.scrollable_frame)
        self.label_descripcion_falla = ctk.CTkLabel(self.scrollable_frame, text="Descripcion de la falla")
        self.entry_descripcion_falla = ctk.CTkEntry(self.scrollable_frame)
        
        # Hide these fields initially
        self.hide_fallo_computadora_fields()

        # Additional widgets for "si" option
        self.label_cantidad_equipos = ctk.CTkLabel(self.scrollable_frame, text="Cantidad de equipos")
        self.combo_cantidad_equipos = ttk.Combobox(self.scrollable_frame, values=[1, 2, 3, 4, 5], state="readonly")
        self.equipos_entries = []

        # Submit button
        self.btn_submit = ctk.CTkButton(self.scrollable_frame, text="Submit", command=self.submit)
        self.btn_submit.grid(row=20, column=4, padx=10, pady=10)
        self.btn_submit.grid_remove()

    def _on_mouse_wheel(self, event):
        """Desplaza el canvas con la rueda del mouse, solo si el cursor NO está sobre la tabla."""
        if self.tree.winfo_containing(event.x_root, event.y_root) == self.tree:
            return  # No hace nada si el cursor está sobre la tabla
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        column = self.tree.identify_column(event.x)
        column_index = int(column.replace('#', '')) - 1
        if column_index == 0:  # Make "No" column read-only
            return
        x, y, width, height = self.tree.bbox(item, column)
        value = self.tree.item(item, "values")[column_index]

        self.entry_edit = ctk.CTkEntry(self.tree, width=width, height=height)
        self.entry_edit.place(x=x, y=y)
        self.entry_edit.insert(0, value)
        self.entry_edit.focus()

        self.entry_edit.bind("<Return>", lambda e: self.save_edit(item, column_index))
        self.entry_edit.bind("<FocusOut>", lambda e: self.entry_edit.destroy())

    def save_edit(self, item, column_index):
        new_value = self.entry_edit.get()
        values = list(self.tree.item(item, "values"))
        values[column_index] = new_value
        self.tree.item(item, values=values)
        self.entry_edit.destroy()

    def on_fallo_computadora_change(self):
        if self.radio_var.get() == "si":
            self.label_cantidad_equipos.grid(row=15, column=0, padx=10, pady=10)
            self.combo_cantidad_equipos.grid(row=15, column=1, padx=10, pady=10)
            self.combo_cantidad_equipos.bind("<<ComboboxSelected>>", self.on_cantidad_equipos_change)
            self.btn_submit.grid_remove()
        else:
            self.label_cantidad_equipos.grid_forget()
            self.combo_cantidad_equipos.grid_forget()
            self.clear_equipos_entries()
            self.btn_submit.grid(row=16, column=4, padx=10, pady=10)

    def on_cantidad_equipos_change(self, event):
        self.clear_equipos_entries()
        cantidad = int(self.combo_cantidad_equipos.get())
        vcmd = (self.register(self._validate_numeric), '%P')
        for i in range(cantidad):
            label_nro_bien = ctk.CTkLabel(self.scrollable_frame, text=f"Nro de bien del equipo {i+1}")
            entry_nro_bien = ctk.CTkEntry(self.scrollable_frame, validate="key", validatecommand=vcmd)
            label_descripcion = ctk.CTkLabel(self.scrollable_frame, text=f"Descripcion {i+1}")
            entry_descripcion = ctk.CTkEntry(self.scrollable_frame)
            label_hora_falla = ctk.CTkLabel(self.scrollable_frame, text=f"Hora de la falla {i+1}")
            time_falla = TimeInput(self.scrollable_frame)

            label_nro_bien.grid(row=16+i, column=0, padx=10, pady=10)
            entry_nro_bien.grid(row=16+i, column=1, padx=10, pady=10)
            label_descripcion.grid(row=16+i, column=2, padx=10, pady=10)
            entry_descripcion.grid(row=16+i, column=3, padx=10, pady=10)
            label_hora_falla.grid(row=16+i, column=4, padx=10, pady=10)
            time_falla.grid(row=16+i, column=5, columnspan=2, padx=5, pady=10)

            self.equipos_entries.append((label_nro_bien, entry_nro_bien, label_descripcion, entry_descripcion, label_hora_falla, time_falla))
        self.btn_submit.grid(row=16+cantidad, column=4, padx=10, pady=10)

    def clear_equipos_entries(self):
        for widgets in self.equipos_entries:
            for widget in widgets:
                widget.grid_forget()
        self.equipos_entries.clear()

    def hide_fallo_computadora_fields(self):
        self.label_numero_bien_falla.grid_forget()
        self.entry_numero_bien_falla.grid_forget()
        self.label_descripcion_falla.grid_forget()
        self.entry_descripcion_falla.grid_forget()

    def update_laboratorios(self):
        selected_sede_name = self.entry_sede.get()
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
        self.entry_laboratorio.set("")
        self.entry_laboratorio.configure(values=self.lab_names)
        if self.lab_names:
            self.entry_laboratorio.set(self.lab_names[0])
        else:
            self.entry_laboratorio.set("")

    def añadir_persona(self):
        tipo_usuario = self.entry_tipo_uso.get()
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        cedula = self.entry_cedula.get()
        organizacion = self.entry_organizacion.get()
        telefono = self.entry_telefono.get()
        numero_bien = self.entry_numero_bien.get()
        
        # Insert the data into the table with the counter
        self.tree.insert("", "end", values=(self.counter, tipo_usuario, nombre, apellido, cedula, organizacion, telefono, numero_bien))
        
        # Increment the counter
        self.counter += 1
        
        # Clear the entries
        self.entry_nombre.delete(0, 'end')
        self.entry_apellido.delete(0, 'end')
        self.entry_cedula.delete(0, 'end')
        self.entry_organizacion.delete(0, 'end')
        self.entry_telefono.delete(0, 'end')
        self.entry_numero_bien.delete(0, 'end')

        # Clear the failure fields if they were filled
        if self.radio_var.get() == "si":
            self.entry_numero_bien_falla.delete(0, 'end')
            self.entry_descripcion_falla.delete(0, 'end')
            self.radio_var.set("")
            self.clear_equipos_entries()

    def submit(self):
        # Recopilar datos generales
        laboratorio_nombre = self.entry_laboratorio.get()
        laboratorio_id = None
        for l in self.laboratorios:
            if l[1] == laboratorio_nombre:
                laboratorio_id = l[0]
                break
        tipo_uso = self.entry_tipo_uso.get()
        fecha = self.entry_fecha.get()
        hora_inicio = self.time_inicio.get_time()
        hora_finalizacion = self.time_finalizacion.get_time()

        # Recopilar personas de la tabla
        personas = []
        for item in self.tree.get_children():
            vals = self.tree.item(item, "values")
            personas.append({
                "tipo_usuario": vals[1],
                "nombre": vals[2],
                "apellido": vals[3],
                "cedula": vals[4],
                "organizacion": vals[5],
                "telefono": vals[6],
                "numero_bien": vals[7]
            })

        # Validación de datos antes de enviar
        if not laboratorio_id:
            messagebox.showerror("Error", "laboratorio_id no seleccionado o inválido.")
            return
        if not tipo_uso:
            messagebox.showerror("Error: tipo_uso no seleccionado o inválido.")
            return
        if not fecha or not hora_inicio or not hora_finalizacion:
            messagebox.showerror("Error: fecha u hora no válidas.")
            return
        if not personas:
            messagebox.showerror("Error: no hay personas para registrar asistencia.")
            return

        # Validar que todos los números de bien existan en la base de datos
        for persona in personas:
            nro_bien = persona["numero_bien"]
            if not nro_bien:
                messagebox.showerror("Error", "El campo 'Numero de bien' no puede estar vacío.")
                return
            equipo = self.db_manager.buscar_equipo_por_nro_bien(nro_bien)
            if equipo is None:
                messagebox.showerror("Error", f"El equipo con número de bien '{nro_bien}' no se encuentra registrado.")
                return

        # Validación de hora de inicio < hora de finalización
        try:
            h_ini = datetime.datetime.strptime(hora_inicio, "%H:%M")
            h_fin = datetime.datetime.strptime(hora_finalizacion, "%H:%M")
            if h_ini >= h_fin:
                messagebox.showerror("Error", "La hora de inicio debe ser menor que la hora de finalización.")
                return
        except Exception:
            messagebox.showerror("Error", "Formato de hora inválido.")
            return

        # Registrar asistencia en la base de datos
        print("Enviando datos a la base de datos...")
        resultado = self.db_manager.registrar_asistencia_laboratorio_usr(
            laboratorio_id, tipo_uso, fecha, hora_inicio, hora_finalizacion, personas
        )
        print(f"Resultado registrar_asistencia_laboratorio_usr: {resultado}")
        if not resultado:
            messagebox.showerror("Error al registrar asistencia en la base de datos.")
            return

        # Si hubo fallas, registrar fallas con descripción y hora
        if self.radio_var.get() == "si" and self.equipos_entries:
            # Obtener IDs de asistencia (últimos N registros)
            asistencias = []
            num_asistencias = len(self.equipos_entries)
            last_ids = self.db_manager.execute_query(
                "SELECT ID FROM Asistencia_usr ORDER BY ID DESC LIMIT ?", (num_asistencias,)
            )
            if last_ids:
                asistencias = [row[0] for row in last_ids]
            for idx, widgets in enumerate(self.equipos_entries):
                nro_bien = widgets[1].get()
                descripcion = widgets[3].get()
                hora_falla = widgets[5].get_time()
                asistencia_id = asistencias[idx] if idx < len(asistencias) else None
                fecha_falla = self.entry_fecha.get()  # Usar la fecha seleccionada
                equipo_id = nro_bien  # El número de bien es el ID del equipo
                if asistencia_id:
                    resultado_falla = self.db_manager.registrar_falla_equipo_completa(
                        asistencia_id, equipo_id, descripcion, fecha_falla, hora_falla
                    )
                    print(f"Resultado registrar_falla_equipo_completa: {resultado_falla}")
                    if not resultado_falla:
                        messagebox.showerror("Error al registrar la falla completa del equipo.")

        # Limpiar todos los campos
        self.entry_sede.set('')
        self.entry_laboratorio.set('')
        self.entry_fecha.set_date(datetime.date.today())
        self.time_inicio.hour_var.set("00")
        self.time_inicio.minute_var.set("00")
        self.time_finalizacion.hour_var.set("00")
        self.time_finalizacion.minute_var.set("00")
        self.entry_tipo_uso.set('')
        self.entry_nombre.delete(0, 'end')
        self.entry_apellido.delete(0, 'end')
        self.entry_cedula.delete(0, 'end')
        self.entry_organizacion.delete(0, 'end')
        self.entry_telefono.delete(0, 'end')
        self.entry_numero_bien.delete(0, 'end')
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.counter = 1
        self.radio_var.set("")
        self.clear_equipos_entries()
        self.radio_var.set("")
        self.clear_equipos_entries()
        self.clear_equipos_entries()
        self.radio_var.set("")
        self.clear_equipos_entries()

    def _validate_numeric(self, value):
        """Permite solo valores numéricos en los campos."""
        return value.isdigit() or value == ""
