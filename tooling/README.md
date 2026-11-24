# Starter tooling (`openalgoritme`)

Optional Python tooling for the Open Algoritme challenge. Python 3.10+, one runtime dependency (PyYAML). Everything it reads is plain JSON or YAML in [`../data/`](../data/), so teams working in another language can skip it and read the files directly.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .\.venv\Scripts\Activate.ps1
pip install -e .[dev]
pytest -v
ruff check .
```

## Modules

| Module | What it does | Layer |
|---|---|---|
| `specs` | Converts RvIG's Gherkin specifications (Dutch) into [`data/rvig-gezag/scenarios.json`](../data/rvig-gezag/); lists and shows test cases in plain Dutch | Data |
| `register` | Reads a registration from the Algoritmeregister, from the snapshot or live from the public API; turns its HTML into text | Data |
| `check` | Asks eleven questions a motivering needs of a registration; drafts a message to the owner | Laag 2 |
| `explain` | Builds a motivering for one case from the test case, the registration, the templates and a decision, with an audit trail | Laag 1 |

## Commands

```bash
# test cases
python -m openalgoritme.specs list                                  # all 294
python -m openalgoritme.specs list --outcome niet_te_bepalen
python -m openalgoritme.specs show twee-ouders-met-relatie:19
python -m openalgoritme.specs build --source ../../brp-api-gezag    # regenerate from a clone of RvIG's repo
python -m openalgoritme.specs build --source ../../brp-api-gezag --check

# the registration
python -m openalgoritme.register show
python -m openalgoritme.register show --field human_intervention
python -m openalgoritme.register fetch 61781447 --out ../data/algoritmeregister/gezag-61781447.json

# Laag 2
python -m openalgoritme.check
python -m openalgoritme.check --as-of 2026-12-09 --format json
python -m openalgoritme.check --melding --bevestig R06

# Laag 1
python -m openalgoritme.explain
python -m openalgoritme.explain --scenario gezag-meerderjarige/meerderjarige-rni:18
python -m openalgoritme.explain --scenario gezag-meerderjarige/gezag-meerderjarige-over-kinderen:30 --besluit geen
python -m openalgoritme.explain --format json --out motivering.json
python -m openalgoritme.explain --write-examples                   # regenerate data/rvig-gezag/examples/
```

`explain` with the default decision (a travel document for a minor) needs a case that asks about a child. For cases that ask about an adult, use `--besluit geen`.

## Using it as a library

```python
from openalgoritme import specs, explain, check
from openalgoritme.register import load_snapshot
from openalgoritme.paths import UITLEG_FILE

data = specs.load()
case = specs.scenario_by_id(data, "twee-ouders-met-relatie:19")
snap = load_snapshot()
doc = explain.explain(case, data, snap, explain.load_yaml(UITLEG_FILE),
                      explain.load_besluit("reisdocument-minderjarige"))
print(explain.to_markdown(doc))
```

`explain.explain` returns a plain dict (title, sections, audit), so a web front end can render it any way it likes.

## Tests

The tests check the parser on a small made-up feature, the committed test cases against their JSON Schema, the registration snapshot against its hash, the findings of the registration check, that every outcome type has a template, that every case can be explained, and that the worked examples are up to date. CI also rebuilds `scenarios.json` from the pinned RvIG commit.

## Design choices

- **No language model.** The same input always gives the same text. That makes the starter testable; it is not a rule for teams.
- **Templates as data.** The texts residents read live in YAML, not in code, so a writer can change them without touching Python.
- **Pinned sources.** The rules are linked at a fixed commit and the registration is a dated snapshot with a hash, so the audit trail points to exactly what was used.
