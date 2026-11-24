"""The registration snapshot and the Laag 2 registration check."""

import json
from datetime import date

import jsonschema
import pytest

from openalgoritme import check
from openalgoritme.paths import SCHEMA_DIR
from openalgoritme.register import field_text, html_to_text, page_url, record_hash

SNAPSHOT_DAY = date(2026, 11, 24)


def test_snapshot_matches_schema(snap):
    schema = json.loads((SCHEMA_DIR / "registration-snapshot.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(snap, schema)


def test_snapshot_record_is_unmodified(snap):
    """The hash was taken from the API response when the snapshot was made. Edit nothing by hand."""
    assert record_hash(snap["record"]) == snap["sha256"]


def test_page_url_is_derived_from_the_record(snap):
    assert page_url(snap["record"]) == snap["page"]


@pytest.mark.parametrize("html, text", [
    ("<p>Een</p><p>Twee</p>", "Een\nTwee"),
    ("<ul><li>a;</li><li>b.</li></ul>", "- a;\n- b."),
    ("<p>B&amp;W  samen</p>", "B&W samen"),
    ("<div><p>x</p><p><br></p><p>y</p></div>", "x\n\ny"),
    (None, ""),
])
def test_html_to_text(html, text):
    assert html_to_text(html) == text


def test_grouping_fields_as_text(snap):
    assert "Logisch Ontwerp BRP: https://www.rvig.nl/lo-brp" in field_text(snap["record"], "source_data_grouping")


def statuses(findings):
    return {f.check.id: f.status for f in findings}


def test_findings_for_the_gezag_registration(snap):
    result = statuses(check.run_checks(snap["record"], SNAPSHOT_DAY))
    assert result == {
        "R01": "ok", "R02": "ok", "R03": "ok", "R04": "ok", "R05": "ok",
        "R06": "handmatig",   # a person has to read 'Doel en impact'; see docs/registration-check.md
        "R07": "ok",
        "R08": "ontbreekt",   # no route for residents
        "R09": "aandacht",    # DPIA only on request
        "R10": "aandacht",    # last changed 21 October 2024
        "R11": "ok",
    }


def test_up_to_date_depends_on_the_day(snap):
    findings = statuses(check.run_checks(snap["record"], date(2025, 6, 1)))
    assert findings["R10"] == "ok"


def test_a_person_can_confirm_a_manual_check(snap):
    findings = check.run_checks(snap["record"], SNAPSHOT_DAY, confirmed=("R06",))
    r06 = next(f for f in findings if f.check.id == "R06")
    assert r06.status == "ontbreekt"


def test_empty_registration_does_not_crash():
    findings = check.run_checks({"name": "Leeg", "organization": "X", "lars": "1"}, SNAPSHOT_DAY)
    assert {f.status for f in findings} <= {"ontbreekt", "handmatig"}


def test_melding_is_a_draft_to_the_contact(snap):
    text = check.melding(snap, check.run_checks(snap["record"], SNAPSHOT_DAY))
    assert text.startswith("Aan: Info@rvig.nl")
    assert "CONCEPT" in text and "Er is niets verstuurd" in text
    # unconfirmed manual checks are listed for a person, not put in the message itself
    body, _, unread = text.partition("---")
    assert "R06" not in body and "R06" in unread


def test_cli_runs(capsys):
    assert check.main(["--as-of", "2026-11-24"]) == 0
    assert "Samenvatting: 7 ok, 1 ontbreekt, 2 aandacht, 1 handmatig" in capsys.readouterr().out
    assert check.main(["--as-of", "2026-11-24", "--strict"]) == 1
