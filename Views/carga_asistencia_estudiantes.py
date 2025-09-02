import customtkinter as ctk
from db_manager import DBManager
from tkcalendar import DateEntry
from tkinter import ttk  # Import ttk for Combobox
from tkinter import messagebox  # Import messagebox for validation alerts

class CargaAsistenciaEstudiantes(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Instanciar DBManager
        self.db_manager = DBManager()

        # Obtener sedes de la base de datos
        self.sedes = self.db_manager.obtener_sedes()
        sede_names = [s[1] for s in self.sedes] if self.sedes else []
        
        # Title
        self.label_title = ctk.CTkLabel(self, text="Carga de asistencia estudiantes", font=("Arial", 20))
        self.label_title.grid(row=0, column=3, columnspan=4, pady=20, sticky="ew")
        
        # Sede
        self.label_sede = ctk.CTkLabel(self, text="Sede")
        self.label_sede.grid(row=1, column=1, padx=10, pady=10)
        self.entry_sede = ctk.CTkComboBox(self, values=sede_names, state="readonly", command=self.on_sede_selected)
        self.entry_sede.grid(row=1, column=2, padx=10, pady=10)

        
        # Inicializar laboratorios según la sede seleccionada
        self.laboratorios = []
        self.lab_names = []
        
        # Laboratorio
        self.label_laboratorio = ctk.CTkLabel(self, text="Laboratorio")
        self.label_laboratorio.grid(row=1, column=3, padx=10, pady=10)
        self.entry_laboratorio = ctk.CTkComboBox(self, values=[], state="readonly")
        self.entry_laboratorio.grid(row=1, column=4, padx=10, pady=10)

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
        
        # Fecha
        self.label_fecha = ctk.CTkLabel(self, text="Fecha")
        self.label_fecha.grid(row=1, column=5, padx=10, pady=10)
        self.entry_fecha = DateEntry(self, date_pattern='dd/mm/y',font=("Arial", 11, "bold"), foreground='#1abc9c', background='#34495e', borderwidth=2, relief='sunken', width=20)
        self.entry_fecha.grid(row=1, column=6, padx=10, pady=10)
        
        # Cantidad de usuarios atendidos
        self.label_cantidad_usuarios = ctk.CTkLabel(self, text="Cantidad de usuarios atendidos")
        self.label_cantidad_usuarios.grid(row=1, column=7, padx=10, pady=10)
        self.entry_cantidad_usuarios = ctk.CTkEntry(self, width=50)
        self.entry_cantidad_usuarios.grid(row=1, column=8, padx=10, pady=10)
        
        # Validation for entry_cantidad_usuarios
        self.entry_cantidad_usuarios.configure(validate="key", validatecommand=(self.register(self.validate_numeric), "%P"))
        
        # Fallo algun equipo?
        self.label_fallo_equipo = ctk.CTkLabel(self, text="Fallo algun equipo?")
        self.label_fallo_equipo.grid(row=3, column=1, padx=10, pady=10)
        
        # Radio buttons
        self.radio_var = ctk.StringVar(value="")
        self.radio_si = ctk.CTkRadioButton(self, text="Si", variable=self.radio_var, value="Si", command=self.on_radio_change)
        self.radio_si.grid(row=3, column=2, padx=10, pady=10)
        self.radio_no = ctk.CTkRadioButton(self, text="No", variable=self.radio_var, value="No", command=self.on_radio_change)
        self.radio_no.grid(row=3, column=3, padx=10, pady=10)
        
        # Button
        self.btn_submit = ctk.CTkButton(self, text="Submit", command=self.validate_and_submit)
        # Initially hide the submit button
        self.btn_submit.grid(row=2, column=4, padx=10, pady=10)
        self.btn_submit.grid_remove()
        
        # Additional widgets for "Si" option
        self.label_cantidad_equipos = ctk.CTkLabel(self, text="Cantidad de equipos")
        self.combo_cantidad_equipos = ttk.Combobox(self, values=[1, 2, 3, 4, 5], state="readonly")
        self.equipos_entries = []

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

    def on_radio_change(self):
        if self.radio_var.get() == "Si":
            self.label_cantidad_equipos.grid(row=4, column=1, padx=10, pady=10)
            self.combo_cantidad_equipos.grid(row=4, column=2, padx=10, pady=10)
            self.combo_cantidad_equipos.bind("<<ComboboxSelected>>", self.on_cantidad_equipos_change)
            self.btn_submit.grid_forget()
        else:
            self.label_cantidad_equipos.grid_forget()
            self.combo_cantidad_equipos.grid_forget()
            self.clear_equipos_entries()
            self.btn_submit.grid(row=4, column=4, padx=10, pady=10)
        
        if self.radio_var.get() == "No":
            self.btn_submit.grid(row=4, column=4, padx=10, pady=10)
        else:
            self.btn_submit.grid_remove()

    def on_cantidad_equipos_change(self, event):
        self.clear_equipos_entries()
        cantidad = int(self.combo_cantidad_equipos.get())
        for i in range(cantidad):
            label_nro_bien = ctk.CTkLabel(self, text=f"Nro de bien del equipo {i+1}")
            entry_nro_bien = ctk.CTkEntry(self, validate="key", validatecommand=(self.register(self.validate_numeric), "%P"))
            label_descripcion = ctk.CTkLabel(self, text=f"Descripcion {i+1}")
            entry_descripcion = ctk.CTkEntry(self)
            label_hora_falla = ctk.CTkLabel(self, text=f"Hora de la falla {i+1}")
            combo_hora =  ctk.CTkComboBox(self, values=[f"{h:02}" for h in range(24)], state="readonly", width=60)
            combo_minutos =  ctk.CTkComboBox(self, values=[f"{m:02}" for m in range(60)], state="readonly", width=60)

            label_nro_bien.grid(row=5+i, column=1, padx=10, pady=10)
            entry_nro_bien.grid(row=5+i, column=2, padx=10, pady=10)
            label_descripcion.grid(row=5+i, column=3, padx=10, pady=10)
            entry_descripcion.grid(row=5+i, column=4, padx=10, pady=10)
            label_hora_falla.grid(row=5+i, column=5, padx=10, pady=10)
            combo_hora.grid(row=5+i, column=6, padx=5, pady=10)
            combo_minutos.grid(row=5+i, column=7, padx=5, pady=10)

            self.equipos_entries.append((label_nro_bien, entry_nro_bien, label_descripcion, entry_descripcion, label_hora_falla, combo_hora, combo_minutos))
        self.btn_submit.grid(row=5+cantidad, column=4, padx=10, pady=10)

    def clear_equipos_entries(self):
        for widgets in self.equipos_entries:
            for widget in widgets:
                widget.grid_forget()
        self.equipos_entries.clear()

    def validate_numeric(self, value_if_allowed):
        if value_if_allowed.isdigit() or value_if_allowed == "":
            return True
        else:
            return False

    def validate_and_submit(self):
        # Check if any field is empty
        if not self.entry_sede.get() or not self.entry_laboratorio.get() or not self.entry_fecha.get() or not self.entry_cantidad_usuarios.get():
            messagebox.showerror("Error", "Todos los campos deben estar llenos.")
            return
        
        if self.radio_var.get() == "Si":
            if not self.combo_cantidad_equipos.get():
                messagebox.showerror("Error", "Seleccione la cantidad de equipos.")
                return
            for widgets in self.equipos_entries:
                for widget in widgets:
                    if isinstance(widget, ctk.CTkEntry) and not widget.get():
                        messagebox.showerror("Error", "Todos los campos deben estar llenos.")
                        return
        
        # If all validations pass, proceed with the submit action
        messagebox.showinfo("Success", "Formulario enviado correctamente.")
        # Add your submit logic here


