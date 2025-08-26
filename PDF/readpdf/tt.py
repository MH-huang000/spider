import fitz  # PyMuPDF

def detect_start_page(pdf_path, password):
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
    
    # Detect start page
    start_page = None
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        page_text = page.get_text("text")
        if page_text.strip():  # Check if the page has non-whitespace text
            start_page = page_num
            break

    if start_page is not None:
        print(f"Detected start page: {start_page + 1}")
    else:
        print("No text found in the document")
    
    return start_page

def extract_text_from_pdf(pdf_path, password, start_page=0):
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
    
    # Extract text from each page starting from start_page
    text = ""
    for page_num in range(start_page, len(document)):
        page = document.load_page(page_num)
        
        # Try different text extraction methods
        page_text = page.get_text("text")  # Standard text extraction
        if not page_text.strip():
            page_text = page.get_text("blocks")  # Extract text blocks
        if not page_text.strip():
            page_text = page.get_text("words")  # Extract individual words
        if not page_text.strip():
            page_text = "No text found on this page"
        
        print(f"Page {page_num + 1} text:\n{page_text}\n")
        text += page_text + "\n"
    
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
pdf_path = r"C:\\Users\\MH\\Downloads\\0-4.pdf"
password = 'multinet'

start_page = detect_start_page(pdf_path, password)
if start_page is not None:
    text = extract_text_from_pdf(pdf_path, password, start_page)
    if text:
        print("Extracted text:")
        print(text)
        write_text_to_docx(text, 'output.docx')
