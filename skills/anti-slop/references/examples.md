# Examples: before and after

All examples come from real reviews, anonymised: no names, channel names, track titles or locations. Each one shows the quote, the signal, the severity, the verdict and the rewrite.

<!-- slop-scan: off -->
## 1. YouTube description (BLOCKED)

Before:
> Soft Rhodes piano, brushed drums, upright bass, tenor sax and muted trumpet, with gentle rain in the background.
> Music generated with AI and curated, arranged and mastered by [channel].

| Quote | Signal | Severity |
|---|---|---|
| "with gentle rain in the background" | stated sound that is not in the audio (the mix contains only the music masters; rain is in the animation and in 3 of 9 prompts) | BLOCKER |
| "curated, arranged and mastered" | inflated role inside a list of three; the model generated the arrangements | BLOCKER |

After:
> Soft Rhodes piano, brushed drums, upright bass, tenor sax and muted trumpet, for a grey, rainy-day mood. Nine instrumental tracks, no vocals, made to sit in the background without getting in your way.
> Music generated with AI, then selected, edited and mastered by [channel].

## 2. Short title with pseudo-agency (BLOCKED)

Before: "The rain is stopping. This piano knows it."
- "This piano knows it": pseudo-agency, a clever line with no fact, two-beat staccato. MAJOR, plus a house rule against empty clever lines.
After: "Piano jazz for the end of a rainy morning"

## 3. Short title with a promise (BLOCKED)

Before: "Muted trumpet and rain on the window. Instant calm."
- "Instant calm": unverifiable promise. BLOCKER.
- "rain on the window": the track has no rain in its audio. BLOCKER for the audio claim.
After: "Muted trumpet lofi jazz for a rainy evening in" (the rain is now the listener's weather, not a sound).

## 4. Series CTA (BLOCKED for the series)

Before: four Shorts in one week end with "Send this to someone who...", and two of them repeat the CTA in both overlay and caption.
- Repeated CTA template across the series; double CTA in one piece. MAJOR per piece, BLOCKED for the series pattern.
After: one CTA per Short at most, varied, and none in most Shorts. Example caption: "Rhodes and brushed drums, quiet enough to keep working."

## 5. "The actual X" (BLOCKED in context)

Before: "Bossa nova for the lunch break you actually deserve"
- "you actually deserve": sincerity adverb (active signal) plus a self-care cliché. MAJOR. Alone it would be a note; with the cliché the title says nothing concrete.
After: "Bossa nova and soft sax for a rainy lunch break"

## 6. What passed (APPROVED)

- "7:30, kettle on, first track of the mix. The Rhodes comes in at 0:12. #smoothjazz #lofi #Shorts": a time, an action, a checkable detail, three hashtags.
- "Via [street] is covered in porticoes": a factual local detail, verified.
- "but make it soft": a meme template, accepted once in a series of 21 (NOTE).

## 7. Generic social post, English (REWRITE mode)

Before:
> In today's fast-paced world, finding focus isn't just about willpower, it's about creating the right environment. Our vibrant playlist seamlessly blends lofi beats and smooth jazz, fostering a sense of calm. Whether you're studying or working, it's the perfect companion. The result? Pure productivity.

Signals: empty opener; "isn't just X, it's Y"; "vibrant", "seamlessly", "fostering" cluster; trailing "-ing" clause; audience catch-all; "perfect companion"; rhetorical question with instant answer; no fact at all. Verdict: BLOCKED (cluster).

After (keywords kept: lofi, smooth jazz, study, work):
> Two hours of lofi and smooth jazz we made for our own work mornings. No vocals, the drums stay on brushes the whole time, and track 4 has a muted trumpet I still like after fifty listens. Good for studying if lyrics distract you.

Note: "two hours", "brushes", "track 4", "fifty listens" must come from the author. If they are not known, ask, or write a shorter post with only verified facts.

## 8. Italian caption (REWRITE mode)

Before:
> Nel mondo frenetico di oggi, immergiti in un viaggio sonoro unico. Non è solo musica, è un'esperienza indimenticabile che ti farà rilassare all'istante.

Signals: empty opener, two mood clichés, "non è solo X, è Y", unverifiable promise ("all'istante"). Verdict: BLOCKED.

After:
> Pioggia fuori, moka sul fuoco e un Rhodes che parte piano. Quarantotto minuti di jazz lofi senza voce, da mettere in sottofondo mentre lavori.

## 9. Fingerprints (always BLOCKED)

- "Here's your caption: Rainy jazz for slow mornings ☕" → chatbot residue. Delete the wrapper.
- "Listen on [Insert link]" → placeholder.
- "Smooth jazz history :contentReference[oaicite:0]{index=0}" → citation code from a chatbot.
- "https://example.com/?utm_source=chatgpt.com" → link copied from a chatbot answer. Remove the parameter and open the link to check it says what the text claims.
<!-- slop-scan: on -->

## Report excerpt (format to copy)

| Piece | Verdict | Reason |
|---|---|---|
| Title | APPROVED | keywords plus a real detail; 84 characters |
| Description | BLOCKED | stated sound not in the audio; inflated role |
| Short 07 | BLOCKED | pseudo-agency; instrument not audible at the clip start (confirm by listening) |
| Short 13 | APPROVED (note) | meme template, accepted once |
