"""Turn the RvIG gezag specifications (Gherkin, in Dutch) into JSON test cases.

RvIG describes every derivation rule of the gezag algorithm as a Gherkin feature file in
Dutch: a ``Functionaliteit`` with ``Regel`` blocks, and per rule ``Voorbeeld`` scenarios with
``Gegeven`` / ``Als`` / ``Dan`` steps. This module reads those files and writes them as plain
data, so teams can use the examples as test cases without running RvIG's Java module.

    # regenerate data/rvig-gezag/scenarios.json from a local clone of BRP-API/brp-api-gezag
    python -m openalgoritme.specs build --source ../../brp-api-gezag

    # CI: is the committed file what the pinned RvIG commit produces?
    python -m openalgoritme.specs build --source ../../brp-api-gezag --check

    # browse the committed test cases
    python -m openalgoritme.specs list --outcome niet_te_bepalen
    python -m openalgoritme.specs show twee-ouders-met-relatie:20

Step texts, rule texts and outcomes are copied unchanged. What this module adds: an id per
scenario (``<file>:<line>``), the person each ``*`` step is about, and a parsed outcome with a
type such as ``gezamenlijk_ouderlijk_gezag``. Those type names are this repository's own labels.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from .paths import SCENARIOS_FILE

REPOSITORY = "https://github.com/BRP-API/brp-api-gezag"
SPEC_DIR = "features/specs"
# The rule specifications. The S-en-T-test folders hold RvIG's integration tests and are left out.
FOLDERS = ("", "gezag-minderjarige", "gezag-meerderjarige")
COPYRIGHT = "Copyright © RvIG 2022"
LICENCE = "EUPL-1.2"

STEP = re.compile(r"^(Gegeven|Als|Dan|En|Maar|\*)\s+(.*)$")
PERSON_INTRO = re.compile(r"^(?:de )?(?:minderjarige )?persoon '([^']+)'(?: met burgerservicenummer '(\d+)')?")
PERSON_ONLY = re.compile(r"^(?:de )?persoon '[^']+'(?: met burgerservicenummer '\d+'| zonder burgerservicenummer)?$")
WHEN = re.compile(r"^'([^']+)' wordt gevraagd van '([^']+)'$")
OUTCOME = re.compile(r"^is het gezag over '([^']+)' (.+)$")
RELATIONS = re.compile(r"^heeft '([^']+)' de volgende gezagsrelaties$")
NO_HOLDER = re.compile(r"^heeft '([^']+)' geen gezaghouder$")
EXPLANATION = re.compile(r"^(?P<body>.*?) met de toelichting '(?P<text>.*)'$")
# Sentences without their own subject ("is meerderjarig") are about the last person introduced.
SUBJECTLESS = re.compile(r"^(is|heeft|zijn|staat|was|wordt) ")

OUTCOME_TYPES = (
    "gezamenlijk_ouderlijk_gezag",
    "eenhoofdig_ouderlijk_gezag",
    "gezamenlijk_gezag",
    "voogdij",
    "tijdelijk_geen_gezag",
    "niet_te_bepalen",
    "geen_gezag",
    "geen_gezaghouder",
    "onbekend",
)

_PATTERNS = [
    ("gezamenlijk_ouderlijk_gezag",
     r"^gezamenlijk ouderlijk gezag met ouder '(?P<p1>[^']+)' en ouder '(?P<p2>[^']+)'$"),
    ("eenhoofdig_ouderlijk_gezag", r"^eenhoofdig ouderlijk gezag met ouder '(?P<p1>[^']+)'$"),
    ("gezamenlijk_gezag", r"^gezamenlijk gezag met ouder '(?P<p1>[^']+)' en derde '(?P<t1>[^']+)'$"),
    ("gezamenlijk_gezag", r"^gezamenlijk gezag met ouder '(?P<p1>[^']+)' en (?P<unknown>een onbekende derde)$"),
    ("gezamenlijk_gezag", r"^gezamenlijk gezag met ouder '(?P<p1>[^']+)' en ouder '(?P<p2>[^']+)'$"),
    ("voogdij", r"^voogdij(?: met derde '(?P<t1>[^']+)')?$"),
    ("tijdelijk_geen_gezag", r"^tijdelijk geen gezag$"),
    ("niet_te_bepalen", r"^niet te bepalen$"),
]
PATTERNS = [(name, re.compile(rx)) for name, rx in _PATTERNS]


# --------------------------------------------------------------------------------------------
# Reading feature files
# --------------------------------------------------------------------------------------------


@dataclass
class Step:
    keyword: str
    text: str
    line: int
    table: list[list[str]] = field(default_factory=list)


@dataclass
class Examples:
    line: int
    tags: list[str]
    header: list[str] | None = None
    rows: list[list[str]] = field(default_factory=list)


@dataclass
class Scenario:
    title: str
    line: int
    tags: list[str]
    outline: bool
    steps: list[Step] = field(default_factory=list)
    examples: list[Examples] = field(default_factory=list)


@dataclass
class Rule:
    title: str | None
    line: int | None
    tags: list[str] = field(default_factory=list)
    description: list[str] = field(default_factory=list)
    background: list[Step] = field(default_factory=list)
    scenarios: list[Scenario] = field(default_factory=list)


@dataclass
class Feature:
    file: str
    title: str = ""
    tags: list[str] = field(default_factory=list)
    description: list[str] = field(default_factory=list)
    background: list[Step] = field(default_factory=list)
    rules: list[Rule] = field(default_factory=list)


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse_feature(text: str, file: str) -> Feature:
    """Parse one Gherkin file in Dutch. Supports the constructs RvIG uses, nothing more."""
    feature = Feature(file=file)
    rule = Rule(title=None, line=None)  # scenarios outside any Regel
    feature.rules.append(rule)
    tags: list[str] = []
    steps: list[Step] | None = None  # where the next step goes
    scenario: Scenario | None = None
    examples: Examples | None = None
    context = "feature"

    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("@"):
            tags += [t[1:] for t in line.split() if t.startswith("@")]
            continue
        keyword, _, rest = line.partition(":")
        rest = rest.strip()
        if keyword == "Functionaliteit":
            feature.title, feature.tags, tags = rest, tags, []
            context, steps = "feature", None
        elif keyword == "Achtergrond":
            steps = rule.background if rule.title else feature.background
            context, scenario, examples = "background", None, None
        elif keyword == "Regel":
            rule = Rule(title=rest, line=number, tags=tags)
            feature.rules.append(rule)
            context, steps, scenario, examples, tags = "rule", None, None, None, []
        elif keyword in ("Voorbeeld", "Scenario", "Abstract Scenario", "Scenariosjabloon"):
            outline = keyword in ("Abstract Scenario", "Scenariosjabloon")
            scenario = Scenario(title=rest, line=number, tags=tags, outline=outline)
            rule.scenarios.append(scenario)
            context, steps, examples, tags = "scenario", scenario.steps, None, []
        elif keyword == "Voorbeelden":
            if scenario is None:
                raise ValueError(f"{file}:{number}: 'Voorbeelden' outside a scenario")
            examples = Examples(line=number, tags=tags)
            scenario.examples.append(examples)
            context, tags = "examples", []
        elif line.startswith("|") and context in ("feature", "rule"):
            (feature.description if context == "feature" else rule.description).append(line)
        elif line.startswith("|"):
            if context == "examples" and examples is not None:
                if examples.header is None:
                    examples.header = _cells(line)
                else:
                    examples.rows.append(_cells(line))
            elif steps:
                steps[-1].table.append(_cells(line))
            else:
                raise ValueError(f"{file}:{number}: table without a step")
        elif context in ("background", "scenario") and (m := STEP.match(line)):
            steps.append(Step(keyword=m.group(1), text=m.group(2).strip(), line=number))
        elif context == "feature":
            feature.description.append(line)
        elif context == "rule":
            rule.description.append(line)
        else:
            raise ValueError(f"{file}:{number}: unexpected line {line!r}")
    return feature


# --------------------------------------------------------------------------------------------
# From parsed features to test cases
# --------------------------------------------------------------------------------------------


def _substitute(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace(f"<{key}>", value)
    return text


def _table(rows: list[list[str]]) -> list[dict[str, str]] | None:
    if not rows:
        return None
    header, *body = rows
    return [dict(zip(header, row, strict=False)) for row in body]


def parse_outcome(about: str | None, rest: str, text: str) -> dict:
    """Parse the part after "is het gezag over 'X' " into a structured outcome."""
    outcome = {
        "about": about,
        "type": "onbekend",
        "parents": [],
        "third_parties": [],
        "unknown_third_party": False,
        "explanation": None,
        "under_investigation": False,
        "text": text,
    }
    body = rest
    if m := EXPLANATION.match(rest):
        body, outcome["explanation"] = m.group("body"), m.group("text")
    for name, pattern in PATTERNS:
        if m := pattern.match(body):
            groups = m.groupdict()
            outcome["type"] = name
            outcome["parents"] = [groups[k] for k in ("p1", "p2") if groups.get(k)]
            outcome["third_parties"] = [groups["t1"]] if groups.get("t1") else []
            outcome["unknown_third_party"] = bool(groups.get("unknown"))
            break
    return outcome


def _blank_outcome(type_: str, text: str, about: str | None = None) -> dict:
    outcome = parse_outcome(about, "", text)
    outcome["type"] = type_
    return outcome


def build_case(feature: Feature, rule: Rule, scenario: Scenario, steps: list[Step], *, case_id: str,
               title: str, tags: list[str], line: int) -> dict:
    persons: list[dict] = []
    given: list[dict] = []
    outcomes: list[dict] = []
    when = None
    perspective = "minderjarige"
    phase = "given"
    subject: str | None = None

    for step in steps:
        if step.keyword == "Als":
            phase = "when"
        elif step.keyword == "Dan":
            phase = "then"
        text = step.text

        if phase == "given":
            step_subject = None
            if m := PERSON_INTRO.match(text):
                subject = m.group(1)
                if all(p["name"] != subject for p in persons):
                    persons.append({"name": subject, "bsn": m.group(2)})
            elif step.keyword == "*" or SUBJECTLESS.match(text):
                step_subject = subject
            item = {"keyword": step.keyword, "text": text, "line": step.line}
            if step_subject:
                item["subject"] = step_subject
            if step.table:
                item["table"] = _table(step.table)
            given.append(item)
        elif phase == "when":
            if m := WHEN.match(text):
                when = {"field": m.group(1), "person": m.group(2)}
            else:
                when = {"field": None, "person": None, "text": text}
        else:
            if m := OUTCOME.match(text):
                outcomes.append(parse_outcome(m.group(1), m.group(2), text))
            elif RELATIONS.match(text):
                perspective = "meerderjarige"
            elif text == "heeft de persoon geen gezag":
                outcomes.append(_blank_outcome("geen_gezag", text))
            elif text == "is het gezag in onderzoek" and outcomes:
                outcomes[-1]["under_investigation"] = True
            elif m := NO_HOLDER.match(text):
                outcomes.append(_blank_outcome("geen_gezaghouder", text, about=m.group(1)))
            else:
                outcomes.append(_blank_outcome("onbekend", text))

    return {
        "id": case_id,
        "source": {"file": f"{SPEC_DIR}/{feature.file}", "line": line},
        "feature": feature.title,
        "rule": rule.title,
        "title": title,
        "tags": tags,
        "persons": persons,
        "given": given,
        "when": when,
        "perspective": perspective,
        "outcomes": outcomes,
    }


def cases_from_feature(feature: Feature) -> list[dict]:
    stem = feature.file.removesuffix(".feature")
    cases = []
    for rule in feature.rules:
        for scenario in rule.scenarios:
            base_tags = feature.tags + rule.tags + scenario.tags
            steps = feature.background + rule.background + scenario.steps
            if not (scenario.outline or scenario.examples):  # a Voorbeeld with Voorbeelden is an outline too
                cases.append(build_case(feature, rule, scenario, steps, case_id=f"{stem}:{scenario.line}",
                                        title=scenario.title, tags=base_tags, line=scenario.line))
                continue
            n = 0
            for examples in scenario.examples:
                for row in examples.rows:
                    n += 1
                    values = dict(zip(examples.header or [], row, strict=False))
                    expanded = [
                        Step(s.keyword, _substitute(s.text, values), s.line,
                             [[_substitute(c, values) for c in r] for r in s.table])
                        for s in steps
                    ]
                    cases.append(build_case(
                        feature, rule, scenario, expanded, case_id=f"{stem}:{scenario.line}:{n}",
                        title=_substitute(scenario.title, values), tags=base_tags + examples.tags,
                        line=scenario.line,
                    ))
    return cases


def feature_files(source: Path) -> list[Path]:
    root = source / SPEC_DIR
    files: list[Path] = []
    for folder in FOLDERS:
        files += sorted((root / folder).glob("*.feature"))
    return files


def _git(source: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(source), *args], check=True, capture_output=True,
                          text=True).stdout.strip()


def build(source: Path, converted: str, commit: str | None = None, commit_date: str | None = None) -> dict:
    root = source / SPEC_DIR
    features, cases = [], []
    for path in feature_files(source):
        rel = path.relative_to(root).as_posix()
        feature = parse_feature(path.read_text(encoding="utf-8"), rel)
        features.append({
            "file": f"{SPEC_DIR}/{rel}",
            "title": feature.title,
            "description": "\n".join(feature.description),
            "rules": [r.title for r in feature.rules if r.title],
        })
        cases += cases_from_feature(feature)
    return {
        "source": {
            "repository": REPOSITORY,
            "commit": commit or _git(source, "rev-parse", "HEAD"),
            "commit_date": commit_date or _git(source, "log", "-1", "--format=%cs"),
            "path": SPEC_DIR,
            "folders": [f"{SPEC_DIR}/{f}".rstrip("/") for f in FOLDERS],
            "licence": LICENCE,
            "copyright": COPYRIGHT,
        },
        "modification": {
            "date": converted,
            "by": "govtechnl/onegov3-open-algoritme",
            "description": (
                "Converted from the Gherkin feature files to JSON with tooling/openalgoritme/specs.py. "
                "Step texts, rule texts and outcomes are unchanged. Added: ids, the person each '*' step "
                "is about, parsed outcomes with this repository's own type names, backgrounds repeated "
                "in every scenario, abstract scenarios expanded per example row."
            ),
        },
        "features": features,
        "scenarios": cases,
    }


# Lists whose items are written on one line each: one step, outcome or person per line.
ONE_LINE_ITEMS = {"given", "outcomes", "persons"}


def _fmt(value, depth: int = 0, items_on_one_line: bool = False) -> str:
    pad = "  " * depth
    if isinstance(value, dict) and any(isinstance(v, (dict, list)) for v in value.values()):
        items = [f"{pad}  {json.dumps(k, ensure_ascii=False)}: {_fmt(v, depth + 1, k in ONE_LINE_ITEMS)}"
                 for k, v in value.items()]
        return "{\n" + ",\n".join(items) + f"\n{pad}}}"
    if isinstance(value, list) and any(isinstance(v, (dict, list)) for v in value):
        if items_on_one_line:
            items = [f"{pad}  {json.dumps(v, ensure_ascii=False)}" for v in value]
        else:
            items = [f"{pad}  {_fmt(v, depth + 1)}" for v in value]
        return "[\n" + ",\n".join(items) + f"\n{pad}]"
    return json.dumps(value, ensure_ascii=False)


def dumps(data: dict) -> str:
    """JSON with one step, outcome or person per line: readable in a diff, valid for any parser."""
    return _fmt(data) + "\n"


# --------------------------------------------------------------------------------------------
# Using the committed test cases
# --------------------------------------------------------------------------------------------


def load(path: Path = SCENARIOS_FILE) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def scenario_by_id(data: dict, case_id: str) -> dict:
    for case in data["scenarios"]:
        if case["id"] == case_id:
            return case
    raise KeyError(f"unknown scenario id {case_id!r}; see 'python -m openalgoritme.specs list'")


def source_url(data: dict, case: dict) -> str:
    src = data["source"]
    return f"{src['repository']}/blob/{src['commit']}/{case['source']['file']}#L{case['source']['line']}"


def unquote(text: str) -> str:
    return re.sub(r"'([^']*)'", r"\1", text)


def readable(step: dict) -> str | None:
    """A given step as a plain sentence, or None for steps that only introduce a person."""
    text = step["text"]
    if PERSON_ONLY.match(text):
        return None
    if step.get("subject"):
        text = f"{step['subject']} {text}"
    text = unquote(text)
    if step.get("table"):
        values = "; ".join(f"{k}: {v}" for row in step["table"] for k, v in row.items() if v)
        if values:
            text = text.removesuffix(" met de volgende gegevens") + f" ({values})"
    return text[:1].upper() + text[1:]


# --------------------------------------------------------------------------------------------
# Command line
# --------------------------------------------------------------------------------------------


def _cmd_build(args: argparse.Namespace) -> int:
    out = Path(args.out)
    converted = args.converted
    if converted is None:
        converted = load(out)["modification"]["date"] if out.exists() else date.today().isoformat()
    text = dumps(build(Path(args.source), converted, commit=args.commit, commit_date=args.commit_date))
    unknown = text.count('"type": "onbekend"')
    if unknown:
        print(f"warning: {unknown} outcome(s) could not be parsed (type 'onbekend')", file=sys.stderr)
    if args.check:
        if not out.exists() or out.read_text(encoding="utf-8") != text:
            print(f"{out} is out of date; run 'python -m openalgoritme.specs build --source ...'",
                  file=sys.stderr)
            return 1
        print(f"{out} is up to date")
        return 0
    out.write_text(text, encoding="utf-8")
    print(f"wrote {out} ({len(load(out)['scenarios'])} scenarios)")
    return 0


def _types(case: dict) -> str:
    return ", ".join(o["type"] for o in case["outcomes"]) or "-"


def _cmd_list(args: argparse.Namespace) -> int:
    data = load()
    for case in data["scenarios"]:
        if args.outcome and all(o["type"] != args.outcome for o in case["outcomes"]):
            continue
        if args.file and args.file not in case["source"]["file"]:
            continue
        print(f"{case['id']:<58} {_types(case):<30} {case['title'][:70]}")
    return 0


def _cmd_show(args: argparse.Namespace) -> int:
    data = load()
    try:
        case = scenario_by_id(data, args.id)
    except KeyError as err:
        print(f"error: {err.args[0]}", file=sys.stderr)
        return 2
    print(f"{case['id']}  ({case['feature']})")
    print(f"Scenario: {case['title']}")
    if case["rule"]:
        print(f"Regel:    {case['rule']}")
    print(f"Bron:     {source_url(data, case)}")
    if case["tags"]:
        print(f"Tags:     {', '.join(case['tags'])}")
    print("\nGegeven:")
    for step in case["given"]:
        sentence = readable(step)
        if sentence:
            print(f"  - {sentence}")
    if case["when"]:
        print(f"\nGevraagd: {case['when'].get('field')} van {case['when'].get('person')}")
    print("\nUitkomst:")
    for outcome in case["outcomes"]:
        print(f"  - [{outcome['type']}] {unquote(outcome['text'])}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m openalgoritme.specs", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("build", help="convert the RvIG feature files to JSON")
    p.add_argument("--source", required=True, help="local clone of BRP-API/brp-api-gezag")
    p.add_argument("--out", default=str(SCENARIOS_FILE))
    p.add_argument("--check", action="store_true", help="fail if --out differs from a fresh build")
    p.add_argument("--converted", help="date of conversion (default: keep the date in --out)")
    p.add_argument("--commit", help="RvIG commit (default: read with git)")
    p.add_argument("--commit-date", help="RvIG commit date (default: read with git)")
    p.set_defaults(func=_cmd_build)

    p = sub.add_parser("list", help="list the test cases")
    p.add_argument("--outcome", choices=OUTCOME_TYPES)
    p.add_argument("--file", help="only scenarios whose file path contains this text")
    p.set_defaults(func=_cmd_list)

    p = sub.add_parser("show", help="show one test case in plain Dutch")
    p.add_argument("id")
    p.set_defaults(func=_cmd_show)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
