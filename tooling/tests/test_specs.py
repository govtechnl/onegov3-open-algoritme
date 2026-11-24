"""The Gherkin parser, and the committed test cases in data/rvig-gezag/scenarios.json."""

import json
from collections import Counter

import jsonschema
import pytest

from openalgoritme import specs
from openalgoritme.paths import SCHEMA_DIR

# A small feature in the style of the RvIG specifications. Names and facts are made up for this test.
FEATURE = """\
# language: nl
Functionaliteit: Voorbeeldfunctionaliteit
  Een omschrijving over
  twee regels.

  Achtergrond:
    Gegeven de persoon 'Pien' met burgerservicenummer '000000012'
    * is meerderjarig
    En de persoon 'Sem' met burgerservicenummer '000000024'
    * heeft 'Pien' als ouder 1

  @to-do
  Regel: Als er één ouder is, dan heeft die ouder het gezag
    Opmerking: alleen voor deze test.

    Voorbeeld: één ouder
      Gegeven 'Sem' is 3 jaar geleden geboren
      En voor 'Sem' is een gerechtelijke uitspraak over het gezag gedaan met de volgende gegevens
        | indicatie gezag (32.10) |
        | 1                       |
      Als 'gezag' wordt gevraagd van 'Sem'
      Dan is het gezag over 'Sem' eenhoofdig ouderlijk gezag met ouder 'Pien'

  Regel: Uitkomsten met een toelichting

    Abstract Scenario: <situatie>
      Gegeven 'Pien' <feit>
      Als 'gezag' wordt gevraagd van 'Sem'
      Dan is het gezag over 'Sem' tijdelijk geen gezag met de toelichting '<toelichting>'

      Voorbeelden:
        | situatie   | feit         | toelichting                     |
        | overleden  | is overleden | Tijdelijk geen gezag: overleden |
        | curatele   | staat onder curatele | Tijdelijk geen gezag: curatele |

    Scenario: vanuit de ouder
      Als 'gezag' wordt gevraagd van 'Pien'
      Dan heeft 'Pien' de volgende gezagsrelaties
      * is het gezag over 'Sem' eenhoofdig ouderlijk gezag met ouder 'Pien'
      En is het gezag in onderzoek
"""


@pytest.fixture(scope="module")
def cases():
    return specs.cases_from_feature(specs.parse_feature(FEATURE, "voorbeeld.feature"))


def test_parser_reads_feature_rules_and_background():
    feature = specs.parse_feature(FEATURE, "voorbeeld.feature")
    assert feature.title == "Voorbeeldfunctionaliteit"
    assert feature.description == ["Een omschrijving over", "twee regels."]
    assert [s.text for s in feature.background][:2] == ["de persoon 'Pien' met burgerservicenummer '000000012'",
                                                        "is meerderjarig"]
    titled = [r for r in feature.rules if r.title]
    assert titled[0].tags == ["to-do"]
    assert titled[0].description == ["Opmerking: alleen voor deze test."]


def test_cases_have_ids_tags_and_background(cases):
    assert [c["id"] for c in cases] == ["voorbeeld:16", "voorbeeld:26:1", "voorbeeld:26:2", "voorbeeld:36"]
    first = cases[0]
    assert first["tags"] == ["to-do"]
    assert first["rule"] == "Als er één ouder is, dan heeft die ouder het gezag"
    assert first["persons"] == [{"name": "Pien", "bsn": "000000012"}, {"name": "Sem", "bsn": "000000024"}]
    assert first["when"] == {"field": "gezag", "person": "Sem"}


def test_star_steps_get_the_last_person_as_subject(cases):
    given = cases[0]["given"]
    assert given[1] == {"keyword": "*", "text": "is meerderjarig", "line": 8, "subject": "Pien"}
    assert given[3]["subject"] == "Sem"
    assert "subject" not in given[4]  # "'Sem' is 3 jaar geleden geboren" names its own subject


def test_step_tables_become_rows(cases):
    step = cases[0]["given"][5]
    assert step["table"] == [{"indicatie gezag (32.10)": "1"}]


