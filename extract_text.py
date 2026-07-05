"""
Step 1: Get text from a PDF file.

This file does ONE job only — read a PDF and return plain text.
"""

import pdfplumber


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Open a PDF and combine text from every page.

    Args:
        pdf_path: Full path to the PDF file on your computer.

    Returns:
        All text found in the PDF as one big string.
    """
    all_text = []

    # pdfplumber opens the file like a book and reads each page
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            # Some scanned PDFs have no text — skip empty pages
            if page_text:
                all_text.append(page_text)

    # Join pages with a blank line between them
    return "\n\n".join(all_text).strip()


def extract_text_from_txt(txt_path: str) -> str:
    """Read a plain .txt file (useful for testing without a PDF)."""
    with open(txt_path, "r", encoding="utf-8") as file:
        return file.read().strip()