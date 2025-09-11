from xhtml2pdf import pisa
import os

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
                with open(css_path, "r") as css_file:
                    css_content = f"<style>{css_file.read()}</style>"
                    html_content = css_content + html_content

            # Generate PDF
            with open(self.output_path, "wb") as pdf_file:
                pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
            return not pisa_status.err
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return False

