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
App_control_de_asistencias/
│
├── Views/
│   ├── ventana_main.py               # Ventana principal de la aplicación
│   ├── ventana_login.py              # Ventana de inicio de sesión
│   ├── gestion_de_usuarios.py        # Gestión de usuarios
│   ├── modulo_estadistico.py         # Módulo para generar reportes estadísticos
│   ├── equipos.py                    # Gestión de equipos
│   ├── consultar_asistencia.py       # Consulta de asistencia
│   ├── carga_asistencia.py           # Carga de asistencia
│   ├── carga_asistencia_estudiantes.py # Carga de asistencia para estudiantes
│
├── Pdf/
│   ├── modulo_estadistico.html       # Plantilla HTML para reportes estadísticos
│   ├── consultar_falla_equipo.html   # Plantilla HTML para consulta de fallas de equipos
│   ├── consultar_asistencia.html     # Plantilla HTML para consulta de asistencia
│   ├── estilos.css                   # Estilos CSS para los reportes
│
├── main.py                           # Archivo principal para iniciar la aplicación
├── requirements.txt                  # Archivo con las dependencias del proyecto
├── README.md                         # Documentación principal del proyecto
└── LICENSE                           # Licencia del proyecto
```
