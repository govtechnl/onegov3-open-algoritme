# Uitleg bij de aanvraag van een paspoort of identiteitskaart voor Bert

> Voorbeeld met fictieve personen uit de testgevallen van de Rijksdienst voor Identiteitsgegevens, gemaakt met de startrepository van OneGov #3. Dit is geen echt besluit.

## Waarom kijken we naar het gezag?

U heeft een paspoort of identiteitskaart aangevraagd voor Bert.

Voor een paspoort of identiteitskaart voor een kind onder de 18 jaar is toestemming nodig van iedereen die het gezag over het kind heeft.

Dit staat in artikel 34 van de Paspoortwet.

## Wie heeft het gezag?

Gerda en Aart hebben samen het gezag over Bert. Dit heet gezamenlijk ouderlijk gezag: de twee ouders hebben samen het gezag.

## Welke gegevens zijn gebruikt?

Deze gegevens uit de Basisregistratie Personen (BRP) zijn gebruikt:

- Gerda is meerderjarig
- Aart is meerderjarig
- Bert is ingeschreven in de BRP
- Bert heeft Aart en Gerda als ouders
- Bert is 7 jaar geleden geboren
- Gerda en Aart zijn 8 jaar geleden gehuwd

## Welke regel is toegepast?

Als de ouders na de geboorte van minderjarige een periode met elkaar gehuwd zijn (geweest) of partnerschap hebben (gehad), dan hebben de ouders gezamenlijk ouderlijk gezag.

Deze regel staat in de openbare afleidingsregels van de Rijksdienst voor Identiteitsgegevens. Zie [features/specs/twee-ouders-met-relatie.feature, regel 19](https://github.com/BRP-API/brp-api-gezag/blob/1d736060ff14bb912c5e970ef6de4f07db2c1597/features/specs/twee-ouders-met-relatie.feature#L19).

## Wat betekent dit voor uw aanvraag?

Wij hebben daarom toestemming nodig van Gerda en Aart.

- Wil een ouder met gezag geen toestemming geven? Dan kunt u de rechter vragen om vervangende toestemming.

## Wie besliste wat?

Wie het gezag heeft, bepaalt het algoritme 'De informatievraag Gezag in de BRP API Personen' van de overheid (Rijksdienst voor Identiteitsgegevens). Dat gebeurt met vaste, openbare regels en met gegevens uit de Basisregistratie Personen (BRP). Het algoritme neemt zelf geen besluit.

Het besluit over uw aanvraag neemt de gemeente.

Twijfelt de gemeente aan de uitkomst? Dan kan de gemeente dat melden bij de Rijksdienst voor Identiteitsgegevens. Zo'n terugmelding is geregeld in artikel 2.7 van het Experimentbesluit dataminimalisatie.

## Klopt er iets niet?

Klopt een gegeven over u of uw kind niet? Vraag dan de gemeente waar u staat ingeschreven om het gegeven in de BRP te verbeteren.

Bent u het niet eens met het besluit op uw aanvraag? Dan kunt u binnen zes weken bezwaar maken bij de gemeente.

## Bronnen

- [Registratie in het Algoritmeregister](https://algoritmes.overheid.nl/nl/algoritme/oorg10103/61781447/de-informatievraag-gezag-in-de-brp-api-personen)
- [Afleidingsregel: features/specs/twee-ouders-met-relatie.feature, regel 19](https://github.com/BRP-API/brp-api-gezag/blob/1d736060ff14bb912c5e970ef6de4f07db2c1597/features/specs/twee-ouders-met-relatie.feature#L19)
- [Experimentbesluit dataminimalisatie](https://zoek.officielebekendmakingen.nl/stb-2024-96.html)
- [Wet Basisregistratie Personen](https://wetten.overheid.nl/BWBR0033715)
- [Paspoortwet, artikel 34](https://wetten.overheid.nl/BWBR0005212)
- [Vervangende toestemming voor een identiteitsbewijs voor een kind (Rechtspraak)](https://www.rechtspraak.nl/onderwerpen/identiteitsbewijs-kinderen/procedure)
- [Uittreksel gezagsregister opvragen (Rechtspraak)](https://rechtspraak.nl/zelf-regelen/uittreksel-gezagsregister)
- [Algemene wet bestuursrecht, artikel 6:7 (bezwaartermijn van zes weken)](https://wetten.overheid.nl/BWBR0005537)

## Verantwoording

| | |
|---|---|
| scenario | twee-ouders-met-relatie:19 |
| afleidingsregel | features/specs/twee-ouders-met-relatie.feature:19 @ 1d736060ff14 |
| registratie | LARS 61781447, laatst gewijzigd 21 oktober 2024, momentopname 24 november 2026 |
| registratiecheck | ontbreekt: R08; aandacht: R09, R10; handmatig: R06 |
| sjablonen | data/uitleg/gezag.yaml; besluit: reisdocument-minderjarige |
| tool | openalgoritme 0.1.0 |
