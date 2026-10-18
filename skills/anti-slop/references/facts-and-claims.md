# Facts and claims

This file decides most BLOCKED verdicts. A false or unverifiable claim is a problem whoever wrote it, and it is the one thing a reader can be hurt by [W1][GGL].

## Contents
- The base pattern: regression to the mean
- Always blocking
- Verification procedure
- Transparency about AI involvement
- What to do when you cannot verify

## The base pattern: regression to the mean

Model text tends to drop rare, specific details and replace them with general, positive statements that would fit any subject. The subject becomes less precise and more inflated at the same time [W1]. Two checks follow:

1. **Interchangeability.** Would this description work unchanged for another product, video, city or person? If yes, it carries no information. Strong as a quality criterion.
2. **Missing specifics.** No names, numbers, places, dates, or things only the maker knows [MAC][W1]. Macaron lists this among its four main checks [MAC].

<!-- slop-scan: off -->
## Always blocking

| Problem | Examples |
|---|---|
| Invented or unverifiable facts | durations, timestamps, BPM, prices, dates, quotes, statistics that no project file or source supports |
| Promises the content cannot keep | "instant calm", "guaranteed focus", "100% relaxing", "scientifically proven", "will put you to sleep in 5 minutes", "no ads" (the creator does not control ads on YouTube) |
| Features or sounds that are not there | "gentle rain in the background" when the audio has no rain layer; "soft sax" in a clip where the sax has not come in yet |
| Inflated role | "composed, arranged and performed by us" when a model generated the arrangement; "live musicians" for generated music |
| Broken or invented sources | citations that do not say what is claimed, wrong DOI or ISBN, dead links that were never archived [W1] |
| Speculation stated as fact | "likely" or "presumably" followed by a precise claim [W1] |
| Metadata errors | Google asks people to check generated titles, meta descriptions and alt text by hand [GGL] |
<!-- slop-scan: on -->

## Verification procedure

1. List every factual claim in the piece: numbers, names, places, instruments, sounds, durations, dates, rankings, causes, quotes, "first" and "only".
2. For each claim, find the source: a project file (tracklist, product sheet, brief), the media itself (listen, watch, measure the duration), or a public source you can open.
3. Mark each claim **verified**, **contradicted** or **unverifiable**. Quote the source line or name the file.
4. Contradicted or unverifiable claims are BLOCKERS. Write the rewrite without them, and say what evidence would let the claim come back.
5. Check internal consistency: timestamps in order, first chapter at 0:00, last chapter before the end, totals that add up.

Example from a real review (anonymised): the description said "with gentle rain in the background". The audio concat list contained only the music masters, the rain existed only in the animation, and only 3 of 9 prompts mentioned rain. Verdict: BLOCKED. Rewrite: "for a grey, rainy-day mood", which describes the scene and the mood without promising a sound.

## Transparency about AI involvement

- Describe the real division of work. "Music generated with AI, then selected, edited and mastered by [name]" is honest when that is what happened. "Arranged" is false if the model produced the arrangement.
- Platform disclosure rules are in [social-and-seo.md](social-and-seo.md) and [visual-and-audio.md](visual-and-audio.md).
- Do not hide AI use and do not exaggerate it. Both are accuracy problems.

## What to do when you cannot verify

- Never fill the gap with a plausible detail. Write a simpler sentence that is true.
- Put the open question in the report ("Confirm by listening: is the sax audible at 0:22?") so a person can check it.
- An opinion is allowed when the author's voice calls for one ("my favourite for the first coffee"). A factual claim is not.
