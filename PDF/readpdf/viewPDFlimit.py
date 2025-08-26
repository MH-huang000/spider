import fitz  # PyMuPDF

def check_pdf_permissions(pdf_path, password=None):
    # Open the PDF file
    document = fitz.open(pdf_path)
    
    # Check if the document is encrypted
    if document.is_encrypted:
        if password:
            if not document.authenticate(password):
                print("Password authentication failed")
                return
        else:
            print("Document is encrypted but no password provided")
            return

    # Check the permissions
    permissions = document.permissions
    print(f"Permissions: {permissions}")
    
    # Check if text extraction is allowed
    if permissions & fitz.PDF_PERM_COPY:
        print("Text extraction is allowed")
    else:
        print("Text extraction is not allowed")

# Example usage
pdf_path = r"C:\\Users\\MH\\Downloads\\0-4.pdf"
password = 'multinet'
check_pdf_permissions(pdf_path, password)
