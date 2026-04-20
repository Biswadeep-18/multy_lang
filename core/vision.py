import pypdf
from PIL import Image
import io
import base64
from core.llms import get_llm
from langchain_core.messages import HumanMessage

def extract_text_from_pdf(file_bytes):
    pdf_reader = pypdf.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_image(file_bytes):
    # Use Gemini for OCR (Optical Character Recognition)
    # We use 'ultra' (Gemini 3 Flash) because it has the best vision capabilities
    llm = get_llm("ultra")
    
    # Convert image to base64
    image_base64 = base64.b64encode(file_bytes).decode("utf-8")
    
    prompt = "Please extract all text from this image accurately. return ONLY the extracted text."
    
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
            },
        ]
    )
    
    response = llm.invoke([message])
    return response.content.strip()

def process_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return None
    
    file_bytes = uploaded_file.read()
    file_type = uploaded_file.type
    
    try:
        if "pdf" in file_type:
            return extract_text_from_pdf(file_bytes)
        elif "image" in file_type:
            return extract_text_from_image(file_bytes)
        else:
            # Try plain text
            return file_bytes.decode("utf-8")
    except Exception as e:
        return f"Error extracting text: {str(e)}"
