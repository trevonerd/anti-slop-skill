# Italian lexicon (IA-taliano)

Signals for Italian copy. Treccani registered the neologism "IA-taliano" for the variety of Italian found in generative AI output [TRV]. The linguist Anna-Maria De Cesare describes English interference in synthetic Italian as "algorithmic fingerprints of English", because models learn mostly from English (about 93% English and 0.6% Italian in GPT-3's training data) [TRC]. A University of Milan study (tests from 2023 to 2025) notes that gross grammar errors and anglicisms are disappearing, so attention moves from correctness to creativity [UNIMI].

Reliability and trend labels are the same as in [lexicon-en.md](lexicon-en.md).

## Contents
- Phrases and structures
- Words
- English interference
- House rules for creators (example)
- What is not a signal

<!-- slop-scan: off -->
## Phrases and structures

| Signal | Examples | Reliability | Trend |
|---|---|---|---|
| Chatbot residue | "Certo! Ecco...", "Ecco la tua caption:", "Spero che ti sia utile", "Fammi sapere se vuoi..." (Pangram: "Certo! Ecco qui" never in human text, 94 per 10,000 words in model text) [PAN] | strong (fingerprint) | active |
| Negative parallelism | "non solo X, ma anche Y", "non si tratta di X, ma di Y", "non è X, è Y" [HUM][PAN][PRO] | strong when repeated; two or three in a row is close to certain [HUM] | active |
| Empty openers | "Nel mondo di oggi", "Nel mondo frenetico di oggi" (35x per Pangram), "Nell'era digitale", "In un contesto sempre più..." [HUM][PAN] | strong | saturated |
| Announced closers | "In conclusione", "In sintesi", "Riassumendo", "In definitiva" [HUM][PANB] | medium | saturated |
| Importance prefaces | "è importante notare che", "vale la pena sottolineare", "è fondamentale sottolineare", "va detto che" [HUM][PRO][PAN] | strong | saturated |
| Template openers | "Diamo un'occhiata", "Scopri il potere", "Non perdere", "Ecco cosa devi sapere", "Unisciti a me", "Preparati a..." [SCR] | strong | saturated |
| Escalation | "E non finisce qui", "Ma c'è di più" [SCR] | strong | saturated |
| Journey closers | "Oggi chiudo un capitolo", "Il viaggio continua", "Da qui riparto" [SCR] | strong | saturated |
| Music and mood clichés | "immergiti", "lasciati trasportare", "un viaggio sonoro", "un'esperienza unica", "atmosfera magica", "una coccola per le orecchie", "la colonna sonora perfetta", "perfetto per ogni momento", "che tu stia studiando o lavorando...", "note che raccontano storie", "emozioni pure" [SCR] | strong | saturated |
| Inflated marketing | "sfruttare il pieno potenziale", "portare al livello successivo", "aprire nuovi orizzonti", "a 360 gradi", "il futuro è qui" [HUM][SCR] | medium | active |
| Solemn truisms | "ogni viaggio inizia con un primo passo" [HUM] | medium | active |
| Bureaucratic nominal style | "l'implementazione dell'ottimizzazione dei processi", "rappresenta una risorsa che costituisce un valore aggiunto" [HUM] | medium | active |
| Final gerund of "analysis" | "...creando un'atmosfera accogliente", "...regalando emozioni" [UNS][SCR] | strong | active |
| Template CTAs | "Commenta SÌ", "Tagga un amico", "Salva se ti è piaciuto", "Manda a chi..." repeated [SCR] | medium | active |
| Perfect parallelisms | "Se X allora Y. Se non X allora non Y." [SCR] | medium | active |

## Words

| Group | Words | Reliability | Trend |
|---|---|---|---|
| Tell words | approfondire, approfondiamo, immergiamoci (Pangram: "approfondisci" 45x), panorama ("in continua evoluzione"), sfruttare, utilizzare, cruciale, vitale, essenziale, arazzo, mosaico, sinfonia, "intricato intreccio", "narrazione avvincente", "testimonianza di" [PAN][PRO][PANB] | medium to strong in a cluster | active |
| Meta-commentary | sorprendentemente, significativamente, "è importante" [SCR] | medium | active |
| Bodyless abstractions | innovativo, fondamentale, consapevole, "in modo profondo", rivoluzionario, "game changer" [SCR] | medium | active |
| Empty bridges in series | inoltre, d'altra parte, detto questo, proprio per questo, ecco perché [SCR] | medium when chained | active |
| Empty emphasis adverbs | davvero, veramente, realmente, assolutamente, letteralmente [PRO][SCR] | weak to medium | active |

## English interference

| Signal | Examples | Reliability | Trend |
|---|---|---|---|
| Calques | "basato su" everywhere, "in termini di" in every sentence, adjective before noun in the English way, "fa senso" for "ha senso", "note storte" for "stonato", "sentirsi visti", "al prossimo livello" [HUM][SCR] | medium | fading [UNIMI] |
| False friends | "realizzare" for "rendersi conto", "eventualmente" for "alla fine", "attualmente" for "in realtà", "supportare", "implementare" [HUM] | strong when present | fading [UNIMI] |
| English spelling and punctuation | capitalised months ("Marzo"), serial comma before "e", spaced em dash, invented words such as "omittare" [TRC][HUM] | strong | fading |
| Extra subject pronouns, missing clitics | "io penso... io credo..."; no "ci" or "ne" ("ci penso io", "non ne posso più") [HUM] | medium | active |
| Calqued gerunds | "implementando la soluzione, otterrai..." [HUM] | medium | active |
<!-- slop-scan: on -->

## House rules for creators (example)

A creator can add a house list on top of this file. The original project behind this skill blocks a few more items: forced clever lines that say nothing, the journey closers above, and repeated "send this to..." CTAs. Keep house rules in a separate section so that they stay distinct from research-backed signals.

## What is not a signal

- Subjunctive errors. Models use the subjunctive correctly, often more than people do [HUM].
- Regional slang and dialect the author really uses (for example words from a local dialect). That is voice. Leave it.
- Short, imperfect, spoken sentences, exclamation marks and asides in brackets. Those are human traits [GRA].
