import customtkinter as ctk
from tkinter import messagebox
from db_manager import DBManager

class GestionSedeLaboratorios(ctk.CTkFrame):
    def __init__(self, parent=None, db_manager=None):
        super().__init__(parent)
        self.parent = parent
        self.configure(fg_color="white")
        self.db_manager = db_manager
        self.db_manager.set_parent(self.parent)

        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text="Gestión de Sedes y Laboratorios",
            font=("Century Gothic", 20, "bold"),
            text_color="navy",
        )
        self.title_label.grid(row=0, column=0, columnspan=4, pady=(20, 40), sticky="n")

        btn_kwargs = {
            "width": 140,
            "height": 36,
            "fg_color": "dodger blue",
            "hover_color": "deep sky blue",
            "border_color": "#ffffff",
            "border_width": 2,
            "text_color": "#ffffff",
            "font": ("Century Gothic", 14, "bold"),
            "corner_radius": 10,
        }

      
        self.btn_consultar = ctk.CTkButton(self, text="Consultar Sede", command=self.mostrar_consultar, **btn_kwargs)
        self.btn_consultar.grid(row=1, column=0, padx=10, pady=(0, 30))

        self.btn_agregar = ctk.CTkButton(self, text="Agregar", command=self.mostrar_agregar, **btn_kwargs)
        self.btn_agregar.grid(row=1, column=1, padx=10, pady=(0, 30))

        self.btn_modificar = ctk.CTkButton(self, text="Modificar", command=self.mostrar_modificar, **btn_kwargs)
        self.btn_modificar.grid(row=1, column=2, padx=10, pady=(0, 30))

        self.btn_eliminar = ctk.CTkButton(self, text="Eliminar", command=self.mostrar_eliminar, **btn_kwargs)
        self.btn_eliminar.grid(row=1, column=3, padx=10, pady=(0, 30))

        self.action_buttons = [self.btn_consultar, self.btn_agregar, self.btn_modificar, self.btn_eliminar]

    def clear_frame(self):
        for widget in list(self.winfo_children()):
            if widget not in [self.title_label] + self.action_buttons:
                widget.destroy()

    def mostrar_consultar(self):
        self.clear_frame()
        frame = ConsultarSedeForm(self, db_manager=self.db_manager)
        frame.grid(row=2, column=0, columnspan=4, sticky="n", padx=20, pady=10)

    def mostrar_agregar(self):
        self.clear_frame()
        frame = AgregarForm(self, db_manager=self.db_manager)
        frame.grid(row=2, column=0, columnspan=4, sticky="n", padx=20, pady=10)

    def mostrar_modificar(self):
        self.clear_frame()
        frame = ModificarForm(self, db_manager=self.db_manager)
        frame.grid(row=2, column=0, columnspan=4, sticky="n", padx=20, pady=10)

    def mostrar_eliminar(self):
        self.clear_frame()
        frame = EliminarForm(self, db_manager=self.db_manager)
        frame.grid(row=2, column=0, columnspan=4, sticky="n", padx=20, pady=10)


