import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import ttk  # Import ttk for Combobox
from tkinter import messagebox  # Import messagebox for validation alerts

class AnalizadorPDF(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Title
        self.label_title = ctk.CTkLabel(self, text="Carga de asistencia estudiantes", font=("Arial", 20))
        self.label_title.grid(row=0, column=3, columnspan=4, pady=20, sticky="ew")
        
        # Sede
        self.label_sede = ctk.CTkLabel(self, text="Sede")
        self.label_sede.grid(row=1, column=1, padx=10, pady=10)
        values_sede = ["Villa asia", "Atlantico"]#recuperar de la bd
        self.entry_sede = ctk.CTkComboBox(self, values=values_sede, state="readonly")
        self.entry_sede.grid(row=1, column=2, padx=10, pady=10)
        
        # Laboratorio
        self.label_laboratorio = ctk.CTkLabel(self, text="Laboratorio")
        self.label_laboratorio.grid(row=1, column=3, padx=10, pady=10)
        values_lab= ["Villa asia", "Atlantico"]#recuperar de la bd
        self.entry_laboratorio = ctk.CTkComboBox(self, values=values_lab, state="readonly")
        self.entry_laboratorio.grid(row=1, column=4, padx=10, pady=10)
        
        # Fecha
        self.label_fecha = ctk.CTkLabel(self, text="Fecha")
        self.label_fecha.grid(row=1, column=5, padx=10, pady=10)
        self.entry_fecha = DateEntry(self, date_pattern='dd/mm/y')
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
            label_nro_bien.grid(row=5+i, column=1, padx=10, pady=10)
            entry_nro_bien.grid(row=5+i, column=2, padx=10, pady=10)
            label_descripcion.grid(row=5+i, column=3, padx=10, pady=10)
            entry_descripcion.grid(row=5+i, column=4, padx=10, pady=10)
            self.equipos_entries.append((label_nro_bien, entry_nro_bien, label_descripcion, entry_descripcion))
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


