# Algoritmeregister snapshot

[gezag-61781447.json](gezag-61781447.json) is the registration of *De informatievraag Gezag in de BRP API Personen* (Rijksdienst voor Identiteitsgegevens) in the Algoritmeregister.

| | |
|---|---|
| Page | <https://algoritmes.overheid.nl/nl/algoritme/oorg10103/61781447/de-informatievraag-gezag-in-de-brp-api-personen> |
| API | `GET https://algoritmes.overheid.nl/api/algoritme/NLD/61781447` |
| Retrieved | 24 November 2026 |
| Last changed in the register | 21 October 2024 (`create_dt` of this version) |
| Publication standard | 1.0 (`standard_version`) |
| Integrity | `sha256` in the file: SHA-256 of the record as compact JSON. A test checks it, so a hand edit fails CI. |

## File format

```json
{
  "source": "https://algoritmes.overheid.nl/api/algoritme/NLD/61781447",
  "page": "https://algoritmes.overheid.nl/nl/algoritme/...",
  "retrieved": "2026-11-24",
  "terms": "https://algoritmes.overheid.nl/nl/footer/copyright",
  "note": "...",
  "sha256": "...",
  "record": { "...": "the unmodified API response, 56 fields" }
}
```

Text fields in `record` contain HTML as published (`<p>`, `<ul><li>`). `tooling/openalgoritme/register.py` turns them into plain text. 28 of the 56 fields are empty for this registration; the register's website only shows filled fields.

Labels: the website shows `goal` as *Doel en impact*, `proportionality` as *Afwegingen*, `human_intervention` as *Menselijke tussenkomst*, `risks` as *Risicobeheer*, `source_data` as *Gegevens*, `methods_and_models` as *Technische werking* and `publiccode` as *Link naar broncode*. The full mapping, checked on 24 November 2026, is in `LABELS` in [register.py](../../tooling/openalgoritme/register.py).

## Refresh, or fetch another registration

The register has a public JSON API without a key. With internet access:

```bash
cd tooling
python -m openalgoritme.register fetch 61781447 --out ../data/algoritmeregister/gezag-61781447.json
python -m openalgoritme.register fetch <LARS> --out other.json    # any other registration
python -m openalgoritme.check --snapshot other.json
```

The LARS number is in the URL of every registration. The full register is also available as a CSV export (`GET https://algoritmes.overheid.nl/api/downloads/NLD?filetype=csv`); its `publiccode` column holds the link to source code, if any.

## Terms

The register's [copyright page](https://algoritmes.overheid.nl/nl/footer/copyright) says the content of the website may be reused, unless a part states otherwise, and that a citation must not suggest that the Rijksoverheid supports the work that cites it. This repository is not endorsed by the Rijksoverheid or by RvIG.

What the registration does and does not contain for a motivering: [docs/registration-check.md](../../docs/registration-check.md).
