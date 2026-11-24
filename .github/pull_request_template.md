## Summary

<!-- One paragraph: what does this PR add or change? -->

## Type of contribution

- [ ] **Hackathon team submission** (one PR per team, fork, PR into `main`)
- [ ] Starter-repo improvement (docs, data, tooling, CI)
- [ ] Bug fix
- [ ] Other (describe)

---

## For hackathon team submissions

### Team

- **Team name:**
- **Members:**
- **Folder:** `submissions/<team-name>/`
- **Focus:** [ ] Laag 1: motivering [ ] Laag 2: audit trail and quality check [ ] Laag 3: service to residents [ ] How the layers connect
- **Algorithm:** [ ] Gezag in de BRP API (this repo) [ ] Another algorithm with public rules or code (link below)

### ✅ Must checklist (jury blocking)

- [ ] **M1** The prototype shows, for at least one concrete decision, how an understandable motivering comes about.
- [ ] **M2** The explanation is understandable for the resident: *kenbaar* in the sense of article 3:47 Awb, without legal jargon.
- [ ] **M3** The solution works with the gezag algorithm from this starter repository, or with a comparable algorithm with public rules or source code (link: ).
- [ ] **M4** Open source under an OSI-approved licence (code) and CC BY 4.0 or CC0 (texts, templates, docs), with a short explanation of the approach. See [`CONTRIBUTING.md`](../CONTRIBUTING.md#licensing-of-contributions).

### ⭐ Should evidence (linked in the PR body)

- [ ] **S1** The explanation shows which data and which rules led to the outcome, linked to the audit trail.
- [ ] **S2** Missing information in the registration is signalled to the owner of the algorithm.
- [ ] **S3** The approach is a reusable template for other algorithms, not only for this use case.
- [ ] **S4** The reasoning is recorded traceably: which steps lead from registration to motivering.

### Hygiene

- [ ] Only fictional persons: the test cases from `data/rvig-gezag/` or your own made-up cases. No real personal data, no real BSN.
- [ ] Tests for your rules or templates are included and pass.
- [ ] If an LLM is used: where, why and which model is described below. It does not decide who has gezag, and it does not add facts that are not in the data, the rules or the registration.
- [ ] Nothing was sent to real algorithm owners or residents.

### Which decision, which residents

<!-- For which decision did you build the explanation, and who did you have in mind? Did you test the text with anyone? -->

### What is simulated

<!-- List every component that is simulated or mocked (for example a MijnOverheid message), and what a real version would need. -->

### Reproduction

```bash
# Single command (or short sequence) that runs your prototype from a clean checkout:
```

### Pitch artefacts

- [ ] Pitch deck (max. 10 slides), link or attachment
- [ ] Short explanation of what you built, for whom and why, with assumptions and limitations

---

## For starter-repo improvements

- [ ] Data, docs and README updated together.
- [ ] `ruff check .` and `pytest -v` pass locally (`tooling/`).
- [ ] Worked examples regenerated if templates changed (`python -m openalgoritme.explain --write-examples`).
- [ ] CI ([`.github/workflows/validate.yml`](workflows/validate.yml)) is green.
- [ ] Related issue: #
