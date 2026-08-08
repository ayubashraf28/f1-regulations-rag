"""Download FIA F1 regulation PDFs and stewards' decisions into data/raw/.

Run:  uv run python scripts/download_documents.py
Safe to re-run: files that already exist are skipped (no re-downloading).
"""

import re
import time
from pathlib import Path

import requests

BASE_URL = "https://www.fia.com"
HEADERS = {"User-Agent": "f1-regulations-rag-portfolio/0.1"}

CHAMPIONSHIP = "/documents/championships/fia-formula-one-world-championship-14"

# Season pages found via the site's own filter dropdown (2026-08-08)
SEASONS = [
    ("2024", f"{BASE_URL}{CHAMPIONSHIP}/season/season-2024-2043"),
    ("2025", f"{BASE_URL}{CHAMPIONSHIP}/season/season-2025-2071"),
    ("2026", f"{BASE_URL}{CHAMPIONSHIP}/season/season-2026-2072"),
]

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


def find_decision_links(page_url: str) -> list[str]:
    """Return relative PDF paths found on a FIA documents page."""
    response = requests.get(page_url, timeout=30, headers=HEADERS)
    response.raise_for_status()
    links = re.findall(r'href="(/system/files/decision-document/[^"]+\.pdf)"', response.text)
    return list(dict.fromkeys(links))  # dedupe, keep order


def find_event_urls(season_url: str) -> list[str]:
    """Find every event URL listed on a season's documents page."""
    response = requests.get(season_url, timeout=30, headers=HEADERS)
    response.raise_for_status()
    relative = re.findall(r'<option value="([^"]*/event/[^"]+)">', response.text)
    return [BASE_URL + path for path in dict.fromkeys(relative)]


def download_decisions(season_url: str, pause: float = 0.3) -> None:
    """Download every decision PDF for every event of a season."""
    target = RAW_DIR / "decisions"
    target.mkdir(parents=True, exist_ok=True)
    event_urls = find_event_urls(season_url)
    print(f"{len(event_urls)} events found")
    for event_url in event_urls:
        for link in find_decision_links(event_url):
            url = BASE_URL + link
            name = Path(link).stem
            out_path = target / f"{name}.pdf"
            if out_path.exists() and out_path.stat().st_size > 0:
                print(f"skip    {name}")
                continue
            response = requests.get(url, timeout=30, headers=HEADERS)
            response.raise_for_status()
            out_path.write_bytes(response.content)
            print(f"fetched {name} ({len(response.content):,} bytes)")
            time.sleep(pause)  # be polite to the site


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for label, url in DOCUMENTS:
        print(download(label, url))
    for year, season_url in SEASONS:
        print(f"--- {year} season decisions ---")
        download_decisions(season_url)


if __name__ == "__main__":
    main()
