import fitz  # PyMuPDF
from docx import Document

def extract_text_from_pdf(pdf_path, password, start_page):
    # Open the PDF file
    document = fitz.open(pdf_path)
    
    # Check if the document is encrypted
    if document.is_encrypted:
        # Try to authenticate with the password
        if document.authenticate(password):
            print("Password authentication successful")
        else:
            print("Password authentication failed")
            return None
    else:
        print("Document is not encrypted")
    
    # Extract text from each page
    text = ""
    for page_num in range(start_page, len(document)):
        page = document.load_page(page_num)
        text += page.get_text("blocks")
    
    return text

def write_text_to_docx(text, docx_path):
    # Create a new Document
    doc = Document()
    
    # Add text to the Document
    doc.add_paragraph(text)
    
    # Save the Document
    doc.save(docx_path)
    print(f"Text successfully written to {docx_path}")

# Example usage
pdf_path = r"C:\\Users\\MH\\Downloads\\國立中興大學114學年度碩士班招生考試成績通知單.pdf"
password = 'multinet'
docx_path = 'output.docx'
start_page = 4 

text = extract_text_from_pdf(pdf_path, password, start_page)
if text:
    print(text)
    # write_text_to_docx(text, docx_path)
