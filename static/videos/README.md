# Hero Video Files

Tähän kansioon tulee lisätä hero-osion taustalla pyörivä video.

## Tarvittavat tiedostot:

1. **hero-video.mp4** - Päävideoformaatti (H.264/MP4)
2. **hero-video.webm** - Vaihtoehtoinen formaatti (WebM)

## Video-vaatimukset:

- **Kesto**: 10-30 sekuntia (looppaa automaattisesti)
- **Resoluutio**: Vähintään 1920x1080 (Full HD)
- **Suhde**: 16:9 (landscape)
- **Koko**: Alle 10MB optimaalinen
- **Sisältö**: Liittyy Suomi-Israel teemaan

## Suositukset:

- Käytä matala liike (subtle motion) parempaa suorituskykyä varten
- Varmista että video toimii ilman ääntä
- Testaa eri laitteilla ja selaimilla
- Optimoi tiedostokoko web-käyttöön

## Fallback:

Jos videotiedostoja ei ole saatavilla, sivusto käyttää automaattisesti 
`images/hero.jpg` -kuvaa taustana.

## Tekniset yksityiskohdat:

- Video ladataan automaattisesti (`autoplay muted loop`)
- Mobiililaitteilla käytetään kuva-fallbackia suorituskyvyn vuoksi
- Video pysähtyy kun ei ole näkyvissä (Intersection Observer)
- Virhetilanteissa siirrytään automaattisesti kuva-fallbackiin