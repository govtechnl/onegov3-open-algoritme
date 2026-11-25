# Judging criteria

How the expert jury, with expertise in administrative law, algorithms and AI, and open source, weighs submissions. Four levels: **Must**, **Should**, **Should not**, **Could**. The criteria are those of the challenge brief; the IDs and the right-hand column are added in this repository to help teams, they are not a description of the jury's procedure.

A submission that fails any Must criterion is not a valid submission, regardless of how well it scores on the rest.

## ✅ Must: minimum requirements for a valid submission

| # | Criterion | What makes it visible |
|---|---|---|
| M1 | The prototype shows, for at least one concrete decision, how an understandable motivering comes about. | A demo from case to motivering for a named decision, for example a travel document for a minor ([data/besluiten/](../data/besluiten/)) |
| M2 | The explanation is understandable for the resident: knowable (*kenbaar*) in the sense of article 3:47 Awb, without legal jargon. | The text a resident reads, ideally tested with someone outside the team; see [legal-context.md](legal-context.md) |
| M3 | The solution works with the gezag determination from the starter repository, or with a comparable algorithm with public rules or source code. | Test cases from [data/rvig-gezag/](../data/rvig-gezag/), or a link to the other algorithm's rules or code |
| M4 | The solution is open source and contains a short explanation of the approach. | Public repository, linked in Alkemio, under an OSI-approved licence (code) and CC BY 4.0 or CC0 (texts, templates, docs) |

## ⭐ Should: distinguishing qualities

| # | Criterion | What it looks like |
|---|---|---|
| S1 | The explanation shows which data and which rules led to the outcome, linked to the audit trail. | Each sentence traceable to a fact, a rule at a fixed version, or a template; the starter's *Verantwoording* table is a minimal version |
| S2 | Missing information in the registration is signalled to the owner of the algorithm. | A message or ticket for the owner, drafted from the registration; see [registration-check.md](registration-check.md) |
| S3 | The approach is a reusable template for other algorithms, not only for this use case. | Templates and checks that do not mention gezag in code; a second algorithm plugged in |
| S4 | The reasoning process is recorded traceably: which steps lead from registration to motivering. | A log or document per motivering with sources, versions and choices |

## ⚠ Should not: pitfalls to avoid

| # | Pitfall | Why it weakens a submission |
|---|---|---|
| X1 | A standard text that is legally watertight but explains nothing to the resident. | Fails the point of the challenge and probably M2 |
| X2 | Technical perfection over understandability. | For the resident, the explanation counts, not the model |
| X3 | Hardcoded motiveringen without reusable logic. | Fails S3; works for the demo case only |
| X4 | A solution so specific to one organisation that others cannot reuse it. | Fails S3; the register has many owners |

## ✨ Could: bonus for outstanding submissions

| # | Bonus | Evidence |
|---|---|---|
| C1 | Connections with GegevensbijBesluiten.overheid.nl or MijnOverheid, as far as feasible. | A working link, or a clearly labelled mock of the message and where it links to |
| C2 | A chatbot variant that stays within legal frameworks, with a clear demarcation of what counts as an answer on behalf of the municipality. | Refusals and hand-overs shown in the demo; facts only from the rules and data |
| C3 | Attention to whether an objection makes sense, and to when in the process the explanation is offered. | The resident's journey, with the moment of the explanation and the six-week objection period |
| C4 | The approach applied to a second algorithm from the Algoritmeregister. | A second registration through the same template; `python -m openalgoritme.register fetch` gets you started |

## How judging works

Musts are pass or fail. Teams pitch per challenge in a first round (10 December, 14:00-15:00), a technical jury reviews every submission in Alkemio, and the best team per challenge goes to the final, where the grand jury scores six criteria from 1 to 5. See [EVENT.md](../EVENT.md#how-judging-works).
