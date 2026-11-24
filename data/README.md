# Data

Everything a team needs to explain one real algorithm, without real personal data.

| Folder | What | Source | Licence |
|---|---|---|---|
| [rvig-gezag/](rvig-gezag/) | 294 test cases of the gezag algorithm as JSON, plus two worked motiveringen | RvIG's rule specifications, pinned commit | EUPL-1.2 |
| [algoritmeregister/](algoritmeregister/) | The registration of the gezag algorithm (LARS 61781447), unmodified | Algoritmeregister API, 24 November 2026 | Register's reuse terms |
| [uitleg/](uitleg/) | Plain-language templates per outcome type (Laag 1) | Written for this repo | CC BY 4.0 |
| [besluiten/](besluiten/) | Decisions in which gezag counts: what the outcome means for the application | Written for this repo, legal facts sourced in the file | CC BY 4.0 |
| [schemas/](schemas/) | JSON Schemas for the test cases and the registration snapshot | Written for this repo | CC BY 4.0 |

## How the pieces fit

```
scenarios.json  ──  facts, rule, outcome of one fictional case ─┐
gezag-61781447.json ── who runs the algorithm, legal basis, gaps ├─> motivering (Laag 1)
uitleg/gezag.yaml ── plain Dutch per outcome type ───────────────┤      + audit trail (Laag 2)
besluiten/*.yaml ── why gezag matters for this decision ─────────┘
```

`python -m openalgoritme.explain` in [tooling/](../tooling/) puts them together; the results are in [rvig-gezag/examples/](rvig-gezag/examples/).

## Adding a decision

Copy [besluiten/reisdocument-minderjarige.yaml](besluiten/reisdocument-minderjarige.yaml), give it a new `id`, and fill in what the outcome means for that decision per outcome type (`gevolg`). Source every legal fact in the file. Then:

```bash
python -m openalgoritme.explain --besluit <id>
```

## What is real and what is not

- **Real:** the algorithm, its rules, its registration, the laws and procedures linked in the files.
- **Fictional:** every person (RvIG's test persons with test numbers), and the municipality's procedure in `besluiten/`.
