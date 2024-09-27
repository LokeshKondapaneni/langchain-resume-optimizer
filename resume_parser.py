import pdfplumber

def parse_resume(file):
    with pdfplumber.open(file) as pdf_file:
        return "\n".join(page.extract_text() for page in pdf_file.pages)