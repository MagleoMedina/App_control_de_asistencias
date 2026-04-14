from xhtml2pdf import pisa
import os
import sys

def link_callback(uri, rel):
    """
    Convierte rutas relativas de HTML en rutas absolutas del sistema.
    Permite que xhtml2pdf encuentre imágenes y recursos en el .exe (PyInstaller).
    """
    # 1. Determinar la base del proyecto
    if hasattr(sys, '_MEIPASS'):
        # Ruta cuando se ejecuta desde el .exe empaquetado
        base_dir = sys._MEIPASS
    else:
        # Ruta en modo desarrollo (subimos un nivel desde la carpeta 'Pdf' a la raíz)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # 2. Limpiar la URI (quitamos los ../ que se usan en HTML para subir carpetas)
    # Ejemplo: "../assets/logo.png" -> "assets/logo.png"
    relative_path = uri.replace("../", "").replace("/", os.sep)
    
    # 3. Crear la ruta absoluta final uniendo la base con la ruta relativa del archivo
    path = os.path.join(base_dir, relative_path)

    # 4. Validar que el archivo exista para evitar errores de tipo None
    if not os.path.isfile(path):
        print(f"Advertencia: No se encontró el recurso en {path}")
    
    return path

class PDFGenerator:
    def __init__(self, output_path):
        # Asegura que la carpeta 'Reportes' exista
        reportes_dir = os.path.join(os.path.dirname(output_path), 'Reportes')
        os.makedirs(reportes_dir, exist_ok=True)
        # Guarda el PDF en la carpeta 'Reportes'
        self.output_path = os.path.join(reportes_dir, os.path.basename(output_path))

    def generate_pdf(self, html_content, css_path=None):
        """
        Generates a PDF file from the provided HTML content and optional CSS file.

        :param html_content: The HTML content as a string.
        :param css_path: Path to the CSS file (optional).
        :return: True if the PDF was generated successfully, False otherwise.
        """
        try:
            # Apply CSS if provided
            if css_path:
                if os.path.exists(css_path):
                    with open(css_path, "r", encoding="utf-8") as css_file:
                        css_content = f"<style>{css_file.read()}</style>"
                        html_content = css_content + html_content
                else:
                    print(f"Advertencia: No se encontró el archivo CSS en {css_path}")

            # Generate PDF
            with open(self.output_path, "wb") as pdf_file:
                pisa_status = pisa.CreatePDF(html_content, dest=pdf_file, link_callback=link_callback)
            return not pisa_status.err
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return False