def test_abstract_scenarios_are_expanded(cases):
    second, third = cases[1], cases[2]
    assert second["title"] == "overleden"
    assert second["given"][-1]["text"] == "'Pien' is overleden"
    assert second["outcomes"][0]["explanation"] == "Tijdelijk geen gezag: overleden"
    assert third["outcomes"][0]["explanation"] == "Tijdelijk geen gezag: curatele"
    assert "<" not in json.dumps(cases)


def test_relations_of_an_adult(cases):
    case = cases[3]
    assert case["perspective"] == "meerderjarige"
    outcome = case["outcomes"][0]
    assert (outcome["about"], outcome["type"], outcome["parents"]) == ("Sem", "eenhoofdig_ouderlijk_gezag", ["Pien"])
    assert outcome["under_investigation"] is True


@pytest.mark.parametrize("rest, expected", [
    ("gezamenlijk ouderlijk gezag met ouder 'A' en ouder 'B'", ("gezamenlijk_ouderlijk_gezag", ["A", "B"], [], False)),
    ("eenhoofdig ouderlijk gezag met ouder 'A'", ("eenhoofdig_ouderlijk_gezag", ["A"], [], False)),
    ("gezamenlijk gezag met ouder 'A' en derde 'C'", ("gezamenlijk_gezag", ["A"], ["C"], False)),
    ("gezamenlijk gezag met ouder 'A' en een onbekende derde", ("gezamenlijk_gezag", ["A"], [], True)),
    ("voogdij", ("voogdij", [], [], False)),
    ("voogdij met derde 'C'", ("voogdij", [], ["C"], False)),
    ("tijdelijk geen gezag met de toelichting 'x'", ("tijdelijk_geen_gezag", [], [], False)),
    ("niet te bepalen met de toelichting 'x'", ("niet_te_bepalen", [], [], False)),
    ("iets nieuws", ("onbekend", [], [], False)),
])
def test_parse_outcome(rest, expected):
    outcome = specs.parse_outcome("K", rest, f"is het gezag over 'K' {rest}")
    assert (outcome["type"], outcome["parents"], outcome["third_parties"], outcome["unknown_third_party"]) == expected


def test_readable_sentences():
    assert specs.readable({"text": "de persoon 'Pien' met burgerservicenummer '000000012'"}) is None
    assert specs.readable({"text": "is meerderjarig", "subject": "Pien"}) == "Pien is meerderjarig"
    assert specs.readable({"text": "'Sem' is 3 jaar geleden geboren"}) == "Sem is 3 jaar geleden geboren"
    step = {"text": "voor 'Sem' is een uitspraak gedaan met de volgende gegevens", "table": [{"indicatie": "1"}]}
    assert specs.readable(step) == "Voor Sem is een uitspraak gedaan (indicatie: 1)"


# ---- the committed file ----------------------------------------------------------------------


def test_committed_file_matches_schema(data):
    schema = json.loads((SCHEMA_DIR / "scenarios.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(data, schema)


def test_committed_file_is_pinned_and_attributed(data):
    assert data["source"]["repository"] == specs.REPOSITORY
    assert len(data["source"]["commit"]) == 40
    assert data["source"]["licence"] == "EUPL-1.2"
    assert data["source"]["copyright"] == specs.COPYRIGHT
    assert data["modification"]["date"]


def test_committed_ids_are_unique(data):
    counts = Counter(case["id"] for case in data["scenarios"])
    assert [i for i, n in counts.items() if n > 1] == []


def test_every_outcome_is_parsed(data):
    unknown = [c["id"] for c in data["scenarios"] for o in c["outcomes"] if o["type"] == "onbekend"]
    assert unknown == []


def test_only_fictional_test_numbers(data):
    """RvIG uses test numbers such as 000000012. Anything else would need a closer look."""
    bsns = {p["bsn"] for c in data["scenarios"] for p in c["persons"] if p["bsn"]}
    assert bsns and all(b.startswith("0000000") for b in bsns)


def test_file_is_written_the_way_the_builder_writes_it(data):
    from openalgoritme.paths import SCENARIOS_FILE

    assert specs.dumps(data) == SCENARIOS_FILE.read_text(encoding="utf-8")
