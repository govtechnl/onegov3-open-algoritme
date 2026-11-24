"""The Laag 1 explanation: templates, decision context and the worked examples."""

import pytest

from openalgoritme import explain
from openalgoritme.paths import EXAMPLES_DIR
from openalgoritme.specs import scenario_by_id


def test_every_outcome_type_has_a_template(data, uitleg):
    types = {o["type"] for c in data["scenarios"] for o in c["outcomes"]}
    assert types <= set(uitleg["uitkomsten"])


def test_every_outcome_for_a_minor_has_a_consequence(data, besluit):
    types = {c["outcomes"][0]["type"] for c in data["scenarios"] if c["perspective"] == "minderjarige"}
    assert types <= set(besluit["gevolg"])


def test_default_example(data, snap, uitleg, besluit):
    doc = explain.explain(scenario_by_id(data, explain.DEFAULT_SCENARIO), data, snap, uitleg, besluit)
    text = explain.to_markdown(doc)
    assert "Gerda en Aart hebben samen het gezag over Bert." in text
    assert "Wij hebben daarom toestemming nodig van Gerda en Aart." in text
    assert data["source"]["commit"] in text  # the rule is linked at the pinned commit
    assert "binnen zes weken bezwaar" in text
    assert "ontbreekt: R08" in doc["audit"]["registratiecheck"]
    assert "'" not in "".join(doc["sections"][2]["items"])  # names without Gherkin quotes


@pytest.mark.parametrize("case_id, name", explain.EXAMPLES.items())
def test_worked_examples_are_up_to_date(case_id, name):
    assert (EXAMPLES_DIR / name).read_text(encoding="utf-8") == explain.example_markdown(case_id), (
        "regenerate with: python -m openalgoritme.explain --write-examples")


def test_every_case_can_be_explained(data, snap, uitleg, besluit):
    for case in data["scenarios"]:
        chosen = besluit if case["perspective"] == "minderjarige" else None
        text = explain.to_markdown(explain.explain(case, data, snap, uitleg, chosen))
        assert "{" not in text and "}" not in text, case["id"]


def test_decision_needs_the_right_perspective(data, snap, uitleg, besluit):
    adult = next(c for c in data["scenarios"] if c["perspective"] == "meerderjarige")
    with pytest.raises(ValueError):
        explain.explain(adult, data, snap, uitleg, besluit)


def test_holders():
    base = {"parents": [], "third_parties": [], "unknown_third_party": False, "type": "gezamenlijk_gezag"}
    assert explain.holders({**base, "parents": ["A"], "third_parties": ["C"]}) == "A en C"
    assert explain.holders({**base, "parents": ["A"], "unknown_third_party": True}) == (
        "A en iemand van wie de naam niet bekend is")
    assert explain.holders({**base, "type": "voogdij"}) == "een voogd"
    assert explain.join_names(["A", "B", "C"]) == "A, B en C"


def test_cli_rejects_unknown_scenario(capsys):
    with pytest.raises(SystemExit) as exit_info:
        explain.main(["--scenario", "bestaat-niet:1"])
    assert exit_info.value.code == 2
