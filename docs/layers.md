# The three layers

Teams choose one layer as their focus, or show how they connect. Per layer: what the starter gives you, where it falls short on purpose, and questions worth an answer.

## Laag 1: Motivering

**Goal.** From the registration, the rules and the data of one case, build a motivering a resident understands: which data, which rule, which reason. A step beyond the legally required minimum.

**What the starter gives you.** `python -m openalgoritme.explain` builds a motivering from four sources ([data/README.md](../data/README.md#how-the-pieces-fit)) and ends with an audit trail. Two results are in [data/rvig-gezag/examples/](../data/rvig-gezag/examples/).

**Where it falls short.** Read the example for *gezag niet te bepalen* as a parent would:

- the rule text is RvIG's text for developers ("krijgt gezag niet te bepalen geleverd wanneer de leeftijd lager is dan 18 jaar");
- the facts use BRP jargon: *RNI*, *ouder 1*, codes such as `indicatie gezag (32.10): 1`;
- every fact is listed, also the ones that did not matter for the outcome;
- nothing says what the resident can do *before* the decision, only after it.

**Questions.** Which facts made the difference, and how do you show only those? How do you write a rule in plain language without losing what it says, and who checks that? What does a resident need to decide whether an objection makes sense?

## Laag 2: Audit trail and quality check

**Goal.** Let the explanation communicate with the audit trail, and signal to the owner of the algorithm what the registration misses for a motivering. A feedback loop and a template for other algorithms.

**What the starter gives you.** `python -m openalgoritme.check` asks eleven questions of a registration and drafts a message to the owner (`--melding`). The motivering's audit trail links the rule at a pinned commit, the registration snapshot and the check result. [registration-check.md](registration-check.md) has the result for the gezag registration and what no field asks for yet.

**Where it falls short.** The checks look at whether fields are filled, not at what the text says. One check (R06) needs a person. The check has no notion of the decision that uses the outcome.

**Questions.** How does the owner receive the signal, and how do you avoid sending the same signal a hundred times? Which questions should be in a template for every algorithm that supports decisions about residents? How do you record, per decision, which version of the rule and the registration was used?

## Laag 3: Service

**Goal.** Decide how and when the resident gets the explanation, for example through MijnOverheid, and how it connects to objection. Is a chatbot's answer an answer on behalf of the municipality?

**What the starter gives you.** Little code on purpose: this layer is about the journey and the legal frame. [legal-context.md](legal-context.md) lists the frame and the open questions. [integrations/greenpt-api.md](integrations/greenpt-api.md) describes optional LLM access.

**Questions.** When does a resident need the explanation: with the decision, before it, or on request? What does a resident see in MijnOverheid, and where does the link go? What may a chatbot answer, what must it refuse, and how does it hand over to a person? How do you prevent a chatbot from stating facts or outcomes that the rules did not produce?

## Connecting the layers

A good demo often follows one case through all three: the motivering a resident reads (Laag 1), the trail behind every sentence and the signal to the owner when something is missing (Laag 2), and the moment and channel in which the resident gets it (Laag 3).
