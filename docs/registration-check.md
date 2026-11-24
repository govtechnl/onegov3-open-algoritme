# The registration check (Laag 2)

A motivering for an individual decision needs answers that should be in the registration of the algorithm: what it does, which data it uses, on which legal basis, and what a resident can do if the outcome is wrong. The check asks those questions of a registration and says, per question, whether the registration answers it.

**It is not a test against the publication standard of the Algoritmeregister.** A field can be optional in the standard and still be needed to explain a decision. And the observations below are about what a motivering needs, not a judgement of RvIG: this registration is one of the most complete starting points in the register, with public code and a detailed list of data.

## The questions

| ID | Question | Fields | Statuses |
|---|---|---|---|
| R01 | Wat doet het algoritme? | `description_short`, `goal` | ok / ontbreekt |
| R02 | Welke gegevens gebruikt het? | `source_data` | ok / ontbreekt |
| R03 | Waar komen die gegevens vandaan? | `source_data_grouping` | ok / aandacht (no link) / ontbreekt |
| R04 | Op welke wettelijke grondslag? | `lawful_basis`, `lawful_basis_grouping` | ok / aandacht (no link) / ontbreekt |
| R05 | Zijn de regels en de code openbaar? | `methods_and_models`, `publiccode` | ok / aandacht (one of two) / ontbreekt |
| R06 | Voor welke besluiten wordt de uitkomst gebruikt? | `decision_making_process`, `impact`, `goal` | ok / handmatig |
| R07 | Kijkt er een mens mee, en wie beslist? | `human_intervention` | ok / ontbreekt |
| R08 | Wat kan een inwoner doen als de uitkomst niet klopt? | `objection_procedure` | ok / ontbreekt |
| R09 | Zijn de impacttoetsen in te zien? | `impacttoetsen_grouping` | ok / aandacht (not public) / ontbreekt |
| R10 | Is de registratie actueel? | `create_dt` | ok / aandacht (older than a year) |
| R11 | Bij wie kan iemand terecht met vragen? | `contact_email` | ok / ontbreekt |

`handmatig` means a person has to read the text. After reading, confirm a gap with `--bevestig R06`; unconfirmed manual checks never go into the message to the owner.

```bash
cd tooling
python -m openalgoritme.check                          # report
python -m openalgoritme.check --melding                # draft message to the owner, never sent
python -m openalgoritme.check --melding --bevestig R06
python -m openalgoritme.check --format json
```

## Result for the gezag registration

Snapshot of 24 November 2026, assessed on that date:

| ID | Status | Finding |
|---|---|---|
| R01-R05 | ok | Purpose, 31 data elements, source (Logisch Ontwerp BRP), legal basis with links, public code |
| R06 | handmatig | No separate field. See the manual review below |
| R07 | ok | Human intervention is described |
| R08 | ontbreekt | No route for residents to contest an outcome or have data corrected |
| R09 | aandacht | The DPIA is only available on request ("Opvraagbaar via info@rvig.nl") |
| R10 | aandacht | Last changed 21 October 2024 |
| R11 | ok | Info@rvig.nl |

## Manual review

Read on 24 November 2026 by the authors of this starter repository.

- **R06, which decisions use the outcome.** *Doel en impact* describes the goals of the BRP API algorithms in general (data minimisation, fewer errors, transparency, lower costs). It does not name the decisions that use the gezag outcome, such as a travel document for a minor. Gap confirmed: `--bevestig R06`.
- **Routes in the text are for organisations, not residents.** *Menselijke tussenkomst* and *Risicobeheer* describe the user organisation's options: it can depart from the answer, and report doubts to RvIG (*terugmelding*). Neither tells a resident where to go.
- **A sentence about another algorithm.** *Afwegingen* contains the sentence "De informatievraag Leeftijd wordt gebruikt door organisaties die ... alleen de leeftijd van de persoon nodig hebben". The register lists *De informatievraag Leeftijd in de BRP API Personen* as a similar registration; the sentence looks reused from it. A check could look for names of other algorithms in a text.

## What no field asks for yet

These came up while building the explanation. They are candidates for a template, and good material for teams in Laag 2:

1. **The possible outcomes and what they mean.** The registration does not list them. *Gezag niet te bepalen* and *tijdelijk geen gezag* in particular need an explanation and a next step.
2. **The decisions that use the outcome**, and which organisation takes them.
3. **The version of the rules.** The registration links to the code, not to the version in use at a given date. A motivering should point to the rule that was applied at the time.
4. **A route for residents**, separate from the route for user organisations.

## Ideas for teams

- Use a language model to *suggest* an answer to a manual check, with the passage it relied on, for a person to confirm.
- Run the check over many registrations: the register's CSV export has every registration (see [data/algoritmeregister/README.md](../data/algoritmeregister/README.md)). Which questions are most often unanswered?
- Turn the questions into a template that an owner fills in once per algorithm, and that a motivering can read.
