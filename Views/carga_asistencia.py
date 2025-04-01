import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import ttk, Canvas, Scrollbar

# ...existing code...

class CargaAsistencia(ctk.CTkFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

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
        
        # ...existing code...
        
        # Dropdown list and Label for "Nombre de laboratorio"
        values_lab=["Laboratorio 1", "Laboratorio 2"]#recuperar de la BD
        self.entry_laboratorio = ctk.CTkComboBox(self.scrollable_frame, values=values_lab, state="readonly")
        self.entry_laboratorio.grid(row=1, column=3, padx=10, pady=10)
        
        self.label_laboratorio = ctk.CTkLabel(self.scrollable_frame, text="Laboratorio")
        self.label_laboratorio.grid(row=1, column=2, padx=10, pady=10)

        # Dropdown list and Label for "Sede"
        values_sede=["Villa asia", "Atlantico"]#recuperar de la BD  
        self.entry_sede = ctk.CTkComboBox(self.scrollable_frame, values=values_sede, state="readonly")
        self.entry_sede.grid(row=1, column=1, padx=10, pady=10)
        
        self.label_sede = ctk.CTkLabel(self.scrollable_frame, text="Sede")
        self.label_sede.grid(row=1, column=0, padx=10, pady=10)
        
        # DateEntry y Label para "Fecha"
        self.entry_fecha = DateEntry(self.scrollable_frame,date_pattern="dd/mm/yyyy")
        self.entry_fecha.grid(row=1, column=5, padx=10, pady=10)
        
        self.label_fecha = ctk.CTkLabel(self.scrollable_frame, text="Fecha")
        self.label_fecha.grid(row=1, column=4, padx=10, pady=10)
        
        # Dropdown lists for "Hora de inicio"
        self.label_hora_inicio = ctk.CTkLabel(self.scrollable_frame, text="Hora de inicio")
        self.label_hora_inicio.grid(row=3, column=0, padx=10, pady=10)

        self.entry_hora_inicio_horas = ctk.CTkComboBox(self.scrollable_frame, values=[str(i) for i in range(24)], width=60)
        self.entry_hora_inicio_horas.grid(row=3, column=1, padx=5, pady=10)

        self.entry_hora_inicio_minutos = ctk.CTkComboBox(self.scrollable_frame, values=[str(i) for i in range(60)], width=60)
        self.entry_hora_inicio_minutos.grid(row=3, column=2, padx=5, pady=10)

        # Dropdown lists for "Hora de finalización"
        self.label_hora_finalizacion = ctk.CTkLabel(self.scrollable_frame, text="Hora de finalización")
        self.label_hora_finalizacion.grid(row=3, column=3, padx=10, pady=10)

        self.entry_hora_finalizacion_horas = ctk.CTkComboBox(self.scrollable_frame, values=[str(i) for i in range(24)], width=60)
        self.entry_hora_finalizacion_horas.grid(row=3, column=4, padx=5, pady=10)

        self.entry_hora_finalizacion_minutos = ctk.CTkComboBox(self.scrollable_frame, values=[str(i) for i in range(60)], width=60)
        self.entry_hora_finalizacion_minutos.grid(row=3, column=5, padx=5, pady=10)

        # Add title
        self.label_titulo = ctk.CTkLabel(self.scrollable_frame, text="Datos de persona", font=("Arial", 24))
        self.label_titulo.grid(row=5, column=0, columnspan=6, pady=20)
        
        # Add labels and entries for personal data
        self.label_tipo_usuario = ctk.CTkLabel(self.scrollable_frame, text="Tipo de uso")
        self.label_tipo_usuario.grid(row=6, column=0, padx=10, pady=10)
        values = ["Servicios de internet", "Atención al usuario", 
                  "Apoyo al estudiante en asesorías con sus equipos, profesores, preparadores",
                  "Talleres de capacitacion al personal administrativo y docente", 
                  "Apoyo en actividades a otras instituciones"] #Recuperar de la BD
        self.entry_tipo_usuario = ctk.CTkComboBox(self.scrollable_frame, values=values)
        self.entry_tipo_usuario.grid(row=6, column=1, padx=10, pady=10)
        
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
        self.entry_cedula = ctk.CTkEntry(self.scrollable_frame)
        self.entry_cedula.grid(row=9, column=1, padx=10, pady=10)

        # Entry y Label para "Organización"
        self.label_organizacion = ctk.CTkLabel(self.scrollable_frame, text="Organización")
        self.label_organizacion.grid(row=9, column=2, padx=10, pady=10)
        self.entry_organizacion = ctk.CTkEntry(self.scrollable_frame)
        self.entry_organizacion.grid(row=9, column=3, padx=10, pady=10)
        
        self.label_telefono = ctk.CTkLabel(self.scrollable_frame, text="Telefono")
        self.label_telefono.grid(row=9, column=4, padx=10, pady=10)
        self.entry_telefono = ctk.CTkEntry(self.scrollable_frame)
        self.entry_telefono.grid(row=9, column=5, padx=10, pady=10)
        
        self.label_numero_bien = ctk.CTkLabel(self.scrollable_frame, text="Numero de bien")
        self.label_numero_bien.grid(row=10, column=2, padx=10, pady=10)
        self.entry_numero_bien = ctk.CTkEntry(self.scrollable_frame)
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
        for i in range(cantidad):
            label_nro_bien = ctk.CTkLabel(self.scrollable_frame, text=f"Nro de bien del equipo {i+1}")
            entry_nro_bien = ctk.CTkEntry(self.scrollable_frame)
            label_descripcion = ctk.CTkLabel(self.scrollable_frame, text=f"Descripcion {i+1}")
            entry_descripcion = ctk.CTkEntry(self.scrollable_frame)
            
            # Add labels and entries for registering the time of the failure
            label_hora_falla = ctk.CTkLabel(self.scrollable_frame, text=f"Hora de la falla {i+1}")
            entry_hora_falla_horas = ctk.CTkComboBox(self.scrollable_frame, values=[str(h) for h in range(24)], width=60)
            entry_hora_falla_minutos = ctk.CTkComboBox(self.scrollable_frame, values=[str(m) for m in range(60)], width=60)

            label_nro_bien.grid(row=16+i, column=0, padx=10, pady=10)
            entry_nro_bien.grid(row=16+i, column=1, padx=10, pady=10)
            label_descripcion.grid(row=16+i, column=2, padx=10, pady=10)
            entry_descripcion.grid(row=16+i, column=3, padx=10, pady=10)
            
            # Place the time of failure widgets
            label_hora_falla.grid(row=16+i, column=4, padx=10, pady=10)
            entry_hora_falla_horas.grid(row=16+i, column=5, padx=5, pady=10)
            entry_hora_falla_minutos.grid(row=16+i, column=6, padx=5, pady=10)

            self.equipos_entries.append((label_nro_bien, entry_nro_bien, label_descripcion, entry_descripcion, label_hora_falla, entry_hora_falla_horas, entry_hora_falla_minutos))
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

    def añadir_persona(self):
        tipo_usuario = self.entry_tipo_usuario.get()
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
        self.entry_tipo_usuario.set('')
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
        # Add your submit logic here
        pass
