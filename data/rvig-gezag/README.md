# Gezag test cases (RvIG)

[scenarios.json](scenarios.json) holds the examples from RvIG's rule specifications for the gezag algorithm as plain JSON: for each case the facts, the rule that applies and the expected outcome. Use them as test cases, as input for an explanation, or to see which situations the algorithm distinguishes.

| | |
|---|---|
| Source | [BRP-API/brp-api-gezag](https://github.com/BRP-API/brp-api-gezag), folder `features/specs` (top level, `gezag-minderjarige/`, `gezag-meerderjarige/`) |
| Commit | [`1d736060ff14bb912c5e970ef6de4f07db2c1597`](https://github.com/BRP-API/brp-api-gezag/tree/1d736060ff14bb912c5e970ef6de4f07db2c1597/features/specs) (19 November 2026) |
| Not included | `S-en-T-test/` and `S-en-T-test-omgekeerd-ouders/`, RvIG's integration tests |
| Contents | 24 feature files, 294 test cases, 307 outcomes |
| Converted | 24 November 2026, with [`tooling/openalgoritme/specs.py`](../../tooling/openalgoritme/specs.py) |

## Licence and attribution

The specifications are Copyright © RvIG 2022 and licensed under the [European Union Public Licence v. 1.2](LICENSE-EUPL-1.2.txt). Everything in this folder is derived from them and is therefore also licensed under the **EUPL-1.2**. That includes the worked examples in [examples/](examples/), which quote names, facts and rule texts from the specifications.

**Modification notice.** On 24 November 2026 the Gherkin feature files were converted to JSON. Step texts, rule texts and outcomes are copied unchanged. Added: an id per case, the person each `*` step is about, parsed outcomes with this repository's own type names, backgrounds repeated in every case, and abstract scenarios expanded per example row. The same notice is in the `modification` block of the file.

## Structure

```json
{
  "source": {"repository": "...", "commit": "...", "licence": "EUPL-1.2", "copyright": "Copyright © RvIG 2022"},
  "modification": {"date": "2026-11-24", "description": "..."},
  "features": [{"file": "...", "title": "...", "description": "...", "rules": ["..."]}],
  "scenarios": [
    {
      "id": "twee-ouders-met-relatie:19",
      "source": {"file": "features/specs/twee-ouders-met-relatie.feature", "line": 19},
      "feature": "Twee ouders met relatie",
      "rule": "Als de ouders na de geboorte van minderjarige ...",
      "title": "Beide ouders zijn gehuwd voor geboorte van het kind en zijn dat nog steeds",
      "tags": [],
      "persons": [{"name": "Gerda", "bsn": "000000012"}],
      "given": [
        {"keyword": "*", "text": "is meerderjarig", "line": 10, "subject": "Gerda"},
        {"keyword": "En", "text": "'Gerda' en 'Aart' zijn 8 jaar geleden gehuwd", "line": 21}
      ],
      "when": {"field": "gezag", "person": "Bert"},
      "perspective": "minderjarige",
      "outcomes": [
        {"about": "Bert", "type": "gezamenlijk_ouderlijk_gezag", "parents": ["Gerda", "Aart"],
         "third_parties": [], "unknown_third_party": false, "explanation": null,
         "under_investigation": false, "text": "is het gezag over 'Bert' gezamenlijk ouderlijk gezag ..."}
      ]
    }
  ]
}
```

- **id** is `<file>:<line>` of the scenario in the pinned commit, with `:<n>` for the n-th example row of an abstract scenario. Line numbers change when RvIG edits a file; the commit keeps them stable.
- **given** holds every step before `Als`, including the background. `subject` is set when the sentence has no subject of its own (`* is meerderjarig` after `de persoon 'Gerda'`). Steps with a data table have `table` as a list of rows; the headers are BRP field names with their code, for example `indicatie gezag (32.10)`.
- **perspective** is `minderjarige` when the case asks for the gezag over a child, `meerderjarige` when it asks over which children an adult has gezag (`Dan heeft 'X' de volgende gezagsrelaties`).
- **outcomes** has one entry per outcome. `explanation` is the *toelichting* the algorithm gives with some outcomes. `under_investigation` is true when the case expects `is het gezag in onderzoek`.
- **schema:** [../schemas/scenarios.schema.json](../schemas/scenarios.schema.json).

## Outcome types

The type names are this repository's own labels. The text of every outcome is kept in `text`.

| type | Dutch term in the specifications | outcomes |
|---|---|---:|
| `gezamenlijk_ouderlijk_gezag` | gezamenlijk ouderlijk gezag: both parents | 126 |
| `eenhoofdig_ouderlijk_gezag` | eenhoofdig ouderlijk gezag: one parent | 61 |
| `voogdij` | voogdij: a guardian who is not a parent | 42 |
| `niet_te_bepalen` | gezag niet te bepalen, with a toelichting | 25 |
| `gezamenlijk_gezag` | gezamenlijk gezag: a parent and someone who is not a parent | 22 |
| `geen_gezag` | an adult has no gezag over a child | 15 |
| `tijdelijk_geen_gezag` | tijdelijk geen gezag, with a toelichting | 12 |
| `geen_gezaghouder` | no gezag is given, for example because the person is an adult or has died | 4 |

## Tags

RvIG tags some scenarios. 54 cases carry `skip-verify`: RvIG's test configuration (`cucumber.js` at the pinned commit) leaves them out of its automated runs. 46 carry `to-do`. Treat tagged cases as described intent rather than verified behaviour of the API, and prefer untagged cases for demos.

## Browse and rebuild

```bash
cd tooling
python -m openalgoritme.specs list --outcome niet_te_bepalen
python -m openalgoritme.specs show gezag-meerderjarige/meerderjarige-rni:18

# rebuild from a clone of RvIG's repository at the pinned commit (CI does this on every push)
python -m openalgoritme.specs build --source ../../brp-api-gezag --check
```

## Worked examples

[examples/](examples/) has two motiveringen for the application of a travel document for a minor, made with `python -m openalgoritme.explain --write-examples`:

- [motivering-gezamenlijk-ouderlijk-gezag.md](examples/motivering-gezamenlijk-ouderlijk-gezag.md): case `twee-ouders-met-relatie:19`
- [motivering-gezag-niet-te-bepalen.md](examples/motivering-gezag-niet-te-bepalen.md): case `gezag-meerderjarige/meerderjarige-rni:18`

They are a starting point, not a good example: read them as a resident would, and improve on them.
