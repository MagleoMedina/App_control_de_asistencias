import customtkinter as ctk

# Función para cargar la vista de "Carga de Asistencia"
def mostrar_carga_asistencia():
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Scrollbar
    canvas = ctk.CTkCanvas(main_frame)
    scrollbar = ctk.CTkScrollbar(main_frame, command=canvas.yview)
    scrollable_frame = ctk.CTkFrame(canvas, fg_color="white")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Carga de Asistencia
    asistencia_label = ctk.CTkLabel(scrollable_frame, text="Carga de Asistencia", font=("Arial", 16, "bold"))
    asistencia_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Tabloide 1
    tabloide1_frame = ctk.CTkFrame(scrollable_frame, fg_color="lightblue", border_width=2)
    tabloide1_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    nombre_usuario_label = ctk.CTkLabel(tabloide1_frame, text="Nombre de usuario:")
    nombre_usuario_label.grid(row=0, column=0, sticky="e", pady=5)
    nombre_usuario_entry = ctk.CTkEntry(tabloide1_frame, placeholder_text="Ingrese nombre de usuario")
    nombre_usuario_entry.grid(row=0, column=1, sticky="w", pady=5, padx=10)

    nombre_lab_label = ctk.CTkLabel(tabloide1_frame, text="Nombre de laboratorio:")
    nombre_lab_label.grid(row=1, column=0, sticky="e", pady=5)
    nombre_lab_entry = ctk.CTkEntry(tabloide1_frame, placeholder_text="Ingrese nombre del laboratorio")
    nombre_lab_entry.grid(row=1, column=1, sticky="w", pady=5, padx=10)

    fecha_label = ctk.CTkLabel(tabloide1_frame, text="Fecha:")
    fecha_label.grid(row=2, column=0, sticky="e", pady=5)
    fecha_entry = ctk.CTkEntry(tabloide1_frame, placeholder_text="DD/MM/AAAA")
    fecha_entry.grid(row=2, column=1, sticky="w", pady=5, padx=10)

    hora_inicio_label = ctk.CTkLabel(tabloide1_frame, text="Hora de inicio:")
    hora_inicio_label.grid(row=3, column=0, sticky="e", pady=5)
    hora_inicio_entry = ctk.CTkEntry(tabloide1_frame, placeholder_text="HH:MM")
    hora_inicio_entry.grid(row=3, column=1, sticky="w", pady=5, padx=10)

    hora_fin_label = ctk.CTkLabel(tabloide1_frame, text="Hora de finalización:")
    hora_fin_label.grid(row=4, column=0, sticky="e", pady=5)
    hora_fin_entry = ctk.CTkEntry(tabloide1_frame, placeholder_text="HH:MM")
    hora_fin_entry.grid(row=4, column=1, sticky="w", pady=5, padx=10)

    # Tabloide 2
    datos_persona_label = ctk.CTkLabel(scrollable_frame, text="Datos de persona", font=("Arial", 16, "bold"))
    datos_persona_label.grid(row=2, column=0, columnspan=2, pady=10)

    tabloide2_frame = ctk.CTkFrame(scrollable_frame, fg_color="lightblue", border_width=2)
    tabloide2_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    tipo_usuario_label = ctk.CTkLabel(tabloide2_frame, text="Tipo de usuario:")
    tipo_usuario_label.grid(row=0, column=0, sticky="e", pady=5)
    tipo_usuario_entry = ctk.CTkEntry(tabloide2_frame, placeholder_text="Estudiante, Profesor, etc.")
    tipo_usuario_entry.grid(row=0, column=1, sticky="w", pady=5, padx=10)

    nombre_label = ctk.CTkLabel(tabloide2_frame, text="Nombre:")
    nombre_label.grid(row=1, column=0, sticky="e", pady=5)
    nombre_entry = ctk.CTkEntry(tabloide2_frame, placeholder_text="Nombre")
    nombre_entry.grid(row=1, column=1, sticky="w", pady=5, padx=10)

    apellido_label = ctk.CTkLabel(tabloide2_frame, text="Apellido:")
    apellido_label.grid(row=2, column=0, sticky="e", pady=5)
    apellido_entry = ctk.CTkEntry(tabloide2_frame, placeholder_text="Apellido")
    apellido_entry.grid(row=2, column=1, sticky="w", pady=5, padx=10)

    cedula_label = ctk.CTkLabel(tabloide2_frame, text="Cédula:")
    cedula_label.grid(row=3, column=0, sticky="e", pady=5)
    cedula_entry = ctk.CTkEntry(tabloide2_frame, placeholder_text="Cédula")
    cedula_entry.grid(row=3, column=1, sticky="w", pady=5, padx=10)

    telefono_label = ctk.CTkLabel(tabloide2_frame, text="Teléfono:")
    telefono_label.grid(row=4, column=0, sticky="e", pady=5)
    telefono_entry = ctk.CTkEntry(tabloide2_frame, placeholder_text="Teléfono")
    telefono_entry.grid(row=4, column=1, sticky="w", pady=5, padx=10)

    num_bien_label = ctk.CTkLabel(tabloide2_frame, text="Número de bien:")
    num_bien_label.grid(row=5, column=0, sticky="e", pady=5)
    num_bien_entry = ctk.CTkEntry(tabloide2_frame, placeholder_text="Número de bien")
    num_bien_entry.grid(row=5, column=1, sticky="w", pady=5, padx=10)

    añadir_persona_button = ctk.CTkButton(tabloide2_frame, text="Añadir persona", fg_color="green")
    añadir_persona_button.grid(row=6, column=0, columnspan=2, pady=20)

    # Tabla de resultados
    tabla_frame = ctk.CTkFrame(scrollable_frame, fg_color="lightblue", border_width=2)
    tabla_frame.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    tabla_label = ctk.CTkLabel(tabla_frame, text="No. | Tipo de usuario | Nombre | Apellido | Cédula | Teléfono | Número de bien")
    tabla_label.pack(pady=5)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

# Configuración de la ventana principal
root = ctk.CTk()
root.title("SASE - Control de Asistencias")
root.geometry("1200x700")

# Configuración del grid
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure((0, 1, 2, 3), weight=1)

# Panel de Navegación
nav_frame = ctk.CTkFrame(root, width=200)
nav_frame.grid(row=0, column=0, rowspan=4, sticky="nsw", padx=10, pady=10)

nav_label = ctk.CTkLabel(nav_frame, text="SASE", font=("Arial", 20, "bold"))
nav_label.pack(pady=10)

# Botones del Panel de Navegación
botones_nav = [
    ("Carga de Asistencia", "📝", mostrar_carga_asistencia),
    ("Carga de Asistencia Estudiantes", "👨‍🎓", None),
    ("Consultar Asistencia", "🔍", None),
    ("Consultar Falla de Computador", "💻", None),
    ("Módulo Estadístico", "📊", None),
    ("Cerrar Sesión", "🚪", None)
]

for texto, icono, command in botones_nav:
    boton = ctk.CTkButton(nav_frame, text=f"{icono} {texto}", width=180, command=command)
    boton.pack(pady=5)

# Frame principal donde se cargarán las vistas
main_frame = ctk.CTkFrame(root)
main_frame.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=10, pady=10)

# Mensaje de bienvenida
bienvenida_label = ctk.CTkLabel(main_frame, text="Bienvenido Magleo", font=("Arial", 18, "bold"))
bienvenida_label.pack(pady=10)

root.mainloop()
