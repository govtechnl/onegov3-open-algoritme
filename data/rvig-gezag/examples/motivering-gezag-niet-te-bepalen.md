# Uitleg bij de aanvraag van een paspoort of identiteitskaart voor Mees

> Voorbeeld met fictieve personen uit de testgevallen van de Rijksdienst voor Identiteitsgegevens, gemaakt met de startrepository van OneGov #3. Dit is geen echt besluit.

## Waarom kijken we naar het gezag?

U heeft een paspoort of identiteitskaart aangevraagd voor Mees.

Voor een paspoort of identiteitskaart voor een kind onder de 18 jaar is toestemming nodig van iedereen die het gezag over het kind heeft.

Dit staat in artikel 34 van de Paspoortwet.

## Wie heeft het gezag?

Uit de gegevens in de BRP is niet af te leiden wie het gezag over Mees heeft. Dat betekent niet dat niemand het gezag heeft. Er zijn alleen niet genoeg gegevens om het met zekerheid te zeggen.

De gezagsbepaling geeft hierbij deze toelichting: Gezag kan niet worden bepaald omdat minderjarige niet in Nederland woont.

## Welke gegevens zijn gebruikt?

Deze gegevens uit de Basisregistratie Personen (BRP) zijn gebruikt:

- Mark is ingeschreven in de BRP
- Mark is meerderjarig
- Marlies is ingeschreven in de BRP
- Marlies is meerderjarig
- Mark en Marlies zijn met elkaar gehuwd
- Mees is ingeschreven in de RNI
- Mees is minderjarig
- Mees is in Nederland geboren
- Mees is niet geëmigreerd geweest
- Mees heeft Marlies als ouder 1
- Mees heeft Mark als ouder 2

## Welke regel is toegepast?

Een persoon die in RNI staat ingeschreven krijgt gezag niet te bepalen geleverd wanneer de leeftijd lager is dan 18 jaar.

Deze regel staat in de openbare afleidingsregels van de Rijksdienst voor Identiteitsgegevens. Zie [features/specs/gezag-meerderjarige/meerderjarige-rni.feature, regel 18](https://github.com/BRP-API/brp-api-gezag/blob/1d736060ff14bb912c5e970ef6de4f07db2c1597/features/specs/gezag-meerderjarige/meerderjarige-rni.feature#L18).

## Wat betekent dit voor uw aanvraag?

Wij kunnen daarom niet vaststellen wie toestemming moet geven. Wij vragen u om een uittreksel uit het gezagsregister. Dat kunt u gratis opvragen bij de rechtbank.

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
- [Afleidingsregel: features/specs/gezag-meerderjarige/meerderjarige-rni.feature, regel 18](https://github.com/BRP-API/brp-api-gezag/blob/1d736060ff14bb912c5e970ef6de4f07db2c1597/features/specs/gezag-meerderjarige/meerderjarige-rni.feature#L18)
- [Experimentbesluit dataminimalisatie](https://zoek.officielebekendmakingen.nl/stb-2024-96.html)
- [Wet Basisregistratie Personen](https://wetten.overheid.nl/BWBR0033715)
- [Paspoortwet, artikel 34](https://wetten.overheid.nl/BWBR0005212)
- [Vervangende toestemming voor een identiteitsbewijs voor een kind (Rechtspraak)](https://www.rechtspraak.nl/onderwerpen/identiteitsbewijs-kinderen/procedure)
- [Uittreksel gezagsregister opvragen (Rechtspraak)](https://rechtspraak.nl/zelf-regelen/uittreksel-gezagsregister)
- [Algemene wet bestuursrecht, artikel 6:7 (bezwaartermijn van zes weken)](https://wetten.overheid.nl/BWBR0005537)

## Verantwoording

| | |
|---|---|
| scenario | gezag-meerderjarige/meerderjarige-rni:18 |
| afleidingsregel | features/specs/gezag-meerderjarige/meerderjarige-rni.feature:18 @ 1d736060ff14 |
| registratie | LARS 61781447, laatst gewijzigd 21 oktober 2024, momentopname 24 november 2026 |
| registratiecheck | ontbreekt: R08; aandacht: R09, R10; handmatig: R06 |
| sjablonen | data/uitleg/gezag.yaml; besluit: reisdocument-minderjarige |
| tool | openalgoritme 0.1.0 |
