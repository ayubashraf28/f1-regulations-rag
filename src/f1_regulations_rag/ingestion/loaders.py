"""PDF loading utilities.

Reads FIA regulation PDFs into plain text, one page at a time.
"""

from pathlib import Path

import pdfplumber


def extract_text(pdf_path: Path | str) -> str:
    """Extract all text from a PDF file, joined page by page.

    Returns an empty string for a PDF with no extractable text
    (e.g. scanned images) rather than crashing.
    """
    pages: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            pages.append(text)
    return "\n".join(pages)
