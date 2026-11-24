# Legal context

A first map of the legal frame for this challenge, to help teams ask the right questions. It is not legal advice, and the challenge owner and mentors are the people to check it with during the hackathon.

## The motivering

- **Awb, articles 3:46 and 3:47.** A decision must rest on a sound motivering (3:46), and the motivering is stated when the decision is made known (3:47). In practice this is read as: the reasoning must carry the decision (*draagkrachtig*) and be knowable for the person concerned (*kenbaar*). [Algemene wet bestuursrecht](https://wetten.overheid.nl/BWBR0005537).
- **What this asks of an algorithm.** If an algorithm contributed to a decision, the person concerned needs to be able to follow how. Case law on this is still moving; the brief mentions two rulings of the district court of The Hague on the IND's CaseMatcher system that point in different directions.

## Objection

- **Awb, article 6:7.** The objection period is six weeks.
- **Awb, article 7:1.** Before going to court, a person first lodges an objection (*bezwaar*) with the body that took the decision.
- **The point for this challenge.** A resident can only judge whether an objection makes sense if the explanation says which facts and rules counted. The explanation has to arrive well within those six weeks, and preferably with the decision itself.

## Automated risk selection and the register

- **Motion Kathmann/Six Dijkstra (2025).** The House of Representatives unanimously asked that residents are always told when a (partly) automated risk selection led to a decision about them, with the options for objection and complaint. The cabinet is still working out how individual decisions should state this. [Motion 2025Z03194](https://www.tweedekamer.nl/kamerstukken/moties/detail?id=2025Z03194&did=2025D07227).
- **Algoritmeregister.** Publishing is voluntary. A legal obligation for high-impact algorithms has been announced, not introduced. The cabinet wants high-impact algorithms for risk selection in central government in the register by the end of 2026. The [Algoritmekader](https://algoritmes.overheid.nl/nl/algoritmekader) describes requirements and measures, also for publication.

The gezag algorithm is not a risk selection: it derives a fact (who has gezag) from registered data. The motion does not apply to it directly, but the question it asks does: does the resident know that an algorithm contributed, and how?

## AI Act and GDPR

- **AI Act, article 86.** A right to an explanation of the role of a high-risk AI system in a decision. The article applies since 2 August 2026; because of the digital omnibus (Regulation (EU) 2026/1744) the high-risk rules it refers to apply from 2 December 2027. [Article 86](https://artificialintelligenceact.eu/nl/article/86/). Whether a rule-based algorithm such as the gezag determination is an AI system under the AI Act is a question for the lawyers; the Awb applies either way.
- **GDPR, article 22.** A right not to be subject to a decision based solely on automated processing that has legal effects or similarly significant effects, with exceptions. Articles 13 to 15 add a right to meaningful information about the logic involved in such decisions. The Court of Justice held that an automatically produced score can itself fall under article 22 when a third party relies on it strongly to take its decision (Case C-634/21, *SCHUFA*, 7 December 2023). Whether that reasoning reaches an outcome like gezag, which an organisation uses but can depart from, is an open question. [GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj).

## The gezag algorithm and the decision in this starter

- **Legal basis of the algorithm.** The Wet BRP does not itself allow processing data into information that can be traced to a person. Article 4.16a allows a temporary deviation by order in council, used in the Experimentbesluit dataminimalisatie (Stb. 2024, 96). Article 2.7 of that decree regulates the *terugmelding*: the user organisation reports doubts about the information it received. All according to the registration: [Wet BRP](https://wetten.overheid.nl/BWBR0033715), [Stb. 2024, 96](https://zoek.officielebekendmakingen.nl/stb-2024-96.html).
- **Paspoortwet, article 34.** A travel document for a minor requires a declaration of consent from each person with gezag (paragraph 1); a court can replace the consent of the other parent (paragraph 2). [Paspoortwet](https://wetten.overheid.nl/BWBR0005212); see the [court procedure for replacement consent](https://www.rechtspraak.nl/onderwerpen/identiteitsbewijs-kinderen/procedure).
- **Gezagsregister.** Courts record decisions on gezag and guardianship in a public register. Anyone can request an extract, free of charge, at a district court. [Uittreksel gezagsregister](https://rechtspraak.nl/zelf-regelen/uittreksel-gezagsregister).
- **Correcting data.** A resident who finds a wrong fact about themselves in the BRP asks the municipality where they are registered to correct it. The algorithm's outcome changes only when the data change.

## Questions for Laag 3

These have no ready answer. They are good questions to put to the challenge owner and mentors:

1. When must a resident get the explanation: with the decision, before it, or on request?
2. Is an explanation sent through MijnOverheid part of making the decision known, or separate information?
3. Is a chatbot's answer an answer on behalf of the municipality? Can a resident rely on it, and what happens if it is wrong?
4. Which parts of an explanation may a language model write, and who is responsible for the text a resident reads?
5. How far does a duty to explain go for algorithms where explanation is legally or practically limited, such as fraud selection?

Many government bodies aim for language level B1 in letters to residents. That is a useful yardstick for *kenbaar*, not a legal test.
