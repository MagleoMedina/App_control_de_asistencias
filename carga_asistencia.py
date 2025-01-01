import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import ttk

# ...existing code...

class CargaAsistencia(ctk.CTkFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
                 
        # Add title
        self.label_titulo = ctk.CTkLabel(self, text="Carga de asistencia", font=("Arial", 24))
        self.label_titulo.grid(row=0, column=0, columnspan=6, pady=20)
        
        # ...existing code...
        
        #self.entry_usuario = ctk.CTkEntry(self)
        #username = "Magleo"  # Get username from logged in user
        #self.entry_usuario.insert(0, username)  # Set default value
        #self.entry_usuario.configure(state="readonly")
        #self.entry_usuario.grid(row=1, column=1, padx=10, pady=10)
        #self.label_usuario = ctk.CTkLabel(self, text="Nombre de usuario")
        #self.label_usuario.grid(row=1, column=0, padx=10, pady=10)
        
        # Entry y Label para "Nombre de laboratorio"
        self.entry_laboratorio = ctk.CTkEntry(self)
        self.entry_laboratorio.grid(row=1, column=2, padx=10, pady=10)
        
        self.label_laboratorio = ctk.CTkLabel(self, text="Nombre de laboratorio")
        self.label_laboratorio.grid(row=1, column=1, padx=10, pady=10)
        
        # DateEntry y Label para "Fecha"
        self.entry_fecha = DateEntry(self,date_pattern="dd/mm/yyyy")
        self.entry_fecha.grid(row=1, column=4, padx=10, pady=10)
        
        self.label_fecha = ctk.CTkLabel(self, text="Fecha")
        self.label_fecha.grid(row=1, column=3, padx=10, pady=10)
        
        # Dropdown lists for "Hora de inicio"
        self.label_hora_inicio = ctk.CTkLabel(self, text="Hora de inicio")
        self.label_hora_inicio.grid(row=3, column=0, padx=10, pady=10)

        self.entry_hora_inicio_horas = ctk.CTkComboBox(self, values=[str(i) for i in range(24)], width=50)
        self.entry_hora_inicio_horas.grid(row=3, column=1, padx=5, pady=10)

        self.entry_hora_inicio_minutos = ctk.CTkComboBox(self, values=[str(i) for i in range(60)], width=50)
        self.entry_hora_inicio_minutos.grid(row=3, column=2, padx=5, pady=10)

        # Dropdown lists for "Hora de finalización"
        self.label_hora_finalizacion = ctk.CTkLabel(self, text="Hora de finalización")
        self.label_hora_finalizacion.grid(row=3, column=3, padx=10, pady=10)

        self.entry_hora_finalizacion_horas = ctk.CTkComboBox(self, values=[str(i) for i in range(24)], width=50)
        self.entry_hora_finalizacion_horas.grid(row=3, column=4, padx=5, pady=10)

        self.entry_hora_finalizacion_minutos = ctk.CTkComboBox(self, values=[str(i) for i in range(60)], width=50)
        self.entry_hora_finalizacion_minutos.grid(row=3, column=5, padx=5, pady=10)

        # Add title
        self.label_titulo = ctk.CTkLabel(self, text="Datos de persona", font=("Arial", 24))
        self.label_titulo.grid(row=5, column=0, columnspan=6, pady=20)
        
        # Add labels and entries for personal data
        self.label_tipo_usuario = ctk.CTkLabel(self, text="Tipo de usuario")
        self.label_tipo_usuario.grid(row=6, column=0, padx=10, pady=10)
        self.entry_tipo_usuario = ctk.CTkComboBox(self, values=["profesor", "personal administrativo", "foraneo"], command=self.on_tipo_usuario_change)
        self.entry_tipo_usuario.grid(row=6, column=1, padx=10, pady=10)
        
        self.label_nombre = ctk.CTkLabel(self, text="Nombre")
        self.label_nombre.grid(row=6, column=2, padx=10, pady=10)
        self.entry_nombre = ctk.CTkEntry(self)
        self.entry_nombre.grid(row=6, column=3, padx=10, pady=10)
        
        self.label_apellido = ctk.CTkLabel(self, text="Apellido")
        self.label_apellido.grid(row=6, column=4, padx=10, pady=10)
        self.entry_apellido = ctk.CTkEntry(self)
        self.entry_apellido.grid(row=6, column=5, padx=10, pady=10)
        
        self.label_cedula = ctk.CTkLabel(self, text="Cedula")
        self.label_cedula.grid(row=9, column=0, padx=10, pady=10)
        self.entry_cedula = ctk.CTkEntry(self)
        self.entry_cedula.grid(row=9, column=1, padx=10, pady=10)
        
        self.label_telefono = ctk.CTkLabel(self, text="Telefono")
        self.label_telefono.grid(row=9, column=2, padx=10, pady=10)
        self.entry_telefono = ctk.CTkEntry(self)
        self.entry_telefono.grid(row=9, column=3, padx=10, pady=10)
        
        self.label_numero_bien = ctk.CTkLabel(self, text="Numero de bien")
        self.label_numero_bien.grid(row=9, column=4, padx=10, pady=10)
        self.entry_numero_bien = ctk.CTkEntry(self)
        self.entry_numero_bien.grid(row=9, column=5, padx=10, pady=10)
        
        self.label_organizacion = ctk.CTkLabel(self, text="Nombre de organizacion")
        self.entry_organizacion = ctk.CTkEntry(self)
        self.label_direccion = ctk.CTkLabel(self, text="Direccion")
        self.entry_direccion = ctk.CTkEntry(self)
        
        # Hide additional fields initially
        self.hide_foraneo_fields()
        
        self.button_añadir_persona = ctk.CTkButton(self, text="Añadir persona", command=self.añadir_persona)
        self.button_añadir_persona.grid(row=12, column=2, columnspan=2, pady=20)
        
        # Initialize counter
        self.counter = 1
        
        # Create table to display added persons
        self.tree = ttk.Treeview(self, columns=("no", "tipo_usuario", "nombre", "apellido", "cedula", "telefono", "numero_bien", "organizacion", "direccion"), show='headings')
        self.tree.heading("no", text="No")
        self.tree.heading("tipo_usuario", text="Tipo de usuario")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("apellido", text="Apellido")
        self.tree.heading("cedula", text="Cedula")
        self.tree.heading("telefono", text="Telefono")
        self.tree.heading("numero_bien", text="Numero de bien")
        self.tree.heading("organizacion", text="Nombre de organizacion")
        self.tree.heading("direccion", text="Direccion")
        
        # Set column widths
        self.tree.column("no", width=50)
        self.tree.column("tipo_usuario", width=100)
        self.tree.column("nombre", width=100)
        self.tree.column("apellido", width=100)
        self.tree.column("cedula", width=100)
        self.tree.column("telefono", width=100)
        self.tree.column("numero_bien", width=100)
        self.tree.column("organizacion", width=150)
        self.tree.column("direccion", width=150)
        
        self.tree.grid(row=13, column=0, columnspan=6, pady=20)
        
        # Initially hide the "organizacion" and "direccion" columns
        self.tree.column("organizacion", width=0, stretch=False)
        self.tree.column("direccion", width=0, stretch=False)

        # Bind double-click event to the table
        self.tree.bind("<Double-1>", self.on_double_click)

        # Add label and radio buttons for "Fallo alguna computadora?"
        self.label_fallo_computadora = ctk.CTkLabel(self, text="Fallo alguna computadora?")
        self.label_fallo_computadora.grid(row=14, column=0, padx=10, pady=10)
        
        self.radio_var = ctk.StringVar(value="no")
        self.radio_si = ctk.CTkRadioButton(self, text="si", variable=self.radio_var, value="si", command=self.on_fallo_computadora_change)
        self.radio_si.grid(row=14, column=1, padx=10, pady=10)
        
        self.radio_no = ctk.CTkRadioButton(self, text="no", variable=self.radio_var, value="no", command=self.on_fallo_computadora_change)
        self.radio_no.grid(row=14, column=2, padx=10, pady=10)
        
        # Labels and entries for "numero de bien" and "Descripcion de la falla"
        self.label_numero_bien_falla = ctk.CTkLabel(self, text="Numero de bien")
        self.entry_numero_bien_falla = ctk.CTkEntry(self)
        self.label_descripcion_falla = ctk.CTkLabel(self, text="Descripcion de la falla")
        self.entry_descripcion_falla = ctk.CTkEntry(self)
        
        # Hide these fields initially
        self.hide_fallo_computadora_fields()

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

    def on_tipo_usuario_change(self, event=None):
        if self.entry_tipo_usuario.get() == "foraneo":
            self.show_foraneo_fields()
            self.tree.column("organizacion", width=100, stretch=True)
            self.tree.column("direccion", width=100, stretch=True)
        else:
            self.hide_foraneo_fields()
            self.tree.column("organizacion", width=0, stretch=False)
            self.tree.column("direccion", width=0, stretch=False)

    def show_foraneo_fields(self):
        self.label_organizacion.grid(row=10, column=0, padx=10, pady=10)
        self.entry_organizacion.grid(row=10, column=1, padx=10, pady=10)
        self.label_direccion.grid(row=10, column=2, padx=10, pady=10)
        self.entry_direccion.grid(row=10, column=3, padx=10, pady=10)

    def hide_foraneo_fields(self):
        self.label_organizacion.grid_forget()
        self.entry_organizacion.grid_forget()
        self.label_direccion.grid_forget()
        self.entry_direccion.grid_forget()

    def on_fallo_computadora_change(self):
        if self.radio_var.get() == "si":
            self.show_fallo_computadora_fields()
        else:
            self.hide_fallo_computadora_fields()

    def show_fallo_computadora_fields(self):
        self.label_numero_bien_falla.grid(row=15, column=0, padx=10, pady=10)
        self.entry_numero_bien_falla.grid(row=15, column=1, padx=10, pady=10)
        self.label_descripcion_falla.grid(row=15, column=2, padx=10, pady=10)
        self.entry_descripcion_falla.grid(row=15, column=3, padx=10, pady=10)

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
        telefono = self.entry_telefono.get()
        numero_bien = self.entry_numero_bien.get()
        organizacion = self.entry_organizacion.get() if tipo_usuario == "foraneo" else ""
        direccion = self.entry_direccion.get() if tipo_usuario == "foraneo" else ""
        
        # Insert the data into the table with the counter
        self.tree.insert("", "end", values=(self.counter, tipo_usuario, nombre, apellido, cedula, telefono, numero_bien, organizacion, direccion))
        
        # Increment the counter
        self.counter += 1
        
        # Clear the entries
        self.entry_tipo_usuario.set('')
        self.entry_nombre.delete(0, 'end')
        self.entry_apellido.delete(0, 'end')
        self.entry_cedula.delete(0, 'end')
        self.entry_telefono.delete(0, 'end')
        self.entry_numero_bien.delete(0, 'end')
        self.entry_organizacion.delete(0, 'end')
        self.entry_direccion.delete(0, 'end')
        self.hide_foraneo_fields()
        self.tree.column("organizacion", width=0, stretch=False)
        self.tree.column("direccion", width=0, stretch=False)

# ...existing code...

