"""Laag 1: a plain-language motivering for one fictional case.

The explanation is built from four sources, and every sentence can be traced back to one of them:

1. the test case (data/rvig-gezag/scenarios.json): the facts, the rule and the outcome;
2. the registration (data/algoritmeregister/gezag-61781447.json): who runs the algorithm, on
   which legal basis, and what the registration check finds missing (Laag 2);
3. the templates (data/uitleg/gezag.yaml): plain Dutch per outcome type;
4. the decision (data/besluiten/*.yaml): why gezag matters for this decision, and what follows.

    python -m openalgoritme.explain                                     # default example
    python -m openalgoritme.explain --scenario niet-ingezetene:40
    python -m openalgoritme.explain --scenario geen-gezag:10 --besluit geen
    python -m openalgoritme.explain --format json

Nothing here is a language model: the same input always gives the same text. That is a choice for
the starter, not a rule for teams (see docs/integrations/greenpt-api.md).
"""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path

import yaml

from . import __version__
from .check import STATUSES, dutch_date, run_checks, summary
from .paths import BESLUITEN_DIR, EXAMPLES_DIR, SCENARIOS_FILE, SNAPSHOT_FILE, UITLEG_FILE
from .register import is_url, links, load_snapshot, page_url
from .specs import load, readable, scenario_by_id, source_url, unquote

DEFAULT_SCENARIO = "twee-ouders-met-relatie:19"
DEFAULT_BESLUIT = "reisdocument-minderjarige"
# The worked examples in data/rvig-gezag/examples/ (regenerate with --write-examples; a test checks them).
EXAMPLES = {
    "twee-ouders-met-relatie:19": "motivering-gezamenlijk-ouderlijk-gezag.md",
    "gezag-meerderjarige/meerderjarige-rni:18": "motivering-gezag-niet-te-bepalen.md",
}
NOTICE = ("Voorbeeld met fictieve personen uit de testgevallen van de Rijksdienst voor Identiteitsgegevens, "
          "gemaakt met de startrepository van OneGov #3. Dit is geen echt besluit.")


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def load_besluit(name: str) -> dict | None:
    if name == "geen":
        return None
    path = Path(name) if name.endswith((".yaml", ".yml")) else BESLUITEN_DIR / f"{name}.yaml"
    return load_yaml(path)


def join_names(names: list[str]) -> str:
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + " en " + names[-1]


def holders(outcome: dict) -> str:
    names = list(outcome["parents"]) + list(outcome["third_parties"])
    if outcome["unknown_third_party"]:
        names.append("iemand van wie de naam niet bekend is")
    if not names and outcome["type"] == "voogdij":
        names = ["een voogd"]
    return join_names(names)


def _fill(template: str, **values: str) -> str:
    return " ".join(template.format(**values).split())


