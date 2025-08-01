import customtkinter as ctk
from db_manager import DBManager

class SedeLaboratorioApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Sedes y Laboratorios")
        self.geometry("500x400")
        self.db = DBManager()

        # Frame para añadir sede
        sede_frame = ctk.CTkFrame(self)
        sede_frame.pack(pady=20, padx=20, fill="x")

        ctk.CTkLabel(sede_frame, text="Añadir Sede", font=("Arial", 16)).pack(pady=(0,10))
        self.sede_nombre_entry = ctk.CTkEntry(sede_frame, placeholder_text="Nombre de la sede")
        self.sede_nombre_entry.pack(pady=5, fill="x")
        ctk.CTkButton(sede_frame, text="Agregar Sede", command=self.agregar_sede).pack(pady=5)

        self.sede_status_label = ctk.CTkLabel(sede_frame, text="")
        self.sede_status_label.pack()

        # Separador
        ctk.CTkLabel(self, text="").pack(pady=5)

        # Frame para añadir laboratorio
        lab_frame = ctk.CTkFrame(self)
        lab_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(lab_frame, text="Añadir Laboratorio", font=("Arial", 16)).pack(pady=(0,10))
        self.lab_nombre_entry = ctk.CTkEntry(lab_frame, placeholder_text="Nombre del laboratorio")
        self.lab_nombre_entry.pack(pady=5, fill="x")

        # Lista desplegable de sedes (solo lectura)
        self.sedes = []
        self.sede_ids = []
        self.sede_combobox = ctk.CTkComboBox(lab_frame, values=[], state="readonly")
        self.sede_combobox.pack(pady=5, fill="x")
        ctk.CTkButton(lab_frame, text="Agregar Laboratorio", command=self.agregar_laboratorio).pack(pady=5)

        self.lab_status_label = ctk.CTkLabel(lab_frame, text="")
        self.lab_status_label.pack()

        self.actualizar_lista_sedes()

    def agregar_sede(self):
        nombre = self.sede_nombre_entry.get().strip()
        if not nombre:
            self.sede_status_label.configure(text="Ingrese un nombre de sede.", text_color="red")
            return
        if self.db.agregar_sede(nombre):
            self.sede_status_label.configure(text="Sede agregada correctamente.", text_color="green")
            self.sede_nombre_entry.delete(0, "end")
            self.actualizar_lista_sedes()
        else:
            self.sede_status_label.configure(text="Error al agregar sede.", text_color="red")

    def actualizar_lista_sedes(self):
        sedes = self.db.obtener_sedes()
        self.sedes = [s[1] for s in sedes]
        self.sede_ids = [s[0] for s in sedes]
        self.sede_combobox.configure(values=self.sedes)
        if self.sedes:
            self.sede_combobox.set(self.sedes[0])
        else:
            self.sede_combobox.set("")

    def agregar_laboratorio(self):
        nombre = self.lab_nombre_entry.get().strip()
        sede_idx = self.sede_combobox.current_index if hasattr(self.sede_combobox, "current_index") else self.sede_combobox.cget("values").index(self.sede_combobox.get()) if self.sede_combobox.get() in self.sede_combobox.cget("values") else -1
        if not nombre:
            self.lab_status_label.configure(text="Ingrese un nombre de laboratorio.", text_color="red")
            return
        if sede_idx < 0 or sede_idx >= len(self.sede_ids):
            self.lab_status_label.configure(text="Seleccione una sede.", text_color="red")
            return
        sede_id = self.sede_ids[sede_idx]
        if self.db.agregar_laboratorio(nombre, sede_id):
            self.lab_status_label.configure(text="Laboratorio agregado correctamente.", text_color="green")
            self.lab_nombre_entry.delete(0, "end")
        else:
            self.lab_status_label.configure(text="Error al agregar laboratorio.", text_color="red")

if __name__ == "__main__":
    app = SedeLaboratorioApp()
    app.mainloop()
