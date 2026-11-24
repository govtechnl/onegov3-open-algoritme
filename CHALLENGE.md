# Challenge Brief | Open Algoritme

> **OneGov #3** · Challenge 4 · 9-10 December 2026 · The Hague Tech, Den Haag
>
> *From algorithm registration to an explanation residents understand.*
>
> **Put forward by and challenge owner:** Olaf Schoelink
> **Contact:** [hack@govtechnl.nl](mailto:hack@govtechnl.nl)

This is an English working translation of the Dutch challenge brief. The authoritative version is the Dutch brief on Alkemio.

*Algorithms increasingly contribute to decisions about residents, but the motivering rarely says what role they played. Teams work with a real government algorithm with public source code, the derivation of parental authority (gezag) in the BRP API of the Rijksdienst voor Identiteitsgegevens, and build an explanation that lets residents judge for themselves whether an objection makes sense.*

**Challenge owner.** Olaf Schoelink introduces the challenge at the pre-hackathon on 26 November and is present on both hackathon days for questions and to guide the teams.

---

## Background

Algorithms play a growing role in decisions about residents, but the motivering (statement of reasons) of those decisions does not yet take this sufficiently into account. The General Administrative Law Act (Algemene wet bestuursrecht, Awb) requires a decision to be based on a sound reasoning that the person concerned can know and follow ([articles 3:46 and 3:47](https://wetten.overheid.nl/BWBR0005537)): the reasoning must hold, and it must be understandable for the person the decision is about.

Courts look critically too, although the line is still moving. In cases about the IND, the district court of The Hague required documentation on how the search system CaseMatcher ranks its results, even though that system is rule-based and not self-learning. In a later ruling, the court held instead that the IND does not have to mention the use of the system in the decision, because the system does not steer the decision.

The Algoritmeregister ([algoritmes.overheid.nl](https://algoritmes.overheid.nl/nl)) makes government algorithms visible. Publishing is still voluntary: a legal obligation for high-impact algorithms has been announced, but not yet introduced. The cabinet does want high-impact algorithms for risk selection in central government to be in the register by the end of 2026. [GegevensbijBesluiten.overheid.nl](https://gegevensbijbesluiten.overheid.nl/) shows which data the government uses for decisions, with source and legal basis.

In 2025 the House of Representatives unanimously adopted the [motion by Kathmann and Six Dijkstra](https://www.tweedekamer.nl/kamerstukken/moties/detail?id=2025Z03194&did=2025D07227): residents must always be told when a (partly) automated risk selection led to a decision about them, together with the options for objection and complaint. The cabinet is still working out how individual decisions should state this.

[Article 86 of the AI Act](https://artificialintelligenceact.eu/nl/article/86/) also gives residents a right to an explanation of the role of a high-risk AI system in a decision. That article applies since 2 August 2026, but because of the digital omnibus (Regulation (EU) 2026/1744) the high-risk rules it refers to only apply from 2 December 2027.

## Problem statement

The explanation of an algorithmic decision falls short, because the building blocks that already exist are not connected:

- The motivering rarely says what role the algorithm played, which data counted and how much.
- The Algoritmeregister describes an algorithm in general. The link with the individual decision is missing.
- There is no feedback: the owner of an algorithm does not know which information is missing from the registration to give a good motivering.
- As a result, the resident may have too little information to decide whether an objection makes sense.
- It is unclear whether an answer from a chatbot counts as an answer on behalf of the municipality.

A scan of the Algoritmeregister shows how rare a good starting position is: of the 1,669 registered algorithms, 80 link to source code, and none of those is a municipal algorithm that supports an individual decision about residents (as of 20 November 2026).

## The challenge

> **How do we make decisions to which an algorithm or machine learning contributed so explainable that residents understand how the decision came about, and can judge for themselves whether they want to object?**

Teams work with one concrete algorithm: the derivation of parental authority (gezag) in the BRP API. A comparable algorithm with public rules or source code is also allowed.

## The use case: gezag in the BRP API

The use case is the algorithm *De informatievraag Gezag in de BRP API Personen* of the Rijksdienst voor Identiteitsgegevens (RvIG), in use since April 2024. From data in the Basisregistratie Personen (BRP, the Dutch personal records database) it derives who has parental authority over a minor: who the parents are, whether they are or were married, whether and when the child was recognised, and whether there is a court ruling.

The algorithm does not take a decision itself. Municipalities and other organisations with a legal task use the outcome in their decisions. Teams therefore link it to a decision in which gezag counts, such as the application for a travel document for a minor: that requires the consent of the holders of gezag.

Why this use case? The derivation rules are public, as code and in plain Dutch. The registration lists exactly which BRP data the algorithm uses. There is an outcome *gezag niet te bepalen* (gezag cannot be determined) that calls for an explanation and a next step. And the registration shows what is missing: it has not been updated since October 2024 and does not say which decisions use the outcome.

Source: the [registration in the Algoritmeregister](https://algoritmes.overheid.nl/nl/algoritme/oorg10103/61781447/de-informatievraag-gezag-in-de-brp-api-personen) (last changed 21 October 2024) and RvIG's repository [brp-api-gezag](https://github.com/BRP-API/brp-api-gezag). As of 24 November 2026.

### Building blocks

| Building block | What it is | Where to find it |
|---|---|---|
| **Registration** | Purpose, the BRP data used, legal basis, risks and human intervention | [Algoritmeregister, LARS 61781447](https://algoritmes.overheid.nl/nl/algoritme/oorg10103/61781447/de-informatievraag-gezag-in-de-brp-api-personen), snapshot in [data/algoritmeregister/](data/algoritmeregister/) |
| **Derivation rules** | Every rule in plain Dutch, with examples, as a Gherkin specification | [brp-api-gezag, folder features/specs](https://github.com/BRP-API/brp-api-gezag/tree/main/features/specs) |
| **Source code** | RvIG's gezag module in Java, under the EUPL 1.2 | [BRP-API/brp-api-gezag](https://github.com/BRP-API/brp-api-gezag) |
| **Flow chart** | The steps of the gezag determination in one chart (PDF) | [Stroomschema gezag in BRP API](https://github.com/BRP-API/Haal-Centraal-BRP-bevragen/blob/master/docs/features/Stroomschema%20gezag%20in%20BRP%20API.pdf) |
| **Test cases** | The examples from the specifications as JSON, with fictional persons | [data/rvig-gezag/](data/rvig-gezag/) |

All persons in the specifications and the starter repository are fictional. The examples use test numbers instead of real citizen service numbers (BSN).

## Three layers

Teams choose one of the three layers as their focus, or show how they connect.

| Laag 1: Motivering | Laag 2: Audit trail and quality check | Laag 3: Service |
|---|---|---|
| Build a prototype that builds an understandable motivering from the algorithm registration, the derivation rules and the data of one case: which data, which rule, which reason. The goal is a step beyond the legally required minimum explanation. | Let the explanation communicate with the audit trail: which rule applied, and with which data? If information is missing from the registration to give a motivering, the owner of the algorithm gets a notification. This creates a feedback loop and a template for the explanation of other algorithms. | Decide how and when the resident gets the explanation, for example through MijnOverheid, and how it connects to objection. Is a chatbot's answer an answer on behalf of the municipality, and which legal frameworks apply then? Deterministic and LLM techniques may be used side by side, within fixed legal frameworks. |

You build for two users with opposite needs. A good solution serves both.

**The resident who receives a decision.** An explanation in plain language of what the algorithm did, which data counted and why. Enough to choose: do I leave it, or do I object? Without legal jargon, and not only once the objection phase has started.

**The owner of the algorithm.** Insight into what is missing from the registration to give a good motivering, and a concrete signal of what to add. A reusable template, not custom work per algorithm.

### Guiding questions

- How do you translate the registration of an algorithm into a motivering that a resident without prior knowledge understands?
- How do you show which data and rules led to the outcome, without overloading the resident?
- How do you signal which information in the Algoritmeregister is missing for a good motivering, and how does that signal reach the owner?
- Which connections are needed, for example with GegevensbijBesluiten.overheid.nl and MijnOverheid, and what is feasible within a hackathon?
- How do you deal with algorithms where explanation is legally or practically limited, such as fraud selection?

## Resources and starting material

GovTechNL provides this starter repository. Teams are free to deviate from it.

| Resource | What it is | Use |
|---|---|---|
| [Starter repository onegov3-open-algoritme](https://github.com/govtechnl/onegov3-open-algoritme) | The registration of the gezag algorithm, the test cases as JSON, an example of a motivering and a check on the registration | Clone the repo and start with [START_HERE.md](START_HERE.md). |
| [BRP API Gezag (RvIG)](https://github.com/BRP-API/brp-api-gezag) | Source code, derivation rules as Gherkin specifications and the flow chart (EUPL 1.2) | The rules are your rules as code, the examples your test cases. |
| [Algoritmeregister](https://algoritmes.overheid.nl/nl) | All registrations, through the website, a JSON API and a full CSV export | For Laag 2: check registrations and make a template for other algorithms. |
| [GegevensbijBesluiten.overheid.nl](https://gegevensbijbesluiten.overheid.nl/) | Which data the government uses for decisions, with source and legal basis | Link the data in your explanation to source and legal basis. |
| [Algoritmekader (BZK)](https://algoritmes.overheid.nl/nl/algoritmekader) | Requirements and measures for the responsible use of algorithms, also for publication in the register | A touchstone for what a registration should contain. |
| GreenPT API (tech partner) | OpenAI-compatible API with credits per participant | Optional, for example for a chatbot or to explain rules in plain language. See [docs/integrations/greenpt-api.md](docs/integrations/greenpt-api.md). |

All data in the repository is fictional or public. No real personal data passes through the challenge.

## Deliverables

- A working prototype or demo that shows, for at least one decision, how an understandable motivering comes about.
- A short explanation: what you built, for whom and why, with your assumptions and limitations.
- The source code, published open source via GitHub, with a short README.
- A pitch (max. 3 minutes) and a pitch deck (max. 10 slides).
- Your submission through Alkemio, with a link to the code.

## Judging criteria

Teams are judged by an expert jury with expertise in administrative law, algorithms and AI, and open source. Four levels:

### ✅ Must: minimum requirements for a valid submission

- The prototype shows, for at least one concrete decision, how an understandable motivering comes about.
- The explanation is understandable for the resident: knowable (*kenbaar*) in the sense of article 3:47 Awb, without legal jargon.
- The solution works with the gezag determination from the starter repository, or with a comparable algorithm with public rules or source code.
- The solution is open source and contains a short explanation of the approach.

### ⭐ Should: distinguishing qualities

- The explanation shows which data and which rules led to the outcome, linked to the audit trail.
- Missing information in the registration is signalled to the owner of the algorithm.
- The approach is a reusable template for other algorithms, not only for this use case.
- The reasoning process is recorded traceably: which steps lead from registration to motivering.

### ⚠ Should not: pitfalls to avoid

- A standard text that is legally watertight but explains nothing to the resident.
- Technical perfection over understandability: for the resident, the explanation counts, not the model.
- Hardcoded motiveringen without reusable logic.
- A solution so specific to one organisation that others cannot reuse it.

### ✨ Could: bonus

- Connections with GegevensbijBesluiten.overheid.nl or MijnOverheid, as far as feasible.
- A chatbot variant that stays within legal frameworks, with a clear demarcation of what counts as an answer on behalf of the municipality.
- Attention to whether an objection makes sense, and to when in the process the explanation is offered.
- The approach applied to a second algorithm from the Algoritmeregister.

The criteria with IDs (M1 to M4, S1 to S4, X1 to X4, C1 to C4) are in [docs/judging-criteria.md](docs/judging-criteria.md).

## Preconditions

**Technology.** RvIG's gezag module is a Java application that needs a database with BRP data. You do not have to run it: the rules are readable specifications in RvIG's repository, and the test cases are JSON in the starter repository. You choose your own language and approach.

**No real personal data.** Work only with the fictional persons from the specifications and the starter repository. A connection to the real BRP is not part of the challenge.

**Algorithm and decision.** The gezag determination supplies information; the decision is taken by an administrative body, such as the municipality. Make clear in your explanation who determines what, and where a resident can go if a piece of data is wrong.

**Careful with the subject.** Gezag touches sensitive family situations, such as a divorce or a court ruling. Also with fictional persons: handle it with care, in examples, pitches and demos.

## Why join

- The winning team of this challenge pitches its solution at the challenge owner's organisation.
- You work with a real government algorithm with public source code, not with a fictional example.
- A good approach is usable for the explanation of other algorithms in the Algoritmeregister.
- Everything you build is published as open source.

## Submission

Submissions go through **Alkemio**, the central submission and review platform for OneGov. The link to the challenge space follows.

Each team submits, via Alkemio:

1. A **link to the team's Pull Request** on this repository, one PR per team (see [CONTRIBUTING.md](CONTRIBUTING.md)).
2. A **short explanation** of what you built, for whom and why, with your assumptions and limitations.
3. The **pitch deck** (max. 10 slides, PDF or link).

The Alkemio submission is what the jury scores during the hackathon. The Pull Request is still required: it holds the open source code.

## Disclaimer

The solutions produced during this hackathon are published as open source. The challenge is an innovation exercise: there are no commitments about further development or adoption in policy, and a prototype is not legal advice. All persons in the data are fictional.

Questions about the hackathon: [hack@govtechnl.nl](mailto:hack@govtechnl.nl)
