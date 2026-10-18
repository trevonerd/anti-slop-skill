# English lexicon

Word and phrase signals for English copy. Read the density rule first: a word on this page is a reason to reread a sentence, not a verdict. Source keys in square brackets point to [sources.md](sources.md).

| Label | Meaning |
|---|---|
| strong | rare in comparable human text, or measured many times above the human rate |
| medium | much more common in model output, still used by good human writers |
| weak | says almost nothing alone |
| active | still over-represented in 2026 models |
| saturated | everyone knows it, it still shows up |
| fading | newer models use it less |
| historical | typical of 2023-2024 models |
| model-dependent | strong for one model family, absent in another |

## Contents
- How the vocabulary changes over time
- Phrases (strongest first)
- Single words
- Copulas and vague links
- What is not a signal

<!-- slop-scan: off -->
## How the vocabulary changes over time

Model vocabularies shift with each generation, so a list from 2024 gives false alarms today [W1][GRA]. Wikipedia's editors group the words by era [W1]:

| Era | Typical words | Trend |
|---|---|---|
| 2023 to mid 2024 | additionally, boasts, crucial, delve, garner, intricate, interplay, landscape, meticulously, pivotal, tapestry, testament, underscore, vibrant | historical |
| mid 2024 to mid 2025 | align with, enhance, fostering, highlighting, showcasing, pivotal, vibrant | fading |
| mid 2025 to mid 2026 | emphasizing, enhance, highlighting, showcasing, language about media coverage | active |
| from mid 2026 | challenge, clearer, dependable, echoed, foster, leverage, matters, multifaceted, practical, prioritize, quietly, steady; shorter sentences with many semicolons | active |

Graphite measured that 65% of the tells it found belong to one model family, and that 55-72% of tells change between two consecutive versions of the same model [GRA]. Practical consequence: weigh clusters and structure more than any single word.

## Phrases (strongest first)

| Signal | Examples | Reliability | Trend |
|---|---|---|---|
| Chatbot residue | "Here's your caption:", "I hope this helps", "Would you like me to...", "Let me know if you'd like more options" [W1][UNS] | strong (fingerprint) | active |
| Knowledge-cutoff and AI disclaimers | "As an AI language model", "as of my last knowledge update" [W1] | strong (fingerprint) | historical |
| Empty openers | "In today's fast-paced world", "In the ever-evolving landscape of" [UNS][SCR] | strong | saturated |
| Importance prefaces | "It's worth noting", "It is important to note", "worth mentioning" [W1][UNS] | strong | saturated |
| Signalling that something matters | "matters because" (357x the human rate in one 2026 model), "this distinction matters", "what matters is" [GRA][W1] | strong | active |
| Legacy and significance puffery | "a testament to", "stands as", "serves as a", "plays a pivotal role", "marks a shift", "reflects broader trends", "setting the stage for" [W1][UNS][TC] | strong in neutral prose | active |
| Travel-brochure language | "nestled in", "in the heart of", "rich heritage", "diverse array", "natural beauty", "renowned" [W1] | strong in text that should be neutral | active |
| Marketing clichés | "look no further", "unlock the power of", "elevate your", "embark on a journey", "immerse yourself", "game-changer", "take it to the next level" [UNS][SCR] | strong | saturated |
| Ritual announcements | "thrilled to announce", "excited to share", "humbled to", journey and chapter metaphors [SLO] | strong | saturated |
| Plastic empathy | "You're not alone", therapist register in non-therapy text [SLO] | strong | saturated |
| Viral hook templates | "Here's the thing", "Here's the kicker", "Let that sink in", "Read that again", "No fluff" [SLO][ORI] | medium to strong | saturated |
| Ritual closers and CTAs | "Curious what others think", "Let me know in the comments" [SLO][GRA] | medium to strong | active |
| Audience catch-all | "Whether you're studying or relaxing...", "perfect for any occasion" [SCR] | strong | saturated |
| Free-benefit framing | "without sacrificing", "without compromising", "without requiring" (70x in one 2026 model) [GRA] | medium to strong | active |
| Source disclaimers | "while specific details are limited", "not widely documented" [W1] | strong | active |
| Media-coverage puffery | "featured in leading outlets", "maintains an active social media presence" [W1] | strong | active (growing since 2025) |
| Vague attributions | "experts say", "studies show", "industry reports" [W1][UNS] | strong in informative text | active |
| Review formulas | "I recently had the pleasure of", "Highly recommend" [PANB] | medium | active |
| "The real question is" | [SLO] | medium | active |
| Sincerity adverbs | "genuinely" (23x), "the actual X" (9.8x) [SLO] | medium to strong | active |
| Formal transitions at sentence start | "Moreover,", "Furthermore,", "Additionally," (about 18x each in explanatory text) [MAC][GRA] | strong in explanatory text | active |

## Single words

| Group | Words | Reliability | Trend |
|---|---|---|---|
| The famous ones | delve, tapestry | weak today | historical. Macaron counted "delve" twice in human texts and zero times in model texts [MAC]; Sloptells lists it as retired [SLO] |
| GPT-4 era cluster | vibrant, pivotal, crucial, intricate, meticulous, underscore, bolster, garner, interplay, enduring | weak alone, strong when three or more sit close together [W1] | fading |
| Explainer register | utilize (~33x), robust (~6x) [MAC] | strong in explainers | active |
| Judging adjectives that describe nothing | dependable (59x), practical (26x), meaningful (13x) for one 2026 model; deliberate, measured, steady for another; incredibly, profound, immense for a third [GRA] | medium to strong | active, model-dependent |
| Intensifiers | incredibly, absolutely, remarkably, highly, entirely, "every single", "single most", "arguably the most" [GRA] | medium | active |
| Marketing verbs | unlock, elevate, amplify, streamline, boost, leverage, seamless [GRA][UNS] | medium | fading in some families (-73% vs an earlier version) [GRA] |
| Inflated adjectives | groundbreaking, revolutionary, transformative, unprecedented, invaluable, indelible [UNS][GRA] | medium | fading |
| Ethereal imagery with no body | quiet, quietly, whispers, ghosts, shadows, hum, echo [KRI][W1] | medium | active in 2025-2026 models |
| "System" words | "the privilege of", "culinary" (13x), "showing up" [SLO] | medium | active |
| Pseudo-scientific words in one family | causal, empirical, correlate [W1] | weak | model-dependent |

## Copulas and vague links

| Signal | Examples | Reliability | Trend |
|---|---|---|---|
| Avoided "is" and "has" | "serves as", "stands as", "represents", "marks" instead of "is"; "boasts", "features", "offers" instead of "has" [W1][UNS] | strong in neutral prose | active. A study cited by Wikipedia found "is/are" down more than 10% in 2023 academic papers [W1] |
| Vague relations | "associated with", "in connection with", "linked to" when the exact relation is known [W1] | medium | active |
<!-- slop-scan: on -->

## What is not a signal

- Perfect grammar, "robotic" prose, or a mix of formal and casual registers. Wikipedia lists these as ineffective indicators [W1].
- One em dash, one list of three, one word from the tables above.
- Genre vocabulary the audience searches for. In a music channel, "lofi", "smooth jazz", "study", "Rhodes" are keywords, not slop.
- Technical terms in technical writing.
