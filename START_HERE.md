# Start Here (Hackathon Teams)

If you are starting the challenge now, follow this order.

## 1) Understand the scope (10 min)

- Read [CHALLENGE.md](CHALLENGE.md).
- Skim [docs/judging-criteria.md](docs/judging-criteria.md). Every Must is blocking, and one of them is about the resident understanding the text.
- Read [docs/use-case-gezag.md](docs/use-case-gezag.md): what gezag is, which outcomes the algorithm gives, and the decision this starter uses (a travel document for a minor).

## 2) Pick your layer (10 min)

All teams need at least one concrete decision with an understandable motivering. Choose where you go deepest; [docs/layers.md](docs/layers.md) says what the starter gives you per layer.

- **Laag 1, motivering:** start with `python -m openalgoritme.explain`, the templates in [data/uitleg/gezag.yaml](data/uitleg/gezag.yaml) and the decision in [data/besluiten/](data/besluiten/).
- **Laag 2, audit trail and quality check:** start with `python -m openalgoritme.check` and [docs/registration-check.md](docs/registration-check.md).
- **Laag 3, service:** start with [docs/legal-context.md](docs/legal-context.md) (MijnOverheid, objection, chatbot answers) and [docs/integrations/greenpt-api.md](docs/integrations/greenpt-api.md).

Make sure your team has someone who writes for residents and someone who thinks about the legal side.

## 3) Set up (10 min)

Fork this repository, then:

```bash
cd tooling
python -m venv .venv
source .venv/bin/activate        # Windows: .\.venv\Scripts\Activate.ps1
pip install -e .[dev]
pytest -v
```

Using another language? Fine. Read [data/rvig-gezag/scenarios.json](data/rvig-gezag/) and [data/algoritmeregister/gezag-61781447.json](data/algoritmeregister/) directly, and make sure your rules and templates are testable.

## 4) Make one explanation work end-to-end (first hours)

- Read one test case in plain Dutch: `python -m openalgoritme.specs show twee-ouders-met-relatie:19`
- Generate its motivering: `python -m openalgoritme.explain`. Read it as a parent would. What is unclear?
- Try a hard case: `python -m openalgoritme.explain --scenario gezag-meerderjarige/meerderjarige-rni:18` (gezag cannot be determined). Words such as *RNI* and *ouder 1* are BRP jargon. What does a resident need here?
- Change one template in [data/uitleg/gezag.yaml](data/uitleg/gezag.yaml) and run `pytest`. The test on the worked examples notices; regenerate them with `python -m openalgoritme.explain --write-examples` if you meant the change.

## 5) Scale out and demo

- Does your explanation work for every outcome type? `python -m openalgoritme.specs list --outcome tijdelijk_geen_gezag` (types are listed in [data/rvig-gezag/README.md](data/rvig-gezag/README.md)).
- Laag 2: `python -m openalgoritme.check --melding` drafts a message to the owner. Try another registration: `python -m openalgoritme.register fetch <LARS> --out other.json`, then `python -m openalgoritme.check --snapshot other.json`.
- Test your text with someone who does not know the topic, and show what changed.

## 6) Keep your submission valid

- Only fictional persons: the test cases, or your own made-up cases. No real BRP data, no real BSN.
- The gezag outcome and the facts come from the rules and the data, not from a prompt. If an LLM writes text, say where, and keep a person or a test between the model and the resident.
- Templates and rules are explicit and testable; put your work in `submissions/<team-name>/`.
- Do not send generated messages to real algorithm owners or residents.
- One Pull Request per team, using the [PR template](.github/pull_request_template.md).
