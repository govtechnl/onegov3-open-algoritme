# The use case: gezag in the BRP API

## What gezag is

Everyone in the Netherlands under 18 is under *gezag* (parental authority). Whoever has gezag over a minor is responsible for the child's care and upbringing, manages the child's money and belongings, and is the child's legal representative. Gezag stops automatically when the child turns 18. Usually the parents have it; sometimes one parent, a parent together with someone who is not a parent, or a guardian (*voogd*).

RvIG explains this in plain Dutch in the [README of its specifications](https://github.com/BRP-API/brp-api-gezag/blob/main/features/specs/README.md), including who counts as a legal parent. Read it before you write for residents: it is a good example of the tone you are aiming for.

## What the algorithm does

*De informatievraag Gezag in de BRP API Personen* derives from data in the Basisregistratie Personen (BRP) who has gezag over a minor. An organisation with a legal task asks the BRP API "who has gezag over this child?" and gets an answer, instead of receiving all the underlying data and working it out itself. The registration calls this data minimisation, and also names fewer errors, transparency and lower costs as goals.

The algorithm uses 31 data elements, listed in the registration: for example the parents' BSN and names, the date the family law relationship started, marriage and partnership dates, date of death, the *indicatie gezag minderjarige* (a code that records a court ruling on gezag) and the *indicatie curateleregister*.

It does not take a decision. The organisation that asks takes the decision, and can depart from the answer. If it doubts the answer, it can report that to RvIG (*terugmelding*, article 2.7 of the Experimentbesluit dataminimalisatie, as the registration says).

## The outcomes

| Outcome | Meaning | In the test cases |
|---|---|---:|
| gezamenlijk ouderlijk gezag | the two parents together | 126 |
| eenhoofdig ouderlijk gezag | one parent | 61 |
| voogdij | a guardian who is not a parent, possibly an organisation | 42 |
| gezag niet te bepalen | the data are not enough to tell; comes with a *toelichting* | 25 |
| gezamenlijk gezag | a parent together with someone who is not a parent | 22 |
| tijdelijk geen gezag | nobody can exercise gezag at the moment; comes with a *toelichting* | 12 |

Plus 15 outcomes in which an adult has no gezag over any child, and 4 in which no gezag is given at all (*geen gezaghouder*), for example because the person asked about is an adult or has died. Counts are outcomes in [data/rvig-gezag/scenarios.json](../data/rvig-gezag/).

The two outcomes with a toelichting are where the explanation matters most. *Gezag niet te bepalen* does not mean that nobody has gezag: it means the BRP cannot tell. The toelichtingen in the test cases name reasons such as a child who does not live in the Netherlands, or a birth mother who cannot be identified from the data. A resident who gets this outcome needs to know what happens next.

## The order of the rules

RvIG's [reading guide](https://github.com/BRP-API/brp-api-gezag/blob/main/features/specs/README.md#leeswijzer-afleidingsregels) applies the rules in this order, summarised:

1. If the minor has their habitual residence abroad, gezag cannot be determined ([niet-ingezetene.feature](https://github.com/BRP-API/brp-api-gezag/blob/main/features/specs/niet-ingezetene.feature)).
2. Check whether there is no gezag at all, for example because the person is an adult or has died ([geen-gezag.feature](https://github.com/BRP-API/brp-api-gezag/blob/main/features/specs/geen-gezag.feature)).
3. If there is a court ruling on gezag, it counts, unless a later adoption, (repair) marriage or denial of parenthood overrides it ([gerechtelijke-uitspraak.feature](https://github.com/BRP-API/brp-api-gezag/blob/main/features/specs/gerechtelijke-uitspraak.feature)).
4. Otherwise gezag follows from the number of parents and their relationship: two parents with a relationship, two parents without one, or one parent.

The flow chart ([Stroomschema gezag in BRP API](https://github.com/BRP-API/Haal-Centraal-BRP-bevragen/blob/master/docs/features/Stroomschema%20gezag%20in%20BRP%20API.pdf), PDF) shows the same steps in one picture.

## The decision in this starter: a travel document for a minor

The starter links the outcome to the application for a passport or identity card for a minor ([data/besluiten/reisdocument-minderjarige.yaml](../data/besluiten/reisdocument-minderjarige.yaml)):

- Article 34 of the [Paspoortwet](https://wetten.overheid.nl/BWBR0005212) requires a declaration of consent from each person who has gezag over the child (paragraph 1). A court can replace the consent of the other parent (paragraph 2). Checked against a 2026 ruling that cites the article: [ECLI:NL:RBZWB:2026:6594](https://omgevingsweb.nl/jurisprudentie/eclinlrbzwb20266594-rechtbank-zeeland-west-brabant-18-06-2026-c-02-446032-fa-rk-26-1323/), consideration 5.6.
- So the gezag outcome decides whose consent the municipality needs. With *gezag niet te bepalen* the municipality cannot tell from the BRP, and has to ask for more, for example an extract from the court's *gezagsregister*, which anyone can [request for free](https://rechtspraak.nl/zelf-regelen/uittreksel-gezagsregister).
- What the fictional municipality does per outcome is in the `gevolg` section of the decision file. That procedure is made up for the example; check with the challenge owners before presenting it as practice.

Other decisions in which gezag counts are possible. Add one as a new file in `data/besluiten/` and source its legal facts.

## What the starter does not do

- **Run the algorithm.** RvIG's Java module needs a database with BRP data. The test cases give the expected outcome for each situation, which is what an explanation needs.
- **Compute dates.** The test cases use relative dates ("7 jaar geleden geboren") and some fixed dates. They are kept as written.
- **Touch real data.** There is no connection to the BRP, MijnOverheid or any real system.
