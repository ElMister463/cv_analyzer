import PyPDF2
from io import BytesIO

def text_extract_pdf( pdf_file ):
    try:
        pdf_reader = PyPDF2.PdfReader( BytesIO( pdf_file.read() ) )
        complete_text = ""

        for page_number, page in enumerate( pdf_reader.pages, 1 ):
            page_text = page.extract_text()

            if page_text.strip():
                complete_text += f"\n--- PÁGINA {page_number} ---\n"
                complete_text += page_text + "\n"


        complete_text = complete_text.strip()

        if not complete_text:
            return "Error: El Archivo PDF parece estar vacío o contener sólo imágenes"
        
        return complete_text
    
    except Exception as e:
        return f"Error al procesar el archivo PDF: {str( e )}"