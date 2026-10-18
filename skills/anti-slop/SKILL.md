---
name: anti-slop
description: Audits and rewrites text so it reads as written by a careful person. AUDIT mode gives an APPROVED or BLOCKED verdict per piece, quoting each flagged phrase with its signal, severity and a ready rewrite. REWRITE mode rewrites drafts while keeping facts, SEO keywords and the author's voice. Catches chatbot residue, invented facts and promises, "not X, it's Y" contrasts, puffery, filler, template series and Markdown leaks in English, Italian, Spanish, French and German, plus checks for YouTube, Shorts, TikTok, Instagram, LinkedIn, thumbnails and AI music disclosure. Use when the user asks to review, check, de-slop, unslop or humanize text, asks whether something "sounds like AI", or before publishing titles, captions, descriptions, posts, emails, newsletters or docs. Judges quality, never authorship.
license: MIT
metadata:
  author: Marco Trevisani
  version: "1.0.0"
---

# Anti-slop

Quality gate for text that people will read. It finds the habits that make writing generic, inflated or false, explains each one with evidence, and fixes it.

## Core rules

1. **Judge the writing and never guess the author.** No person, tool or detector can tell reliably who wrote a text ([references/detector-limits.md](references/detector-limits.md)). Never write "this was written by AI". Write "template-like", "generic", "pattern cluster", "unverified claim".
2. **Count clusters.** One em dash, one list of three or one word from a list proves nothing. Act on clusters (three or more different signals in about 100 words), on repetition across a series, and on fingerprints.
3. **Facts first.** An invented or unverifiable fact, a promise the content cannot keep, or a feature that is not there is always a BLOCKER, however well written the sentence is.
4. **Never add facts while rewriting.** No new number, name, date, quote, place, sound or cause unless it comes from the user or a source you checked. If a sentence needs a detail you do not have, ask for it or write a simpler true sentence.
5. **Respect the author's voice.** Deliberate slang, dialect, catchphrases and fixed format lines agreed by the team are not slop. Keep them at the author's own rate.
6. **Keep what works.** Real search keywords, useful lists, technical terms for technical readers, and plain repetition of the right word all stay.
7. **No detector evasion.** See "What this skill never does" at the end.

## Pick the mode

- AUDIT. The user wants a verdict, a review or a check before publishing. Do not rewrite unless asked; still provide a ready rewrite for every blocked piece.
- REWRITE. The user wants better text. Rewrite, then run the AUDIT checks on your own output before returning it.
- WRITE + GATE. You are writing new copy for the user. Follow [references/human-writing-guide.md](references/human-writing-guide.md), then audit your draft silently and return only the final text plus open questions.

If the request is unclear, default to AUDIT for finished copy and REWRITE for drafts.

## Step 0: gather context

Before judging, collect what you can (ask only for what is missing and matters):

- Platform and field: YouTube title, description, Short caption, overlay, Instagram, TikTok, LinkedIn, email, blog, README.
- Language and register.
- A sample of the author's real writing, and any house rules or slang list.
- Source facts: tracklist, product sheet, brief, the media itself. Without them, mark claims as unverifiable instead of guessing.
- Whether the piece belongs to a series (21 Shorts, a week of posts).
- Required keywords.

## AUDIT workflow

Copy this checklist and tick it as you go:

```
Audit progress:
- [ ] 1. Split into pieces
- [ ] 2. Run the scanner (if a shell is available)
- [ ] 3. Fact pass
- [ ] 4. Pattern pass
- [ ] 5. Series pass
- [ ] 6. Verdict per piece
- [ ] 7. Report
```

**1. Split into pieces.** Each title, description, caption, overlay, hashtag set and tag list is its own piece with its own verdict.

**2. Run the scanner.**

```bash
python3 scripts/slop_scan.py draft.md --lang en,it            # Markdown or text
python3 scripts/slop_scan.py captions.txt --plain --lang en   # platforms that show raw text
python3 scripts/slop_scan.py draft.md --json                  # machine-readable
```

Paths are relative to this skill's folder. The script needs only Python 3.8+. It reports line, column, signal, severity, trend, density per 100 words, paragraph clusters and a verdict hint. The hint is a starting point. A hit is a reason to reread the line, and a clean scan does not mean the text is good: the script cannot see invented facts, generic content or a series built from one template. If no shell is available, do steps 3 to 5 by reading.

**3. Fact pass.** Follow [references/facts-and-claims.md](references/facts-and-claims.md): list every claim, check it against the sources, mark it verified, contradicted or unverifiable. Check timestamps, durations, instruments, sounds, prices, roles, and AI disclosure.

**4. Pattern pass.** Read the piece once for meaning, then look for signals by family. Load only the reference you need:

| Family | Reference |
|---|---|
| English words and phrases | [references/lexicon-en.md](references/lexicon-en.md) |
| Italian | [references/lexicon-it.md](references/lexicon-it.md) |
| Spanish, French, German | [references/lexicon-es-fr-de.md](references/lexicon-es-fr-de.md) |
| Contrast, inflation, rhythm, agency, document shape | [references/structure-and-rhetoric.md](references/structure-and-rhetoric.md) |
| Markdown, dashes, emoji, bold, hidden characters | [references/formatting-and-punctuation.md](references/formatting-and-punctuation.md) |
| Platform rules, series, SEO | [references/social-and-seo.md](references/social-and-seo.md) |
| Thumbnails, video frames, AI music | [references/visual-and-audio.md](references/visual-and-audio.md) |

