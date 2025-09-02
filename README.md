# App_control_de_asistencias

# Proyecto de Gestión de Asistencia

Este proyecto es una aplicación de escritorio para la gestión de asistencia utilizando la biblioteca `customtkinter` y otras dependencias.

## Requisitos

Asegúrate de tener instalado Python 3.6 o superior. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).

## Instalación de dependencias

Para instalar las dependencias necesarias, puedes utilizar `pip`. A continuación se muestra una lista de las bibliotecas requeridas:

- customtkinter
- tkcalendar
- PyPDF2
- tkinter

Puedes instalar todas las dependencias ejecutando el siguiente comando:

```sh

pip install -r requirements.txt
```

## Estructura del proyecto

La estructura del proyecto es la siguiente:

```
├── 📁 Pdf/
│   ├── 🌐 consultar_asistencia.html
│   ├── 🌐 consultar_falla_equipo.html
│   ├── 🎨 estilos.css
│   ├── 🖼️ logo_uneg.png
│   ├── 🌐 modulo_estadistico.html
│   └── 🐍 pdf.py
├── 📁 Views/
│   ├── 📁 Imagen/
│   │   ├── 🖼️ CL.png
│   │   └── 🖼️ logoUNEG.png
│   ├── 🐍 carga_asistencia.py
│   ├── 🐍 carga_asistencia_estudiantes.py
│   ├── 🐍 consultar_asistencia.py
│   ├── 🐍 equipos.py
│   ├── 🐍 gestion_de_usuarios.py
│   ├── 🐍 modulo_estadistico.py
│   ├── 🐍 ventana_login.py
│   └── 🐍 ventana_main.py
├── 🔒 .env 🚫 (auto-hidden)
├── 🚫 .gitignore
├── 🖼️ MER servicio.png
├── 📖 README.md
├── 🐍 db_manager.py
├── 🐍 main.py
├── 📄 requirements.txt
├── 🗄️ salu-db.db
├── 📄 salu-db.db-info
├── 📄 salu-db.db-shm
├── 📄 salu-db.db-wal
└── 🐍 sede.py
```


