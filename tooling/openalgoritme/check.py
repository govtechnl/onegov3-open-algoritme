"""Laag 2: does a registration in the Algoritmeregister hold what a motivering needs?

Each check asks one question that a motivering for an individual decision has to answer, and
looks at the fields of the registration where the answer should be. This is not a test against
the publication standard of the register: a field can be optional in the standard and still be
needed to explain a decision.

    python -m openalgoritme.check                          # report for the gezag registration
    python -m openalgoritme.check --as-of 2026-12-09       # 'today' for the up-to-date check
    python -m openalgoritme.check --format json
    python -m openalgoritme.check --melding                # draft message to the owner (never sent)
    python -m openalgoritme.check --snapshot other.json    # any registration, see register.py fetch

Statuses: ``ok``; ``ontbreekt`` (missing); ``aandacht`` (present but weak, for example not
public or out of date); ``handmatig`` (a person has to read the text to decide).
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from .paths import SNAPSHOT_FILE
from .register import field_text, is_empty, is_url, label, links, load_snapshot

OK, ONTBREEKT, AANDACHT, HANDMATIG = "ok", "ontbreekt", "aandacht", "handmatig"
STATUSES = (OK, ONTBREEKT, AANDACHT, HANDMATIG)
MAX_AGE_DAYS = 365
MONTHS = ("januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september",
          "oktober", "november", "december")


def dutch_date(d: date) -> str:
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


@dataclass(frozen=True)
class Check:
    id: str
    question: str
    fields: tuple[str, ...]
    run: Callable[[dict, date], tuple[str, str]]


@dataclass(frozen=True)
class Finding:
    check: Check
    status: str
    message: str

    def as_dict(self) -> dict:
        return {"id": self.check.id, "question": self.check.question, "fields": list(self.check.fields),
                "status": self.status, "message": self.message}


def _empty(record: dict, *fields: str) -> list[str]:
    return [f for f in fields if is_empty(record.get(f))]


def _names(fields: list[str]) -> str:
    return ", ".join(f"{label(f)} ({f})" if label(f) != f else f for f in fields)


def check_what(record: dict, today: date) -> tuple[str, str]:
    missing = _empty(record, "description_short", "goal")
    if missing:
        return ONTBREEKT, f"Niet ingevuld: {_names(missing)}."
    return OK, "Korte omschrijving en doel zijn beschreven."


def check_data(record: dict, today: date) -> tuple[str, str]:
    items = [line for line in field_text(record, "source_data").splitlines() if line.strip()]
    if not items:
        return ONTBREEKT, "Er staat niet in welke gegevens het algoritme gebruikt."
    return OK, f"{len(items)} gegevens genoemd."


def check_data_sources(record: dict, today: date) -> tuple[str, str]:
    groups = links(record, "source_data_grouping")
    if not groups:
        return ONTBREEKT, "Geen bron van de gegevens genoemd."
    no_url = [g.get("title") or "?" for g in groups if not is_url(g.get("link"))]
    if no_url:
        return AANDACHT, f"Bron zonder link: {', '.join(no_url)}."
    return OK, ", ".join(g.get("title") or g["link"] for g in groups) + "."


def check_legal_basis(record: dict, today: date) -> tuple[str, str]:
    if is_empty(record.get("lawful_basis")):
        return ONTBREEKT, "Geen wettelijke grondslag beschreven."
    urls = [g for g in links(record, "lawful_basis_grouping") if is_url(g.get("link"))]
    if not urls:
        return AANDACHT, "Grondslag beschreven, maar zonder link naar de regeling."
    return OK, "Grondslag met link: " + ", ".join(g.get("title") or g["link"] for g in urls) + "."


def check_rules_public(record: dict, today: date) -> tuple[str, str]:
    has_code = is_url(record.get("publiccode"))
    has_text = not is_empty(record.get("methods_and_models"))
    if has_code and has_text:
        return OK, f"Werking beschreven, broncode openbaar: {record['publiccode']}"
    if has_code or has_text:
        return AANDACHT, "Alleen " + ("de broncode" if has_code else "een beschrijving van de werking") + "."
    return ONTBREEKT, "Geen beschrijving van de werking en geen link naar de broncode."


def check_decisions(record: dict, today: date) -> tuple[str, str]:
    filled = [f for f in ("decision_making_process", "impact") if not is_empty(record.get(f))]
    if filled:
        return OK, f"Beschreven in {_names(filled)}."
    return HANDMATIG, ("Geen apart veld ingevuld (decision_making_process, impact). Lees Doel en impact (goal) "
                       "na: staat erin voor welke besluiten de uitkomst wordt gebruikt?")


def check_human(record: dict, today: date) -> tuple[str, str]:
    if is_empty(record.get("human_intervention")):
        return ONTBREEKT, "Niet beschreven of er een mens meekijkt en wie het besluit neemt."
    return OK, "Menselijke tussenkomst is beschreven."


def check_objection(record: dict, today: date) -> tuple[str, str]:
    if is_empty(record.get("objection_procedure")):
        return ONTBREEKT, ("Geen route voor inwoners beschreven om een uitkomst aan te vechten of een gegeven "
                           "te laten verbeteren (objection_procedure is leeg).")
    return OK, "Bezwaarprocedure is beschreven."


def check_assessments(record: dict, today: date) -> tuple[str, str]:
    groups = links(record, "impacttoetsen_grouping")
    if not groups:
        return ONTBREEKT, "Geen impacttoetsen genoemd (bijvoorbeeld DPIA of IAMA)."
    closed = [g for g in groups if not is_url(g.get("link"))]
    if closed:
        return AANDACHT, "Niet openbaar: " + "; ".join(f"{g.get('title')} ({g.get('link')})" for g in closed) + "."
    return OK, "Openbaar: " + ", ".join(g.get("title") or g["link"] for g in groups) + "."


def check_up_to_date(record: dict, today: date) -> tuple[str, str]:
    stamp = record.get("create_dt")
    if not stamp:
        return HANDMATIG, "Datum van de laatste wijziging onbekend."
    changed = datetime.fromisoformat(stamp.replace("Z", "+00:00")).date()
    age = (today - changed).days
    text = f"Laatst gewijzigd op {dutch_date(changed)}"
    if age > MAX_AGE_DAYS:
        return AANDACHT, f"{text}, {age} dagen voor {dutch_date(today)}: meer dan een jaar niet bijgewerkt."
    return OK, f"{text}."


def check_contact(record: dict, today: date) -> tuple[str, str]:
    if is_empty(record.get("contact_email")):
        return ONTBREEKT, "Geen contactgegevens."
    return OK, f"Contact: {record['contact_email']}"


CHECKS = (
    Check("R01", "Wat doet het algoritme?", ("description_short", "goal"), check_what),
    Check("R02", "Welke gegevens gebruikt het?", ("source_data",), check_data),
    Check("R03", "Waar komen die gegevens vandaan?", ("source_data_grouping",), check_data_sources),
    Check("R04", "Op welke wettelijke grondslag?", ("lawful_basis", "lawful_basis_grouping"), check_legal_basis),
    Check("R05", "Zijn de regels en de code openbaar?", ("methods_and_models", "publiccode"), check_rules_public),
    Check("R06", "Voor welke besluiten wordt de uitkomst gebruikt?", ("decision_making_process", "impact", "goal"),
          check_decisions),
    Check("R07", "Kijkt er een mens mee, en wie beslist?", ("human_intervention",), check_human),
    Check("R08", "Wat kan een inwoner doen als de uitkomst niet klopt?", ("objection_procedure",), check_objection),
    Check("R09", "Zijn de impacttoetsen in te zien?", ("impacttoetsen_grouping",), check_assessments),
    Check("R10", "Is de registratie actueel?", ("create_dt",), check_up_to_date),
    Check("R11", "Bij wie kan iemand terecht met vragen?", ("contact_email",), check_contact),
)


def run_checks(record: dict, today: date, confirmed: tuple[str, ...] = ()) -> list[Finding]:
    """Run every check. ``confirmed``: ids of 'handmatig' checks a person has read and found missing."""
    findings = []
    for check in CHECKS:
        status, message = check.run(record, today)
        if status == HANDMATIG and check.id in confirmed:
            status, message = ONTBREEKT, "Niet gevonden in de registratie (handmatig beoordeeld)."
        findings.append(Finding(check, status, message))
    return findings


def summary(findings: list[Finding]) -> dict[str, list[str]]:
    return {status: [f.check.id for f in findings if f.status == status] for status in STATUSES}


def report_text(snap: dict, findings: list[Finding], today: date) -> str:
    record = snap["record"]
    lines = [
        f"Registratiecheck: {record['name']} ({record['organization']}, LARS {record['lars']})",
        f"Momentopname van {snap.get('retrieved')}, beoordeeld op {today.isoformat()}",
        "Vraag: staat in de registratie wat een motivering bij een besluit nodig heeft?",
        "",
    ]
    for f in findings:
        lines.append(f"{f.check.id}  {f.status:<10} {f.check.question}")
        lines.append(f"     {'':<10} {f.message}")
    counts = summary(findings)
    lines += ["", "Samenvatting: " + ", ".join(f"{len(v)} {k}" for k, v in counts.items())]
    return "\n".join(lines)


def melding(snap: dict, findings: list[Finding]) -> str:
    """A draft message to the owner of the algorithm. This tool never sends anything."""
    record = snap["record"]
    missing = [f for f in findings if f.status == ONTBREEKT]
    weak = [f for f in findings if f.status == AANDACHT]
    unread = [f for f in findings if f.status == HANDMATIG]
    lines = [
        f"Aan: {record.get('contact_email') or '(geen contactgegevens in de registratie)'}",
        f"Onderwerp: Aanvulling registratie '{record['name']}' (LARS {record['lars']})",
        "",
        "Beste beheerder van deze algoritmeregistratie,",
        "",
        "Bij een besluit willen we uitleggen welke rol dit algoritme speelde. Daarvoor gebruiken we de registratie "
        "in het Algoritmeregister. "
        + ("Deze informatie ontbreekt nog:" if missing else "We hebben geen ontbrekende informatie gevonden."),
        "",
    ]
    lines += [f"- {f.check.question} {f.message}" for f in missing]
    if weak:
        lines += ["", "Deze punten vragen aandacht:", ""]
        lines += [f"- {f.check.question} {f.message}" for f in weak]
    lines += [
        "",
        f"Registratie: {snap.get('page') or snap.get('source')}",
        "",
        "CONCEPT. Opgesteld door de registratiecheck van de startrepository govtechnl/onegov3-open-algoritme. "
        "Er is niets verstuurd.",
    ]
    if unread:
        lines += ["", "---", "Nog door een mens te beoordelen, niet in dit bericht opgenomen "
                  "(bevestig met --bevestig <id> als het echt ontbreekt):"]
        lines += [f"- {f.check.id} {f.check.question} {f.message}" for f in unread]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m openalgoritme.check", description=__doc__.splitlines()[0])
    parser.add_argument("--snapshot", default=str(SNAPSHOT_FILE))
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today(), help="YYYY-MM-DD")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--melding", action="store_true", help="print a draft message to the owner instead")
    parser.add_argument("--bevestig", nargs="*", default=[], metavar="ID",
                        help="ids of 'handmatig' checks a person has read and found missing, e.g. R06")
    parser.add_argument("--strict", action="store_true", help="exit 1 if anything is 'ontbreekt'")
    args = parser.parse_args(argv)

    snap = load_snapshot(Path(args.snapshot))
    findings = run_checks(snap["record"], args.as_of, tuple(args.bevestig))
    if args.melding:
        print(melding(snap, findings))
    elif args.format == "json":
        print(json.dumps({"registration": snap["record"]["lars"], "as_of": args.as_of.isoformat(),
                          "findings": [f.as_dict() for f in findings], "summary": summary(findings)},
                         ensure_ascii=False, indent=2))
    else:
        print(report_text(snap, findings, args.as_of))
    return 1 if args.strict and any(f.status == ONTBREEKT for f in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
