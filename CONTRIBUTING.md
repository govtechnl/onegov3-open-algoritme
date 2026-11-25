# Contributing

Thanks for your interest in the **OneGov #3 | Open Algoritme** challenge repository.

This repo is maintained by **GovTechNL** together with the challenge owners from **Minbzk** and **ECP** for the hackathon on **9-10 December 2026** at The Hague Tech. Contributions are welcome from organisers, mentors, participating teams and the wider community.

## Two contribution flows

### 1. Hackathon teams: build in your fork, submit on Alkemio

This is the primary flow during the hackathon.

1. **Fork** this repository to your team's GitHub account (or start your own repository) and clone it.
2. Build your prototype in your fork. Put everything team-specific under `submissions/<team-name>/` (see [submissions/README.md](submissions/README.md)).
3. Keep your repository **public**, under the licences below.
4. **Submit on [Alkemio](https://alkem.io/onegov-hackathon) before Thursday 10 December, 14:00**, with a link to your repository. See [EVENT.md](EVENT.md#submission).
5. A Pull Request into this repository is welcome but optional. If you open one, use the [pull request template](.github/pull_request_template.md).

### 2. Improving the starter repo

- **Improve the templates** in [`data/uitleg/`](data/uitleg/) and [`data/besluiten/`](data/besluiten/), preferably after testing them with residents.
- **Add a decision** in which gezag counts, as a new file in [`data/besluiten/`](data/besluiten/), with sources.
- **Sharpen documentation** under [`docs/`](docs/).
- **Improve the tooling** under [`tooling/`](tooling/).
- **Report issues** using the [issue templates](.github/ISSUE_TEMPLATE/).

## Ground rules

1. **Fictional persons only.** Use the test cases in `data/rvig-gezag/` or your own made-up cases. Never commit real personal data or a real BSN, also not in issues, screenshots or demo videos.
2. **Traceable explanations.** Every sentence a resident reads can be traced to a test case, a registration, a template or a decision file. Keep the audit trail.
3. **Explicit rules.** Who has gezag follows from RvIG's rules. A language model may help to write or rephrase, but it does not decide the outcome and does not add facts.
4. **Careful with the subject.** Gezag touches divorce, death, court rulings and custody. Choose examples with care, also in pitches.
5. **No verdicts on real organisations.** Findings about a registration are about what a motivering needs. They are not a judgement of the organisation that registered the algorithm.
6. **Nothing is sent.** Generated messages to algorithm owners or residents stay drafts. Do not send them to real addresses.
7. **Open source.** All submitted code and texts are released under the licences below.
8. **Language.** Documentation in this repo is primarily English. Texts for residents and messages to owners are in Dutch, because that is who reads them.

## Development workflow

```bash
cd tooling
python -m venv .venv
source .venv/bin/activate        # Windows: .\.venv\Scripts\Activate.ps1
pip install -e .[dev]
ruff check .
pytest -v
```

CI ([`.github/workflows/validate.yml`](.github/workflows/validate.yml)) runs lint and tests, rebuilds the test cases from the pinned RvIG commit to check that `data/rvig-gezag/scenarios.json` is up to date, and smoke-tests the command line tools. Make sure the tests pass locally before opening a PR.

If you change a template or a decision file, regenerate the worked examples with `python -m openalgoritme.explain --write-examples`.

## Pull requests

- Keep PRs focused, one logical change per PR (a team's hackathon PR is the exception).
- Update the README, data and docs together when behaviour changes.
- Reference the related issue if there is one.

## Code of Conduct

By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md) (Contributor Covenant 2.1), including the section on **personal data, sensitive topics and registrations**.

## Licensing of contributions

This is the **canonical licensing rule** for the repository. All other documents refer back here.

- This **starter repository** is licensed under **Apache-2.0** for code (see [LICENSE](LICENSE)) and **CC BY 4.0** for data, documentation and challenge text (see [LICENSE-DATA](LICENSE-DATA)), with two exceptions:
  - **`data/rvig-gezag/`** is derived from the specifications in [BRP-API/brp-api-gezag](https://github.com/BRP-API/brp-api-gezag) (Copyright © RvIG 2022) and is licensed under the **EUPL-1.2**, see [data/rvig-gezag/README.md](data/rvig-gezag/README.md).
  - **`data/algoritmeregister/`** holds text from the Algoritmeregister, reused under the [register's terms](https://algoritmes.overheid.nl/nl/footer/copyright).
- **Hackathon team submissions** must be open source under an **OSI-approved licence** for code (Apache-2.0, MIT, EUPL-1.2 or another OSI-approved licence) and an open licence for texts, templates and documentation (CC BY 4.0 recommended; CC0 also accepted). If you copy or adapt RvIG material, that part stays under the EUPL-1.2.
- Code contributed *into this starter repo* is licensed under Apache-2.0; data and documentation under CC BY 4.0, except contributions to the two folders above.
- Laws and other sources referenced in the docs keep their own terms. Link to them; do not copy protected texts into the repo.

By submitting a contribution you confirm that you have the right to license it under these terms.