class ConsultarSedeForm(ctk.CTkFrame):
    def __init__(self, parent=None, db_manager=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.configure(fg_color="navy", height=260, width=620)

        for i in range(3): self.grid_columnconfigure(i, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.title_label = ctk.CTkLabel(self, text="Consultar Sede", font=("Century Gothic", 16, "bold"), text_color="white")
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(10, 20))

        self.sede_label = ctk.CTkLabel(self, text="Seleccione una sede:", font=("Century Gothic", 12), text_color="white")
        self.sede_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.sede_combobox = ctk.CTkComboBox(self, values=[], state="readonly", command=self.mostrar_laboratorios, width=200, font=("Century Gothic", 12),
        border_color="dodger blue",
        button_color="dodger blue",
        fg_color="white",
        button_hover_color="deep sky blue")
        self.sede_combobox.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        self.labs_text = ctk.CTkLabel(self, text="Seleccione una sede para ver sus laboratorios.", font=("Century Gothic", 12), justify="left", wraplength=520, text_color="white")
        self.labs_text.grid(row=3, column=0, columnspan=3, padx=10, pady=15, sticky="nsew")

        self.cargar_sedes()

    def cargar_sedes(self):
        sedes = self.db_manager.obtener_sedes()
        self.sede_ids = [s[0] for s in sedes]
        self.sede_names = [s[1] for s in sedes]
        self.sede_combobox.configure(values=self.sede_names)
        if self.sede_names:
            self.sede_combobox.set(self.sede_names[0])
            self.mostrar_laboratorios()

    def mostrar_laboratorios(self, value=None):
        sede_nombre = self.sede_combobox.get().strip()
        if not sede_nombre or sede_nombre not in self.sede_names:
            self.labs_text.configure(text="Seleccione una sede válida.")
            return

        sede_id = self.sede_ids[self.sede_names.index(sede_nombre)]
        laboratorios = self.db_manager.obtener_laboratorios_por_sede(sede_id)
        if not laboratorios:
            self.labs_text.configure(text="No hay laboratorios asociados a esta sede.")
            return

        self.labs_text.configure(text="\n".join([f"• {lab[1]}" for lab in laboratorios]))



class AgregarForm(ctk.CTkFrame):
    def __init__(self, parent=None, db_manager=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.configure(fg_color="navy", width=550)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        btn_mode_kwargs = {"width": 140, "height": 30, "fg_color": "dodger blue", "hover_color": "deep sky blue", "text_color": "white", "font": ("Century Gothic", 12, "bold")}
        self.mode_sede_button = ctk.CTkButton(self, text="Modo Sede", command=lambda: self.set_mode("sede"), **btn_mode_kwargs)
        self.mode_sede_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.mode_lab_button = ctk.CTkButton(self, text="Modo Laboratorio", command=lambda: self.set_mode("laboratorio"), **btn_mode_kwargs)
        self.mode_lab_button.grid(row=0, column=1, padx=10, pady=10)

        
        self.input_container = ctk.CTkFrame(self, fg_color="transparent")
        self.input_container.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
        self.input_container.grid_columnconfigure(0, weight=1)

    
        self.sede_frame = ctk.CTkFrame(self.input_container, fg_color="transparent")
        self.sede_frame.grid_columnconfigure(0, weight=1)
        
        self.nombre_entry = ctk.CTkEntry(self.sede_frame, placeholder_text="Nombre de la sede", font=("Century Gothic", 12), fg_color="white", border_width=2, border_color="light blue", corner_radius=10)
        self.nombre_entry.grid(row=0, column=0, pady=5, padx=20, sticky="ew")
        self._style_entry(self.nombre_entry)

        self.cantidad_combobox = ctk.CTkComboBox(self.sede_frame, values=[str(i) for i in range(1, 6)], state="readonly", command=self.update_entries, font=("Century Gothic", 12),
        border_color="dodger blue",
        button_color="dodger blue",
        fg_color="white",
        button_hover_color="deep sky blue")
        self.cantidad_combobox.set("1")
        self.cantidad_combobox.grid(row=1, column=0, pady=5, padx=20, sticky="ew")

        self.entries_frame = ctk.CTkFrame(self.sede_frame, fg_color="transparent")
        self.entries_frame.grid(row=2, column=0, pady=5, sticky="ew")
        self.entries_frame.grid_columnconfigure(0, weight=1)
        
        self.lab_entries = []
        for i in range(5):
            entry = ctk.CTkEntry(self.entries_frame, placeholder_text=f"Nombre Laboratorio {i+1}", font=("Century Gothic", 12), fg_color="white", border_width=2, border_color="light blue", corner_radius=10)
            self._style_entry(entry)
            self.lab_entries.append(entry)

        
        self.lab_frame = ctk.CTkFrame(self.input_container, fg_color="transparent")
        self.lab_frame.grid_columnconfigure(0, weight=1)
        
        self.sede_combobox = ctk.CTkComboBox(self.lab_frame, values=[], state="readonly", font=("Century Gothic", 12),
        border_color="dodger blue",
        button_color="dodger blue",
        fg_color="white",
        button_hover_color="deep sky blue")
        self.sede_combobox.grid(row=0, column=0, pady=5, padx=20, sticky="ew")
        
        self.lab_nombre_entry = ctk.CTkEntry(self.lab_frame, placeholder_text="Nombre del laboratorio", font=("Century Gothic", 12), fg_color="white", border_width=2, border_color="light blue", corner_radius=10)
        self.lab_nombre_entry.grid(row=1, column=0, pady=5, padx=20, sticky="ew")
        self._style_entry(self.lab_nombre_entry)

        self.action_button = ctk.CTkButton(self, text="Guardar", command=self.on_guardar, fg_color="dodger blue", hover_color="deep sky blue", text_color="white", font=("Century Gothic", 14, "bold"))
        self.action_button.grid(row=2, column=0, columnspan=2, pady=15)
 
        self.status_label = ctk.CTkLabel(self, text="", font=("Century Gothic", 12), text_color="white")
        self.status_label.grid(row=3, column=0, columnspan=2, pady=5)

        self.set_mode("sede")

    def set_mode(self, mode):
        self.current_mode = mode
        self.status_label.configure(text="")
        if mode == "sede":
            self.lab_frame.grid_forget()
            self.sede_frame.grid(row=0, column=0, pady=10, sticky="ew")
            self.action_button.configure(text="Registrar Sede")
            self.update_entries()
        else:
            self.sede_frame.grid_forget()
            self.lab_frame.grid(row=0, column=0, pady=10, sticky="ew")
            self.action_button.configure(text="Registrar Laboratorio")
            self.cargar_sedes()

    def update_entries(self, value=None):
        cant = int(self.cantidad_combobox.get())
        for i, entry in enumerate(self.lab_entries):
            if i < cant: 
                entry.grid(row=i, column=0, pady=2, padx=20, sticky="ew")
            else: 
                entry.grid_forget()

    def _style_entry(self, entry):
        entry.bind("<Enter>", lambda event, widget=entry: widget.configure(border_color="dodger blue"))
        entry.bind("<Leave>", lambda event, widget=entry: widget.configure(border_color="light blue"))

    def cargar_sedes(self):
        sedes = self.db_manager.obtener_sedes()
        self.sede_ids = [s[0] for s in sedes]
        self.sede_names = [s[1] for s in sedes]
        self.sede_combobox.configure(values=self.sede_names)
        if self.sede_names: self.sede_combobox.set(self.sede_names[0])

    def on_guardar(self):
        self.status_label.configure(text="") 
        
        if self.current_mode == "sede":
            nombre = self.nombre_entry.get().strip()
            if not nombre:
                self.status_label.configure(text="Ingrese el nombre de la sede.", text_color="red")
                return
            
            cant = int(self.cantidad_combobox.get())

            if cant >= 1:
                primer_lab = self.lab_entries[0].get().strip()
                if not primer_lab:
                    respuesta = messagebox.askyesno(
                        "Laboratorio requerido",
                        "La sede debe tener como mínimo un laboratorio asociado. "
                        "Si no escribe un nombre en el campo del laboratorio, el sistema lo denominará Laboratorio 1.\n\n" 
                        "¿Desea agregar el nombre del laboratorio?"
                    )
                    if respuesta:
                        self.status_label.configure(text="Ingrese el nombre del laboratorio antes de guardar.", text_color="orange")
                        return
                    else:
                        self.lab_entries[0].delete(0, "end")
                        self.lab_entries[0].insert(0, "Laboratorio 1")

            nombres_ingresados = []
            for i in range(cant):
                lab_n = self.lab_entries[i].get().strip() or f"Laboratorio {i+1}"
                if lab_n in nombres_ingresados:
                    self.status_label.configure(text=f"Error: Has escrito el nombre '{lab_n}' más de una vez.", text_color="red")
                    return
                nombres_ingresados.append(lab_n)

            
            sede_id = self.db_manager.agregar_sede(nombre)
            if sede_id:
                
                for lab_n in nombres_ingresados:
                    resultado_lab = self.db_manager.agregar_laboratorio(lab_n, sede_id)
                    
                    
                    if not resultado_lab:
                        self.status_label.configure(
                            text=f"Sede creada, pero el '{lab_n}' ya existía.", 
                            text_color="orange"
                        )
                
                messagebox.showinfo("Éxito", "Proceso de registro de Sede finalizado.")
                self.nombre_entry.delete(0, "end")
                for e in self.lab_entries: e.delete(0, "end")
            else:
                self.status_label.configure(text="Error: La sede ya existe o no se pudo crear.", text_color="red")

        else:
            # MODO LABORATORIO INDIVIDUAL
            sede_sel = self.sede_combobox.get()
            lab_n = self.lab_nombre_entry.get().strip()
            
            if not sede_sel or not lab_n:
                self.status_label.configure(text="Complete todos los campos.", text_color="red")
                return
                
            sede_id = self.sede_ids[self.sede_names.index(sede_sel)]
            
            exito = self.db_manager.agregar_laboratorio(lab_n, sede_id)
            
            if exito:
                messagebox.showinfo("Éxito", f"¡'{lab_n}' agregado exitosamente a la sede {sede_sel}!")
                self.lab_nombre_entry.delete(0, "end")
            else:
                
                self.status_label.configure(
                    text=f"El laboratorio '{lab_n}' ya existe en la sede {sede_sel}.\nPor favor, intente con otro nombre.", 
                    text_color="red"
                )


class ModificarForm(ctk.CTkFrame):
    def __init__(self, parent=None, db_manager=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.configure(fg_color="navy", width=500)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        btn_mode_kwargs = {"width": 140, "height": 30, "fg_color": "dodger blue", "hover_color": "deep sky blue", "text_color": "white", "font": ("Century Gothic", 12, "bold")}
        ctk.CTkButton(self, text="Modificar Sede", command=lambda: self.set_mode("sede"), **btn_mode_kwargs).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(self, text="Modificar Lab", command=lambda: self.set_mode("laboratorio"), **btn_mode_kwargs).grid(row=0, column=1, padx=10, pady=10)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
        self.container.grid_columnconfigure(0, weight=1)

        self.sede_label = ctk.CTkLabel(self.container, text="Seleccione Sede:", font=("Century Gothic", 12), text_color="white")
        self.sede_combobox = ctk.CTkComboBox(self.container, values=[], state="readonly", command=self.on_sede_change, font=("Century Gothic", 12),
        border_color="dodger blue",
        button_color="dodger blue",
        fg_color="white",
        button_hover_color="deep sky blue")
        
        self.lab_label = ctk.CTkLabel(self.container, text="Seleccione Laboratorio:", font=("Century Gothic", 12), text_color="white")
        self.lab_combobox = ctk.CTkComboBox(self.container, values=[], state="readonly", font=("Century Gothic", 12),
        border_color="dodger blue",
        button_color="dodger blue",
        fg_color="white",
        button_hover_color="deep sky blue")

        self.nuevo_nombre_label = ctk.CTkLabel(self.container, text="Nuevo Nombre:", font=("Century Gothic", 12), text_color="white")
        self.nuevo_nombre_entry = ctk.CTkEntry(self.container, font=("Century Gothic", 12), fg_color="white", border_width=2, border_color="light blue", corner_radius=10)
        self._style_entry(self.nuevo_nombre_entry)

        self.btn_action = ctk.CTkButton(self, text="Modificar", command=self.on_modificar, fg_color="dodger blue", hover_color="deep sky blue", text_color="white", font=("Century Gothic", 14, "bold"))
        self.btn_action.grid(row=2, column=0, columnspan=2, pady=15)

        self.set_mode("sede")

    def set_mode(self, mode):
        self.current_mode = mode
        
        self.nuevo_nombre_entry.delete(0, "end")
        
        self.sede_label.grid_forget()
        self.sede_combobox.grid_forget()
        self.lab_label.grid_forget()
        self.lab_combobox.grid_forget()
        self.nuevo_nombre_label.grid_forget()
        self.nuevo_nombre_entry.grid_forget()

        self.cargar_sedes()
        
        r = 0
        self.sede_label.grid(row=r, column=0, pady=2)
        r += 1
        self.sede_combobox.grid(row=r, column=0, pady=2, padx=40, sticky="ew")
        r += 1

        if mode == "laboratorio":
            self.lab_label.grid(row=r, column=0, pady=2)
            r += 1
            self.lab_combobox.grid(row=r, column=0, pady=2, padx=40, sticky="ew")
            r += 1
            self.on_sede_change()

        self.nuevo_nombre_label.grid(row=r, column=0, pady=2)
        r += 1
        self.nuevo_nombre_entry.grid(row=r, column=0, pady=2, padx=40, sticky="ew")

    def _style_entry(self, entry):
        entry.bind("<Enter>", lambda event, widget=entry: widget.configure(border_color="dodger blue"))
        entry.bind("<Leave>", lambda event, widget=entry: widget.configure(border_color="light blue"))

    def cargar_sedes(self):
        sedes = self.db_manager.obtener_sedes()
        self.sede_ids = [s[0] for s in sedes]
        self.sede_names = [s[1] for s in sedes]
        self.sede_combobox.configure(values=self.sede_names)
        if self.sede_names: self.sede_combobox.set(self.sede_names[0])

    def on_sede_change(self, value=None):
        if self.current_mode == "laboratorio" and self.sede_combobox.get():
            sede_id = self.sede_ids[self.sede_names.index(self.sede_combobox.get())]
            labs = self.db_manager.obtener_laboratorios_por_sede(sede_id)
            self.lab_ids = [l[0] for l in labs]
            self.lab_names = [l[1] for l in labs]
            self.lab_combobox.configure(values=self.lab_names)
            if self.lab_names: self.lab_combobox.set(self.lab_names[0])

    def on_modificar(self):
        nuevo = self.nuevo_nombre_entry.get().strip()
        if not nuevo: return

        if self.current_mode == "sede":
            sede_id = self.sede_ids[self.sede_names.index(self.sede_combobox.get())]
            if self.db_manager.modificar_sede(sede_id, nuevo):
                messagebox.showinfo("Éxito", "Sede modificada.")
                self.nuevo_nombre_entry.delete(0, "end")
                self.cargar_sedes()
        else:
            lab_id = self.lab_ids[self.lab_names.index(self.lab_combobox.get())]
            if self.db_manager.modificar_laboratorio(lab_id, nuevo):
                messagebox.showinfo("Éxito", "Laboratorio modificado.")
                self.nuevo_nombre_entry.delete(0, "end")
                self.on_sede_change()



class EliminarForm(ctk.CTkFrame):
    def __init__(self, parent=None, db_manager=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.configure(fg_color="navy", width=500)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        btn_mode_kwargs = {"width": 140, "height": 30, "fg_color": "dodger blue", "hover_color": "deep sky blue", "text_color": "white", "font": ("Century Gothic", 12, "bold")}
        ctk.CTkButton(self, text="Eliminar Sede", command=lambda: self.set_mode("sede"), **btn_mode_kwargs).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(self, text="Eliminar Lab", command=lambda: self.set_mode("laboratorio"), **btn_mode_kwargs).grid(row=0, column=1, padx=10, pady=10)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
        self.container.grid_columnconfigure(0, weight=1)

        self.sede_label = ctk.CTkLabel(self.container, text="Seleccione Sede:", font=("Century Gothic", 12), text_color="white")
        self.sede_combobox = ctk.CTkComboBox(self.container, values=[], state="readonly", command=self.on_sede_change, font=("Century Gothic", 12),
        border_color="dodger blue",
        button_color="dodger blue",
        fg_color="white",
        button_hover_color="deep sky blue")
        
        self.lab_label = ctk.CTkLabel(self.container, text="Seleccione Laboratorio:", font=("Century Gothic", 12), text_color="white")
        self.lab_combobox = ctk.CTkComboBox(self.container, values=[], state="readonly", font=("Century Gothic", 12),
        border_color="dodger blue",
        button_color="dodger blue",
        fg_color="white",
        button_hover_color="deep sky blue")

        self.btn_action = ctk.CTkButton(self, text="Eliminar", command=self.on_eliminar, fg_color="red", hover_color="#FF315E", text_color="white", font=("Century Gothic", 14, "bold"))
        self.btn_action.grid(row=2, column=0, columnspan=2, pady=15)

        self.set_mode("sede")

    def set_mode(self, mode):
        self.current_mode = mode
        
        self.sede_label.grid_forget()
        self.sede_combobox.grid_forget()
        self.lab_label.grid_forget()
        self.lab_combobox.grid_forget()
        
        self.cargar_sedes()
        
        r = 0
        self.sede_label.grid(row=r, column=0, pady=2)
        r += 1
        self.sede_combobox.grid(row=r, column=0, pady=2, padx=40, sticky="ew")
        r += 1

        if mode == "laboratorio":
            self.lab_label.grid(row=r, column=0, pady=2)
            r += 1
            self.lab_combobox.grid(row=r, column=0, pady=2, padx=40, sticky="ew")
            r += 1
            self.on_sede_change()

    def cargar_sedes(self):
        sedes = self.db_manager.obtener_sedes()
        self.sede_ids = [s[0] for s in sedes]
        self.sede_names = [s[1] for s in sedes]
        self.sede_combobox.configure(values=self.sede_names)
        if self.sede_names: self.sede_combobox.set(self.sede_names[0])

    def on_sede_change(self, value=None):
        if self.current_mode == "laboratorio" and self.sede_combobox.get():
            sede_id = self.sede_ids[self.sede_names.index(self.sede_combobox.get())]
            labs = self.db_manager.obtener_laboratorios_por_sede(sede_id)
            self.lab_ids = [l[0] for l in labs]
            self.lab_names = [l[1] for l in labs]
            self.lab_combobox.configure(values=self.lab_names)
            if self.lab_names: self.lab_combobox.set(self.lab_names[0])

    def on_eliminar(self):
        if self.current_mode == "sede":
            sede_sel = self.sede_combobox.get()
            if not sede_sel: return
            sede_id = self.sede_ids[self.sede_names.index(sede_sel)]
            if messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar la sede '{sede_sel}'?"):
                if self.db_manager.eliminar_sede(sede_id):
                    messagebox.showinfo("Éxito", "Sede eliminada.")
                    self.cargar_sedes()
        else:
            lab_sel = self.lab_combobox.get()
            if not lab_sel:
                return

            sede_id = self.sede_ids[self.sede_names.index(self.sede_combobox.get())]
            laboratorios = self.db_manager.obtener_laboratorios_por_sede(sede_id)
            if len(laboratorios) <= 1:
                messagebox.showwarning(
                    "No se puede eliminar",
                    "No se puede eliminar el laboratorio porque es el único que existe en la sede."
                )
                return

            lab_id = self.lab_ids[self.lab_names.index(lab_sel)]
            if messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar el laboratorio '{lab_sel}'?"):
                if self.db_manager.eliminar_laboratorio(lab_id):
                    messagebox.showinfo("Éxito", "Laboratorio eliminado.")
                    self.on_sede_change()