Also ask the two content questions: Could this piece be pasted under a different product, video or person unchanged? Does it contain at least one specific, true detail?

**5. Series pass.** If pieces belong to a series, put them side by side and count skeletons, CTAs, mood words, lists of three and near-identical overlays ([references/social-and-seo.md](references/social-and-seo.md)). A pattern that repeats through most of a series is a BLOCKER for that element, because platforms treat mass-produced sameness as inauthentic content.

**6. Verdict per piece.** Use the severity table below.

**7. Report.** Use the report format below. Quote exact text. Give every BLOCKED piece a rewrite that can be pasted as is.

### Severity

| Severity | What belongs here | Effect on the verdict |
|---|---|---|
| BLOCKER | fingerprints (chatbot residue, placeholders, citation codes such as `oaicite` or `turn0search0`, `utm_source=chatgpt.com`, hidden characters, visible Markdown on a plain-text platform); invented, contradicted or unverifiable facts; promises; features or sounds that are absent; inflated or hidden AI role; misleading title or thumbnail; tag stuffing in a description; a template repeated across a series | one is enough for BLOCKED |
| MAJOR | strong signals: corrective contrast, legacy puffery, empty openers and prefaces, audience catch-alls, pseudo-agency, clever lines with no fact, rhetorical question with instant answer, viral hook templates, the same CTA twice in one piece | BLOCKED with two MAJOR in one piece, or one MAJOR plus a cluster |
| MINOR | medium signals: formal transitions, intensifiers, bold labels, emoji bullets, one list of three that repeats one idea, unexplained jargon for a general audience | never blocks alone; three or more different ones in about 100 words make a cluster, which counts as MAJOR |
| NOTE | weak signals alone: one famous AI word, one em dash, curly quotes, Title Case, one meme template in a long series | mention only if useful; never blocks |

House rules can promote a signal (for example a creator who bans all "send this to..." CTAs). Say in the report when a verdict comes from a house rule and not from the research.

### Report format

```markdown
# Anti-slop audit: <what was reviewed>
Result: <N> pieces, <B> BLOCKED, <A> APPROVED. Scanner: <density, verdict hint or "not run">.

## Fact check
- <claim>: verified / contradicted / unverifiable (source: <file or evidence>)

## Verdicts
| Piece | Verdict | Reason |
|---|---|---|

## Blocked pieces
### <piece>
- Quote: "<exact text>"
  Signal: <name> (<reference file>), reliability <strong/medium/weak>, trend <active/saturated/fading>
  Severity: <BLOCKER/MAJOR/MINOR>
  Why: <one line>
- Rewrite: <ready text>

## Series patterns
<counts before and after the fixes>

## Open questions
<facts a person must confirm, e.g. "listen at 0:22: is the sax audible?">
```

Keep the report in the user's language; keep quotes and rewrites in the language of the copy.

## REWRITE workflow

```
Rewrite progress:
- [ ] 1. Facts and keywords locked
- [ ] 2. One real detail chosen
- [ ] 3. Rewritten from the point, not patched
- [ ] 4. Voice matched
- [ ] 5. Self-audit passed
```

1. **Lock facts and keywords.** List the facts you may use (from the user, the source files or the original) and the keywords that must stay. Nothing else may enter the text as a fact.
2. **Choose one real detail per piece.** A time, an instrument, a place, a number, a decision. In a series, choose a different one for each piece.
3. **Rewrite from the point.** State what the piece is for in one sentence, then write it the way the author would say it out loud. Swapping flagged words for synonyms keeps the skeleton; change the sentence instead.
4. **Match the voice** with the sample if there is one. Keep slang and fixed lines. Keep the register of the genre.
5. **Self-audit.** Run the scanner on the result, then check by reading:
   - no fact added or dropped compared with step 1 (a cut caveat is a change of meaning);
   - keywords still in the title and first line;
   - no new clusters (rewrites often leave contrasts, closers, triads and bold labels behind);
   - read aloud: would the author say it this way?
   If anything fails, fix that sentence and check again.

Return: the final text, then a short list of what changed and why, then open questions. Do not show intermediate drafts unless asked. For files, edit only prose: leave code, commands, paths, front matter, data and link targets unchanged.

## What not to flag

- Real keywords the audience searches for.
- Plain repetition of the right word.
- Lists and tables that help a reader scan.
- Correct grammar and the subjunctive.
- The author's own slang, dialect, jokes and fixed format lines.
- A single weak signal in otherwise specific, true copy.
- Quoted material, code and examples of bad writing inside a guide (the scanner skips code and supports `<!-- slop-scan: off -->` regions).

## What this skill never does

- Inserting invisible characters, homoglyphs or odd Unicode to fool detectors.
- Running text through paraphrasers built to beat detectors.
- Adding fake typos or fake personal anecdotes to look human.
- Removing watermarks or provenance metadata from generated media.
- Claiming that a text is or is not AI-written.

These tricks hide a problem without solving it, and some of them mislead readers. The only goal here is better, truer writing. If a user asks for detector evasion, say so plainly and offer the REWRITE mode instead.

## Files

- `scripts/slop_scan.py`: the heuristic scanner. Run it; read it only to change the signal list.
- `references/examples.md`: before-and-after cases from real audits, anonymised.
- `references/human-writing-guide.md`: how to write copy that sounds like a person while keeping SEO.
- `references/detector-limits.md`: numbers to quote when someone asks "is this AI?".
- `references/sources.md`: every source, with what was read in full and what only through summaries.
