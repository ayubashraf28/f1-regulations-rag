"""Download FIA F1 regulation PDFs into data/raw/.

Run:  uv run python scripts/download_documents.py
Safe to re-run: files that already exist are skipped (no re-downloading).
"""

from pathlib import Path

import requests

# (label, url) pairs for the current 2026 F1 Regulations.
# Retrieved from https://www.fia.com/regulation/category/110 on 2026-08-08.
DOCUMENTS = [
    (
        "2026_section_a_general_provisions",
        "https://www.fia.com/system/files/documents/fia_2026_f1_regulations_-_section_a_general_provisions_-_iss_03_-_2026-06-25.pdf",
    ),  # noqa: E501
    (
        "2026_section_b_sporting",
        "https://www.fia.com/system/files/documents/fia_2026_f1_regulations_-_section_b_sporting_-_iss_08_-_2026-08-05_7.pdf",
    ),  # noqa: E501
    (
        "2026_section_c_technical",
        "https://www.fia.com/system/files/documents/fia_2026_f1_regulations_-_section_c_technical_-_iss_20_-_2026-08-05.pdf",
    ),  # noqa: E501
    (
        "2026_section_d_financial_teams",
        "https://www.fia.com/system/files/documents/fia_2026_f1_regulations_-_section_d_financial_-_f1_teams_-_iss_07_-_2026-06-25.pdf",
    ),  # noqa: E501
    (
        "2026_section_e_financial_pu",
        "https://www.fia.com/system/files/documents/fia_2026_f1_regulations_-_section_e_financial_-_pu_manufacturers_-_iss_06_-_2026-06-25.pdf",
    ),  # noqa: E501
    (
        "2026_section_f_operational",
        "https://www.fia.com/system/files/documents/fia_2026_f1_regulations_-_section_f_operational_-_iss_10_-_2026-08-05.pdf",
    ),  # noqa: E501
]

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def download(label: str, url: str) -> str:
    """Download one PDF to data/raw/ if not already there. Returns a status string."""
    out_path = RAW_DIR / f"{label}.pdf"
    if out_path.exists() and out_path.stat().st_size > 0:
        return f"skip    {label} (already downloaded)"
    response = requests.get(url, timeout=30)
    response.raise_for_status()  # turns "404 Not Found" into an error we can see
    out_path.write_bytes(response.content)
    return f"fetched {label} ({len(response.content):,} bytes)"


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for label, url in DOCUMENTS:
        print(download(label, url))


if __name__ == "__main__":
    main()
