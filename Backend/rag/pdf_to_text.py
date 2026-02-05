import os
from pypdf import PdfReader


def pdf_to_text(pdf_path: str) -> str:
    # Check if file exists and is not empty
    if not os.path.exists(pdf_path) or os.path.getsize(pdf_path) == 0:
        return "Error: The PDF file is missing or empty."
        
    reader = PdfReader(pdf_path)
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")

    text = "\n".join(pages)
    text = text.replace("\r", "\n")
    text = "\n".join([line.strip() for line in text.split("\n") if line.strip()])
    return text