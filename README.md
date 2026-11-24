# OneGov #3 | Open Algoritme

> *From algorithm registration to an explanation residents understand.*

This repository hosts the challenge brief, supporting documents, starter data and optional tooling for challenge 4 of **OneGov #3**, part of the OneGov Hackathon Series hosted by [GovTech NL](https://govtechnl.nl). The question was put forward by Olaf Schoelink.

- **Theme:** Digital autonomy and sovereignty
- **Date:** 9-10 December 2026
- **Location:** The Hague Tech, Den Haag
- **Challenge owner:** Olaf Schoelink
- **Tech partner:** [GreenPT](https://greenpt.nl/)
- **Contact:** [hack@govtechnl.nl](mailto:hack@govtechnl.nl)

## The challenge in one paragraph

Algorithms increasingly contribute to decisions about residents, but the *motivering* (the statement of reasons in a decision) rarely says what role they played. **How do we make decisions to which an algorithm or machine learning contributed so explainable that residents understand how the decision came about, and can judge for themselves whether to object?** Teams work with a real government algorithm with public source code: the derivation of parental authority (*gezag*) in the BRP API of the Rijksdienst voor Identiteitsgegevens (RvIG).

The full brief is in [CHALLENGE.md](CHALLENGE.md). New teams start with [START_HERE.md](START_HERE.md).

## What's in here

| Path | Purpose | Status |
|---|---|---|
| [CHALLENGE.md](CHALLENGE.md) | Full challenge brief (English working translation of the Dutch original) | Available |
| [START_HERE.md](START_HERE.md) | Step-by-step start for teams | Available |
| [docs/](docs/) | The use case, the three layers, the registration check, legal context, judging criteria, glossary | Available |
| [data/rvig-gezag/scenarios.json](data/rvig-gezag/) | 294 test cases from RvIG's rule specifications as JSON: facts, rule, outcome. Fictional persons | Available (EUPL-1.2) |
| [data/rvig-gezag/examples/](data/rvig-gezag/examples/) | Two worked motiveringen made by the starter tooling | Available |
| [data/algoritmeregister/](data/algoritmeregister/) | The registration of the gezag algorithm (LARS 61781447), unmodified, with provenance | Snapshot of 24 November 2026 |
| [data/uitleg/gezag.yaml](data/uitleg/gezag.yaml) | Plain-language templates per outcome type | First draft, improve it |
| [data/besluiten/](data/besluiten/) | A decision in which gezag counts: a travel document for a minor | Available (fictional procedure) |
| [data/schemas/](data/schemas/) | JSON Schemas for the test cases and the registration snapshot | Available |
| [tooling/](tooling/) | Optional Python starter: spec parser, register reader, registration check (Laag 2), explanation builder (Laag 1) | Available |
| [submissions/](submissions/) | Where your team's work lands in your Pull Request | Empty |
| [resources/](resources/) | Source material as delivered by the challenge owner | Follows |

**The algorithm is real, the persons are not.** Every person in this repository comes from RvIG's test cases and uses a test number instead of a real citizen service number (BSN). No real personal data passes through the challenge.

## Quick start

```bash
cd tooling
python -m venv .venv
source .venv/bin/activate        # Windows: .\.venv\Scripts\Activate.ps1
pip install -e .[dev]
pytest -v

# One test case in plain Dutch: the facts, the rule, the outcome
python -m openalgoritme.specs show twee-ouders-met-relatie:19

# Laag 1: a motivering for that case, for an application for a travel document
python -m openalgoritme.explain

# A harder case: gezag cannot be determined
python -m openalgoritme.explain --scenario gezag-meerderjarige/meerderjarige-rni:18

# Laag 2: what does the registration miss for a motivering? And a draft message to the owner
python -m openalgoritme.check
python -m openalgoritme.check --melding
```

The tooling is optional. **Teams are free to choose any language and approach.** The test cases are plain JSON, so any language can read them.

## Important to know

- You do not need to run RvIG's Java module. The rules are readable specifications, and every example is in [data/rvig-gezag/scenarios.json](data/rvig-gezag/).
- For the jury, the explanation counts, not the model. Test your text with someone who does not know the topic.
- Use an LLM where it helps, for example to rephrase or in a chatbot, but the outcome of the gezag determination and the facts come from the rules and the data, never from a prompt.
- Gezag touches sensitive family situations, such as a divorce or a court ruling. Be careful in examples, pitches and demos, also with fictional persons.
- The texts the starter produces are a first draft. They have not been tested with residents.

## Licensing

See [CONTRIBUTING.md](CONTRIBUTING.md#licensing-of-contributions) for the canonical rule. In short:

- This **starter repo** ships under **Apache-2.0** (code, see [LICENSE](LICENSE)) and **CC BY 4.0** (data, docs, challenge text, see [LICENSE-DATA](LICENSE-DATA)), with two exceptions:
  - [data/rvig-gezag/](data/rvig-gezag/) is derived from RvIG's specifications (Copyright © RvIG 2022) and is licensed under the **EUPL-1.2**;
  - [data/algoritmeregister/](data/algoritmeregister/) holds text from the Algoritmeregister, reused under the [register's terms](https://algoritmes.overheid.nl/nl/footer/copyright).
- **Team submissions** must be open source under an **OSI-approved licence** for code (Apache-2.0, MIT, EUPL-1.2, ...) and an open licence (CC BY 4.0 recommended, CC0 accepted) for texts, templates and documentation. Material you take from RvIG keeps the EUPL-1.2.

## Contributing

Issues and pull requests are welcome, see [CONTRIBUTING.md](CONTRIBUTING.md). During the hackathon the rule is **one PR per team**.

## Submission

Submissions go through **Alkemio**. Each team submits a link to its Pull Request on this repo, a short explanation of what it built, for whom and why, and the pitch deck. See [CHALLENGE.md](CHALLENGE.md#submission).

## Disclaimer

The prototypes and designs produced during this hackathon are published as open source. The challenge is an innovation exercise: there are no commitments about further development or adoption in policy, and a prototype is not legal advice. All persons in the data are fictional. The observations about the gezag registration in [docs/registration-check.md](docs/registration-check.md) describe what a motivering needs; they are not a judgement of RvIG or of the Algoritmeregister.