def explain(case: dict, data: dict, snap: dict, uitleg: dict, besluit: dict | None) -> dict:
    """Build the motivering as data: a title, sections of paragraphs and items, and an audit trail."""
    record = snap["record"]
    when = case.get("when") or {}
    if besluit and besluit.get("perspectief") and case["perspective"] != besluit["perspectief"]:
        raise ValueError(f"scenario {case['id']} asks about a {case['perspective']}; the decision "
                         f"'{besluit['id']}' needs a {besluit['perspectief']}. Use --besluit geen.")
    first = case["outcomes"][0]
    kind = first["about"] or when.get("person") or ""
    values = {"kind": kind, "persoon": when.get("person") or "", "organisatie": record["organization"],
              "naam": record["name"], "bestuursorgaan": (besluit or {}).get("bestuursorgaan", "de organisatie")}
    sections: list[dict] = []

    if besluit:
        grondslag = besluit.get("grondslag") or []
        paragraphs = [_fill(besluit["aanleiding"], **values), _fill(besluit["waarom_gezag"], **values)]
        if besluit.get("grondslag_zin"):
            paragraphs.append(_fill(besluit["grondslag_zin"], **values))
        elif grondslag:
            paragraphs.append("Grondslag: " + join_names([g["titel"] for g in grondslag]) + ".")
        sections.append({"title": "Waarom kijken we naar het gezag?", "paragraphs": paragraphs})

    paragraphs = []
    for outcome in case["outcomes"]:
        template = uitleg["uitkomsten"][outcome["type"]]
        v = {**values, "kind": outcome["about"] or kind, "houders": holders(outcome)}
        paragraphs.append(_fill(template["uitleg"], **v) + " " + _fill(template["betekenis"], **v))
        if outcome["explanation"]:
            paragraphs.append(_fill(uitleg["toelichting"], toelichting=outcome["explanation"]))
        if outcome["under_investigation"]:
            paragraphs.append(_fill(uitleg["in_onderzoek"]))
    minor = case["perspective"] == "minderjarige"
    title = "Wie heeft het gezag?" if minor else f"Over wie heeft {values['persoon']} gezag?"
    sections.append({"title": title, "paragraphs": paragraphs})

    facts = [s for s in (readable(step) for step in case["given"]) if s]
    sections.append({"title": "Welke gegevens zijn gebruikt?", "paragraphs": [uitleg["algoritme"]["gegevens"]],
                     "items": facts})

    rule = unquote(case["rule"]) if case["rule"] else f"{case['feature']}: {unquote(case['title'])}"
    sections.append({"title": "Welke regel is toegepast?", "paragraphs": [
        rule[:1].upper() + rule[1:] + ("" if rule.endswith(".") else "."),
        f"{uitleg['algoritme']['regel']} Zie [{case['source']['file']}, regel {case['source']['line']}]"
        f"({source_url(data, case)}).",
    ]})

    if besluit:
        gevolg = besluit["gevolg"][first["type"]]
        sections.append({"title": "Wat betekent dit voor uw aanvraag?",
                         "paragraphs": [_fill(gevolg, **values, houders=holders(first))],
                         "items": [_fill(v) for v in besluit.get("vervolg", [])]})

    who = [_fill(uitleg["algoritme"]["rol"], **values)]
    if besluit:
        who.append(f"Het besluit over uw aanvraag neemt {besluit['bestuursorgaan']}.")
    who.append(_fill(uitleg["algoritme"]["terugmelding"], **values))
    sections.append({"title": "Wie besliste wat?", "paragraphs": who})

    if besluit:
        sections.append({"title": "Klopt er iets niet?",
                         "paragraphs": [_fill(besluit["correctie"]), _fill(besluit["bezwaar"])]})

    sources = [f"[Registratie in het Algoritmeregister]({snap.get('page') or page_url(record)})",
               f"[Afleidingsregel: {case['source']['file']}, regel {case['source']['line']}]"
               f"({source_url(data, case)})"]
    sources += [f"[{g['title']}]({g['link']})" for g in links(record, "lawful_basis_grouping") if is_url(g.get("link"))]
    if besluit:
        sources += [f"[{g['titel']}]({g['url']})" for g in besluit.get("grondslag", []) + besluit.get("bronnen", [])]
    sections.append({"title": "Bronnen", "items": sources})

    retrieved = date.fromisoformat(snap["retrieved"])
    changed = datetime.fromisoformat(record["create_dt"].replace("Z", "+00:00")).date()
    counts = summary(run_checks(record, retrieved))
    audit = {
        "scenario": case["id"],
        "afleidingsregel": f"{case['source']['file']}:{case['source']['line']} @ {data['source']['commit'][:12]}",
        "registratie": f"LARS {record['lars']}, laatst gewijzigd {dutch_date(changed)}, "
                       f"momentopname {dutch_date(retrieved)}",
        "registratiecheck": "; ".join(f"{status}: {', '.join(counts[status])}"
                                      for status in STATUSES if counts[status] and status != "ok"),
        "sjablonen": f"data/uitleg/gezag.yaml; besluit: {besluit['id'] if besluit else 'geen'}",
        "tool": f"openalgoritme {__version__}",
    }
    if besluit:
        heading = _fill(besluit["titel"], **values)
    else:
        heading = f"Uitleg: gezag over {kind}" if minor else f"Uitleg: gezag van {values['persoon']}"
    return {"title": heading, "notice": NOTICE, "sections": sections, "audit": audit}


def to_markdown(doc: dict) -> str:
    lines = [f"# {doc['title']}", "", f"> {doc['notice']}", ""]
    for section in doc["sections"]:
        lines += [f"## {section['title']}", ""]
        for paragraph in section.get("paragraphs", []):
            lines += [paragraph, ""]
        if section.get("items"):
            lines += [f"- {item}" for item in section["items"]] + [""]
    lines += ["## Verantwoording", "", "| | |", "|---|---|"]
    lines += [f"| {key} | {value} |" for key, value in doc["audit"].items()]
    return "\n".join(lines) + "\n"


def example_markdown(case_id: str) -> str:
    data = load(SCENARIOS_FILE)
    doc = explain(scenario_by_id(data, case_id), data, load_snapshot(SNAPSHOT_FILE), load_yaml(UITLEG_FILE),
                  load_besluit(DEFAULT_BESLUIT))
    return to_markdown(doc)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m openalgoritme.explain", description=__doc__.splitlines()[0])
    parser.add_argument("--scenario", default=DEFAULT_SCENARIO, help="test case id, see 'specs list'")
    parser.add_argument("--besluit", default=DEFAULT_BESLUIT,
                        help="decision in data/besluiten (name or path), or 'geen' for none")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--out", help="write to this file instead of printing")
    parser.add_argument("--write-examples", action="store_true", help=f"regenerate {EXAMPLES_DIR.name}/ and stop")
    args = parser.parse_args(argv)

    if args.write_examples:
        for case_id, name in EXAMPLES.items():
            (EXAMPLES_DIR / name).write_text(example_markdown(case_id), encoding="utf-8")
            print(f"wrote {EXAMPLES_DIR / name}")
        return 0

    data = load(SCENARIOS_FILE)
    try:
        case = scenario_by_id(data, args.scenario)
        doc = explain(case, data, load_snapshot(SNAPSHOT_FILE), load_yaml(UITLEG_FILE), load_besluit(args.besluit))
    except (KeyError, ValueError) as err:
        parser.exit(2, f"error: {err.args[0]}\n")
    text = to_markdown(doc) if args.format == "markdown" else json.dumps(doc, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
