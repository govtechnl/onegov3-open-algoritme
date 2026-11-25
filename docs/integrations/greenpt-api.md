# GreenPT API (optional)

[GreenPT](https://greenpt.nl/), the tech partner of the OneGov Hackathon Series, provides API access to LLMs hosted on European infrastructure. It is an **optional resource** for teams that want an AI step in their prototype.

## Where an LLM call might help

- **Rephrasing.** Turn a rule text written for developers into a plain-language draft, for a person to check before it is used.
- **Questions from residents.** A chatbot that answers questions about an explanation the resident already received, using only that explanation and its sources.
- **Reading registrations.** Suggest an answer to a manual check (for example R06), quoting the passage it relied on, for a person to confirm.

## Where an LLM call should **not** be used

- To decide who has gezag. That follows from RvIG's rules and the test cases.
- To add facts, rules or legal consequences that are not in the data, the registration or a sourced template.
- To send anything a resident reads without a check, by a person or by tests.
- With real personal data. Only the fictional persons from the test cases.

## Practical notes

- **Access.** Every participant can claim free API credits through GreenPT's sign-up link, shared on [Alkemio](https://alkem.io/onegov-hackathon) and at the kick-off. Documentation: [docs.greenpt.ai](https://docs.greenpt.ai/). Keep them in environment variables, never in git.
- **Reproducibility.** Pin a model version and log prompts and responses wherever they influence what a resident sees. Those logs are part of your audit trail.
- **Laag 3.** If a chatbot answers on behalf of a municipality, show where it refuses and where it hands over to a person.

If your submission uses GreenPT or another LLM, note in your README and your Alkemio submission **where**, **why** and **which model**.

GreenPT awards a bonus prize to a team that makes good use of its API; GreenPT selects the winner. See [EVENT.md](../../EVENT.md#prizes).
