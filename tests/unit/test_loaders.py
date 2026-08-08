from pathlib import Path

from reportlab.pdfgen import canvas

from f1_regulations_rag.ingestion.loaders import extract_text


def _make_pdf(tmp_path: Path, text: str) -> Path:
    """Create a tiny PDF containing the given text."""
    path = tmp_path / "sample.pdf"
    c = canvas.Canvas(str(path))
    c.drawString(72, 720, text)
    c.save()
    return path


def test_extract_text_returns_document_text(tmp_path: Path) -> None:
    pdf = _make_pdf(tmp_path, "Article 33.4 overtaking rules")
    extracted = extract_text(pdf)
    assert "Article 33.4" in extracted
