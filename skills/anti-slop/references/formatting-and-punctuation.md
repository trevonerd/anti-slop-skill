# Formatting and punctuation

Labels as in [lexicon-en.md](lexicon-en.md). Formatting depends on the platform: Markdown that renders in a README shows up as raw asterisks in a YouTube description.

<!-- slop-scan: off -->
| Signal | Examples | Reliability | Trend |
|---|---|---|---|
| Visible Markdown on a plain-text platform | `**bold**` with asterisks in a YouTube caption, `##` in a description [W1][PAN] | strong (fingerprint) when the symbols show | active (bold at 43x the human rate per Pangram) [PAN] |
| Em dash (—) | Macaron: 10-15x in model LinkedIn posts [MAC]; Pangram: 9x and 7x for two families, 0.7x for a third [PAN]; Graphite 2026: one family uses it at 1/8 of the human rate, one at the human rate, one almost never [GRA]; The Economist (July 2026): only one family above humans [ECO] | model-dependent | fading and split by model. In Italian, Spanish and French the spaced dash is rarer, so it stays more suspicious [HUM][PRO] |
| Punctuation that is too poor | almost no semicolons, brackets or exclamation marks; long sentences glued with "and" [SLO][ECO][GRA]; since September 2026 some models dropped dashes and punctuation variety fell [W1] | medium | new, growing |
| Bold everywhere | [W1][SLO][PAN] | strong in prose | active |
| Bold label lists | "**Mood:** cozy..." [W1][UNS] | medium to strong | active |
| Bullets for a conversation | [SLO][PAN] (9x and 7.9x) | medium | active |
| Headers inside a social post | [SLO] | strong | active |
| Emoji as structure | ✅ (167x), 1️⃣2️⃣3️⃣, 🚀 (26x), ⚠️ at the start of list items [PAN][W1] | strong for these emoji; faces such as 😊 ❤️ read as more human [PAN] | fading in prose, still common in social |
| Unusual Unicode symbols | ─ (940x), ≈ (241x), → (48x) [PAN] | medium | active |
| Title Case on every heading | "Perfect Morning Jazz For Focus" [W1][UNS] | weak on YouTube, where many channels use it | active |
| Curly quotes “ ” | [W1][SLO] | weak (Word and macOS insert them; some models never do) | fading |
| `---` separators between sections | [W1] | medium | active |
| Pointless small tables | [W1] | medium | active |
| Hidden characters | zero-width spaces, bidi controls, tag characters pasted along with chatbot output [MSB] | strong when present | active |
| Hashtag walls | 15+ hashtags under a caption | medium; on YouTube, see the tag rules in [social-and-seo.md](social-and-seo.md) | active |
<!-- slop-scan: on -->

## Rules of thumb

- Prose for people: sentences, not bullets, unless the reader will scan a list.
- Emoji: at most one per title, and only if it adds information or tone the author would use.
- Removing every dash has itself become a pattern [W1][ECO]. Use one where it helps; do not use one per sentence.
- Hidden characters: delete them. Never add them (see "What this skill never does" in SKILL.md).
