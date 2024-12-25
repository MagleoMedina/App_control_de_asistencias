import customtkinter as ctk
from tkinter import filedialog, ttk
from PyPDF2 import PdfReader
import re
from tkcalendar import DateEntry


class AnalizadorPDF(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.counter = 1  # Initialize counter
        self.entry_usuario.insert(0, "Magleo")  # Set default value
        self.entry_usuario.configure(state="readonly")  # Make read-only
       # print("Magleo")  # Print the string

    def setup_ui(self):
        btn_seleccionar = ctk.CTkButton(self, text="Seleccionar archivo PDF", command=self.seleccionar_archivo)
        btn_seleccionar.grid(row=0, column=5, columnspan=2, pady=20)
        # Initialize labels and entry fields but don't grid them yet
        self.label_sede = ctk.CTkLabel(self, text="Sede")
        self.entry_sede = ctk.CTkEntry(self, state="readonly")
        self.label_carrera = ctk.CTkLabel(self, text="Carrera")
        self.entry_carrera = ctk.CTkEntry(self, state="readonly")
        self.label_curso = ctk.CTkLabel(self, text="Curso")
        self.entry_curso = ctk.CTkEntry(self, state="readonly")
        self.label_docente = ctk.CTkLabel(self, text="Docente")
        self.entry_docente = ctk.CTkEntry(self, state="readonly")

        # New labels and entries
        self.label_usuario = ctk.CTkLabel(self, text="Nombre de usuario")
        self.entry_usuario = ctk.CTkEntry(self, state="readonly")
        
        self.label_laboratorio = ctk.CTkLabel(self, text="Nombre de laboratorio")
        self.entry_laboratorio = ctk.CTkEntry(self)
        self.label_fecha = ctk.CTkLabel(self, text="Fecha")
        self.entry_fecha = DateEntry(self)
        self.label_hora_inicio = ctk.CTkLabel(self, text="Hora de inicio")
        self.entry_hora_inicio_horas = ctk.CTkEntry(self, width=2)
        self.entry_hora_inicio_minutos = ctk.CTkEntry(self, width=2)
        self.label_hora_fin = ctk.CTkLabel(self, text="Hora de finalizacion")
        self.entry_hora_fin_horas = ctk.CTkEntry(self, width=2)
        self.entry_hora_fin_minutos = ctk.CTkEntry(self, width=2)

        # Initially hide new labels and entries
        self.label_usuario.grid_remove()
        self.entry_usuario.grid_remove()
        self.label_laboratorio.grid_remove()
        self.entry_laboratorio.grid_remove()
        self.label_fecha.grid_remove()
        self.entry_fecha.grid_remove()
        self.label_hora_inicio.grid_remove()
        self.entry_hora_inicio_horas.grid_remove()
        self.entry_hora_inicio_minutos.grid_remove()
        self.label_hora_fin.grid_remove()
        self.entry_hora_fin_horas.grid_remove()
        self.entry_hora_fin_minutos.grid_remove()

        # Initialize table for "DOS_PALABRAS_COMA_DOS_PALABRAS" pattern matches using CustomTkinter
        self.table_frame = ctk.CTkFrame(self)
        self.table = ttk.Treeview(self.table_frame, columns=("No", "Apellidos", "Nombres", "Numero de Bien", "¿Asistencia?"), show="headings")
        self.table.heading("No", text="No")
        self.table.heading("Apellidos", text="Apellidos")
        self.table.heading("Nombres", text="Nombres")
        self.table.heading("Numero de Bien", text="Numero de Bien")
        self.table.heading("¿Asistencia?", text="¿Asistencia?")
        self.table.column("No", width=50)
        self.table.column("Numero de Bien", width=150)
        self.table.column("¿Asistencia?", width=100)
        self.table.pack(fill="both", expand=True)
        self.table_frame.grid(row=3, column=0, columnspan=8, padx=10, pady=10)
        self.table_frame.grid_remove()  # Initially hide the table frame
        
        self.table.bind("<Double-1>", self.on_double_click)

        # Label and radio buttons for "Fallo alguna computadora?"
        self.label_fallo_computadora = ctk.CTkLabel(self, text="Fallo alguna computadora?")
        self.radio_var = ctk.StringVar(value="No")
        self.radio_si = ctk.CTkRadioButton(self, text="Si", variable=self.radio_var, value="Si")
        self.radio_no = ctk.CTkRadioButton(self, text="No", variable=self.radio_var, value="No")

        # Initially hide the label and radio buttons
        self.label_fallo_computadora.grid_remove()
        self.radio_si.grid_remove()
        self.radio_no.grid_remove()

        # Additional labels and entries for "Fallo alguna computadora?"
        self.label_numero_bien = ctk.CTkLabel(self, text="Numero de Bien")
        self.entry_numero_bien = ctk.CTkEntry(self)
        self.label_descripcion = ctk.CTkLabel(self, text="Descripcion")
        self.entry_descripcion = ctk.CTkEntry(self)

        # Initially hide the additional labels and entries
        self.label_numero_bien.grid_remove()
        self.entry_numero_bien.grid_remove()
        self.label_descripcion.grid_remove()
        self.entry_descripcion.grid_remove()

        # Bind radio button selection to a method
        self.radio_si.configure(command=self.toggle_fallo_computadora)
        self.radio_no.configure(command=self.toggle_fallo_computadora)

    def toggle_fallo_computadora(self):
        if self.radio_var.get() == "Si":
            self.label_numero_bien.grid(row=5, column=0, padx=5, pady=5)
            self.entry_numero_bien.grid(row=5, column=1, padx=5, pady=5)
            self.label_descripcion.grid(row=5, column=2, padx=5, pady=5)
            self.entry_descripcion.grid(row=5, column=3, padx=5, pady=5)
        else:
            self.label_numero_bien.grid_remove()
            self.entry_numero_bien.grid_remove()
            self.label_descripcion.grid_remove()
            self.entry_descripcion.grid_remove()

    def on_double_click(self, event):
        item = self.table.selection()[0]
        column = self.table.identify_column(event.x)
        column_index = int(column.replace('#', '')) - 1
        if column_index == 0:  # Make "No" column read-only
            return
        if column_index == 4:  # Toggle boolean value for "¿Asistencia?" column
            values = list(self.table.item(item, "values"))
            current_value = values[column_index]
            new_value = "SI" if current_value == "NO" else "NO"
            values[column_index] = new_value
            self.table.item(item, values=values)
            return
        x, y, width, height = self.table.bbox(item, column)
        value = self.table.item(item, "values")[column_index]

        self.entry_edit = ctk.CTkEntry(self.table, width=width, height=height)
        self.entry_edit.place(x=x, y=y)
        self.entry_edit.insert(0, value)
        self.entry_edit.focus()

        self.entry_edit.bind("<Return>", lambda e: self.save_edit(item, column_index))
        self.entry_edit.bind("<FocusOut>", lambda e: self.entry_edit.destroy())

    def save_edit(self, item, column_index):
        new_value = self.entry_edit.get()
        values = list(self.table.item(item, "values"))
        values[column_index] = new_value
        self.table.item(item, values=values)
        self.entry_edit.destroy()

    def analizar_pdf(self, ruta_pdf):
        try:
            with open(ruta_pdf, 'rb') as archivo:
                lector_pdf = PdfReader(archivo)
                num_paginas = len(lector_pdf.pages)
                texto_paginas = []

                for pagina in range(num_paginas):
                    pagina_obj = lector_pdf.pages[pagina]
                    texto_paginas.append(pagina_obj.extract_text())

                return {
                    'num_paginas': num_paginas,
                    'texto_paginas': texto_paginas
                }
        except Exception as e:
            print(f"Error al analizar el PDF: {e}")
            return None

    def filtrar_texto(self, texto, filtros):
        for filtro in filtros:
            texto = re.sub(filtro, "", texto, flags=re.IGNORECASE)
        return texto

    def reconocer_patrones(self, texto, patrones):
        resultados = {}
        for nombre, patron in patrones.items():
            coincidencias = re.findall(patron, texto, flags=re.IGNORECASE)
            if coincidencias:
                resultados[nombre] = coincidencias
        return resultados

    def seleccionar_archivo(self):
        ruta_pdf = filedialog.askopenfilename(
            title="Seleccionar archivo PDF",
            filetypes=(("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*"))
        )
        if ruta_pdf:
            resultados = self.analizar_pdf(ruta_pdf)
            if resultados:
                # Show the labels and entries
                self.label_usuario.grid(row=2, column=0, padx=5, pady=5)
                self.entry_usuario.grid(row=2, column=1, padx=5, pady=5)
                self.label_laboratorio.grid(row=2, column=2, padx=5, pady=5)
                self.entry_laboratorio.grid(row=2, column=3, padx=5, pady=5)
                self.label_fecha.grid(row=2, column=4, padx=5, pady=5)
                self.entry_fecha.grid(row=2, column=5, padx=5, pady=5)
                self.label_hora_inicio.grid(row=2, column=6, padx=5, pady=5)
                self.entry_hora_inicio_horas.grid(row=2, column=7, padx=5, pady=5)
                self.entry_hora_inicio_minutos.grid(row=2, column=8, padx=5, pady=5)
                self.label_hora_fin.grid(row=2, column=9, padx=5, pady=5)
                self.entry_hora_fin_horas.grid(row=2, column=10, padx=5, pady=5)
                self.entry_hora_fin_minutos.grid(row=2, column=11, padx=5, pady=5)

                # Show the label and radio buttons
                self.label_fallo_computadora.grid(row=4, column=0, padx=5, pady=5)
                self.radio_si.grid(row=4, column=1, padx=5, pady=5)
                self.radio_no.grid(row=4, column=2, padx=5, pady=5)

                filtros = [
                    "UNIVERSIDAD NACIONAL EXPERIMENTAL DE GUAYANA",
                    "SECRETARÍA",
                    "COORDINACIÓN DE ADMISIÓN Y CONTROL DE ESTUDIOS",
                ]
                patrones = {
                    "SEDE": r"SEDE:\s*(\w+\s*\w*)",
                    "CARRERA": r"CARRERA:\s*([\w\s]+?)\s*SEMESTRE",
                    "CURSO": r"\b\d{7}\s+([\w\s]+)(?<!\bSECCIÓN\b)(?<!\b\d{7})\b",
                    "SECCION": r"SECCIÓN:\s*(\d+)",
                    "DOCENTE": r"DOCENTE:\s*[A-Za-z]\d{0,8}\s((?:\w+\s){0,3}\w+)",
                    "DOS_PALABRAS_COMA_DOS_PALABRAS": r"(\w+\s\w+),\s(\w+\s\w+)"
                    
                }
                for i, texto in enumerate(resultados['texto_paginas']):
                    texto_filtrado = self.filtrar_texto(texto, filtros)
                    patrones_encontrados = self.reconocer_patrones(texto_filtrado, patrones)
                    for nombre, coincidencias in patrones_encontrados.items():
                        # Display the labels and entry fields with the first found pattern only
                        if nombre == "SEDE" and not self.entry_sede.get():
                            self.label_sede.grid(row=1, column=0, padx=5, pady=5)
                            self.entry_sede.grid(row=1, column=1, padx=5, pady=5)
                            self.entry_sede.configure(state="normal")
                            self.entry_sede.insert(0, coincidencias[0])
                            self.entry_sede.configure(state="readonly")
                        elif nombre == "CARRERA" and not self.entry_carrera.get():
                            self.label_carrera.grid(row=1, column=2, padx=5, pady=5)
                            self.entry_carrera.grid(row=1, column=3, padx=5, pady=5)
                            self.entry_carrera.configure(state="normal")
                            self.entry_carrera.insert(0, coincidencias[0])
                            self.entry_carrera.configure(state="readonly")
                        elif nombre == "CURSO" and not self.entry_curso.get():
                            self.label_curso.grid(row=1, column=4, padx=5, pady=5)
                            self.entry_curso.grid(row=1, column=5, padx=5, pady=5)
                            self.entry_curso.configure(state="normal")
                            self.entry_curso.insert(0, coincidencias[0])
                            self.entry_curso.configure(state="readonly")
                        elif nombre == "DOCENTE" and not self.entry_docente.get():
                            self.label_docente.grid(row=1, column=6, padx=5, pady=5)
                            self.entry_docente.grid(row=1, column=7, padx=5, pady=5, columnspan=3)
                            self.entry_docente.configure(state="normal")
                            self.entry_docente.insert(0, coincidencias[0])
                            self.entry_docente.configure(state="readonly")
                        elif nombre == "DOS_PALABRAS_COMA_DOS_PALABRAS":
                            self.table_frame.grid()  # Show the table frame
                            for coincidencia in coincidencias:
                                self.table.insert("", "end", values=(self.counter, coincidencia[0], coincidencia[1], "", "NO"))  # Add empty "Numero de Bien" and "¿Asistencia?" columns
                                self.counter += 1


