"""Read registrations from the Algoritmeregister (algoritmes.overheid.nl).

The repository holds a snapshot of the registration of the gezag algorithm (LARS 61781447).
The register also has a public JSON API, so the same code works for any other registration.

    python -m openalgoritme.register show                    # the snapshot, as plain text
    python -m openalgoritme.register show --field risks      # one field
    python -m openalgoritme.register fetch 61781447 --out ../data/algoritmeregister/gezag-61781447.json
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import urllib.request
from datetime import date
from pathlib import Path

from .paths import SNAPSHOT_FILE

API = "https://algoritmes.overheid.nl/api/algoritme/{language}/{lars}"
PAGE = "https://algoritmes.overheid.nl/nl/algoritme/{org_id}/{lars}/{slug}"
TERMS = "https://algoritmes.overheid.nl/nl/footer/copyright"

# Labels as algoritmes.overheid.nl shows them, checked on 24 November 2026 on the page of the gezag
# registration. The site only shows filled fields, so fields this registration leaves empty have no
# checked label here; they are shown by their API name.
LABELS = {
    "category": "Thema",
    "begin_date": "Begindatum",
    "contact_email": "Contactgegevens",
    "website": "Link naar publiekspagina",
    "status": "Status",
    "publication_category": "Publicatiecategorie",
    "goal": "Doel en impact",
    "proportionality": "Afwegingen",
    "human_intervention": "Menselijke tussenkomst",
    "risks": "Risicobeheer",
    "lawful_basis": "Wettelijke basis",
    "lawful_basis_grouping": "Links naar wettelijke basis",
    "process_index_url": "Link naar verwerkingsregister",
    "impacttoetsen_grouping": "Impacttoetsen",
    "source_data": "Gegevens",
    "source_data_grouping": "Links naar gegevensbronnen",
    "methods_and_models": "Technische werking",
    "provider": "Leverancier",
    "publiccode": "Link naar broncode",
}


def label(field: str) -> str:
    return LABELS.get(field, field)


def load_snapshot(path: Path = SNAPSHOT_FILE) -> dict:
    """The snapshot file: provenance plus the unmodified API response under ``record``."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def html_to_text(value: str | None) -> str:
    """Plain text from the HTML the register stores: paragraphs as lines, list items as '- '."""
    if not value:
        return ""
    text = value.replace(" ", " ")
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?i)<li[^>]*>", "\n- ", text)
    text = re.sub(r"(?i)</li>", "", text)
    text = re.sub(r"(?i)</(p|div|ul|ol)>", "\n", text)
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    lines: list[str] = []
    for line in text.splitlines():
        line = re.sub(r"[ \t]+", " ", line).strip()
        if line or (lines and lines[-1]):
            lines.append(line)
    return "\n".join(lines).strip()


def is_empty(value) -> bool:
    return value is None or value == "" or value == []


def is_url(value: str | None) -> bool:
    return bool(value) and re.match(r"^https?://\S+$", value.strip()) is not None


def links(record: dict, field: str) -> list[dict]:
    """The ``*_grouping`` fields: a list of {title, link}. The link is not always a URL."""
    value = record.get(field) or []
    return [item for item in value if isinstance(item, dict)]


def field_text(record: dict, field: str) -> str:
    value = record.get(field)
    if is_empty(value):
        return ""
    if isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, dict):
                title, link = item.get("title") or "", item.get("link") or ""
                parts.append(f"{title}: {link}" if title and link else title or link)
            else:
                parts.append(str(item))
        return "\n".join(parts)
    if isinstance(value, str):
        return html_to_text(value)
    return str(value)


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def page_url(record: dict) -> str:
    return PAGE.format(org_id=record["org_id"], lars=record["lars"], slug=slug(record["name"]))


def fetch(lars: str, language: str = "NLD", timeout: float = 30) -> dict:
    """One registration from the public API. Needs internet access."""
    url = API.format(language=language, lars=lars)
    request = urllib.request.Request(url, headers={"Accept": "application/json",
                                                   "User-Agent": "onegov3-open-algoritme"})
    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310 (fixed https URL)
        return json.loads(response.read().decode("utf-8"))


def record_hash(record: dict) -> str:
    """SHA-256 of the record as compact JSON (the form the API returns), to detect edits."""
    compact = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(compact.encode("utf-8")).hexdigest()


def snapshot(record: dict, retrieved: date, language: str = "NLD") -> dict:
    return {
        "source": API.format(language=language, lars=record["lars"]),
        "page": page_url(record),
        "retrieved": retrieved.isoformat(),
        "terms": TERMS,
        "note": "Unmodified response of the Algoritmeregister API. Text fields contain HTML as published.",
        "sha256": record_hash(record),
        "record": record,
    }


def _cmd_show(args: argparse.Namespace) -> int:
    snap = load_snapshot(Path(args.snapshot))
    record = snap["record"]
    fields = [args.field] if args.field else list(record)
    print(f"{record['name']} ({record['organization']}), LARS {record['lars']}")
    print(f"Bron: {snap.get('page') or snap.get('source')}, opgehaald {snap.get('retrieved')}\n")
    for field in fields:
        text = field_text(record, field)
        if text or args.field:
            heading = f"{label(field)} ({field})" if field in LABELS else field
            print(f"## {heading}\n{text or '(leeg)'}\n")
    return 0


def _cmd_fetch(args: argparse.Namespace) -> int:
    record = fetch(args.lars, args.language)
    data = snapshot(record, date.today(), args.language)
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text, end="")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m openalgoritme.register", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("show", help="print a snapshot as plain text")
    p.add_argument("--snapshot", default=str(SNAPSHOT_FILE))
    p.add_argument("--field", help="only this field (API name, for example 'goal')")
    p.set_defaults(func=_cmd_show)

    p = sub.add_parser("fetch", help="fetch a registration from the API and write a snapshot")
    p.add_argument("lars", help="the register's id of the algorithm, for example 61781447")
    p.add_argument("--language", default="NLD")
    p.add_argument("--out", help="file to write (default: print)")
    p.set_defaults(func=_cmd_fetch)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
