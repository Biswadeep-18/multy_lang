from fpdf import FPDF
import io

def generate_pdf(text, title="Exported Document"):
    pdf = FPDF()
    pdf.add_page()
    
    # We attempt to use a standard font. 
    # Note: For non-Latin characters (Odia, Hindi), fpdf requires a Unicode font (.ttf) to be added.
    # Without a TTF file, we fallback to a safe rendering or the user should use TXT.
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.ln(10)
    
    # Body
    pdf.set_font("Arial", size=12)
    # multi_cell handles line breaks
    pdf.multi_cell(0, 10, txt=text)
    
    return pdf.output()

def generate_txt(text):
    return text.encode("utf-8")
