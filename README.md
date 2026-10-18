# anti-slop

An Agent Skill that audits and rewrites text so it reads like a careful person wrote it. It gives a verdict per piece (APPROVED or BLOCKED), quotes the exact phrase, names the signal and its severity, and hands you a rewrite you can paste. It works on English, Italian, Spanish, French and German, and it knows the rules that matter for YouTube, Shorts, TikTok, Instagram and LinkedIn.

It judges **quality, never authorship**. No detector, human or tool can tell reliably who wrote a text, so this skill does not try.

```text
skills/anti-slop/
├── SKILL.md                 # workflow, severity table, report format (loaded when the skill triggers)
├── agents/openai.yaml       # optional display metadata for Codex / ChatGPT
├── scripts/slop_scan.py     # dependency-free scanner (Python 3.8+)
└── references/              # loaded only when needed
    ├── lexicon-en.md  lexicon-it.md  lexicon-es-fr-de.md
    ├── structure-and-rhetoric.md  formatting-and-punctuation.md
    ├── facts-and-claims.md  social-and-seo.md  visual-and-audio.md
    ├── detector-limits.md  human-writing-guide.md
    ├── examples.md  sources.md
```

## What it does

- AUDIT splits copy into pieces (title, description, each caption, overlay, tags), checks facts against your sources, looks for signal clusters and series templates, and returns a report with a verdict per piece, exact quotes, severity and ready rewrites.
- REWRITE rewrites a draft from its point, keeps your facts, keywords and voice, then audits its own output before returning it.
- WRITE + GATE is for copy an agent writes for you: the skill makes the agent check its own draft before you see it.

Rules it follows:
- Clusters count, single hits do not. One em dash or one famous "AI word" is a note, never a block.
- Invented facts, promises and missing features always block.
- Your slang, dialect and fixed format lines are voice, not slop.
- It never adds facts while rewriting.

## Install

The skill follows the open [Agent Skills](https://agentskills.io/specification) format, so the same folder works in every tool below.

**Any agent, one command** (with the [skills CLI](https://github.com/vercel-labs/skills)):

```bash
npx skills add trevonerd/anti-slop-skill            # this project
npx skills add trevonerd/anti-slop-skill -g         # all projects
npx skills add trevonerd/anti-slop-skill -a cursor  # one agent only (claude-code, cursor, codex, ...)
```

**Claude Code** (personal or project):

```bash
git clone https://github.com/trevonerd/anti-slop-skill.git
cp -r anti-slop-skill/skills/anti-slop ~/.claude/skills/        # all projects
# or: cp -r anti-slop-skill/skills/anti-slop .claude/skills/   # this project only
```

As a plugin: `/plugin marketplace add trevonerd/anti-slop-skill`, then `/plugin install anti-slop@anti-slop-skill`.

**Claude.ai and the Claude desktop app**: zip the folder (`cd skills && zip -r anti-slop.zip anti-slop`) and upload it in the Skills section of Settings. Code execution must be on for the scanner to run.

**Cursor**: copy the folder to `~/.cursor/skills/` (global) or `.cursor/skills/` in a repo. Cursor also reads `.agents/skills/`, `.claude/skills/` and `.codex/skills/`.

**Codex (OpenAI)**: copy the folder to `~/.agents/skills/` (user) or `.agents/skills/` at the repo root. `~/.codex/skills/` still works but is the legacy path.

**Any other agent or chat**: paste `SKILL.md` at the start of the conversation, and paste the reference file you need. Without a shell the scanner is skipped and the agent does the checks by reading.

## Use it

Ask in plain words:

- "Audit these 21 Shorts captions before I schedule them. The tracklist is in tracklist.md."
- "Rewrite this YouTube description so it sounds like me. Keep the keywords lofi, smooth jazz, study."
- "Does this LinkedIn post sound like AI?" (you get a list of patterns, not a percentage)
- "Controlla questa caption in italiano, senza toccare lo slang."

Run the scanner yourself:

```bash
python3 skills/anti-slop/scripts/slop_scan.py draft.md
python3 skills/anti-slop/scripts/slop_scan.py captions.txt --plain --lang en,it
python3 skills/anti-slop/scripts/slop_scan.py post.md --json
python3 skills/anti-slop/scripts/slop_scan.py docs/*.md --fail-on cluster   # for CI or a pre-publish hook
```

It finds chatbot residue, placeholders, chatbot citation codes (`oaicite`, `turn0search0`, `[cite: 1]` and others), `utm_source=chatgpt.com`, hidden characters, phrases from the lexicons, "not X, it's Y" contrasts in five languages, lists of three, em-dash density, emoji bullets, bold labels, excess bold, visible Markdown on plain-text platforms, hashtag walls, rhetorical questions with instant answers, staccato fragments and metronome rhythm. It reports line and column, density per 100 words, paragraph clusters and a verdict hint. It skips front matter, code and anything between `<!-- slop-scan: off -->` and `<!-- slop-scan: on -->`.

A scanner hit is a reason to reread a line. A clean scan proves nothing: the script cannot see invented facts, generic content or a series built from one template. That is the agent's job in the AUDIT workflow.

## What it will not do

No detector evasion. The skill does not insert invisible characters or homoglyphs, does not use paraphrasers built to beat detectors, does not add fake typos or fake anecdotes, and does not remove watermarks or provenance metadata. These tricks hide a problem without fixing it and can mislead readers. The scanner flags hidden characters so you can delete them.

## How it compares

Honest notes on the skills that already exist (October 2026). Several are very good, and this one borrows ideas from them with credit.

| Skill | Strengths | Gaps this skill tries to fill |
|---|---|---|
| [blader/humanizer](https://github.com/blader/humanizer) (MIT, very popular) | clear rewrite workflow, patterns ranked by strength, strong rule against adding facts, voice matching from a sample | English only; rewrite-first, no per-piece verdict report; no scanner; no platform policy or series checks |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) (MIT) | short and easy to load; phrase and structure references | very strict rules (no adverbs, no passive, no em dashes) that can flatten a real voice; no fact checks; no scanner |
| [crypdick/unslop](https://github.com/crypdick/unslop) (no license file) | careful about meaning and voice; regex detector for directories and CI; eval corpus | English only; no social or policy layer; no license, so it can be read and cited but not reused |
| [misbahsy/anti-ai-slop](https://github.com/misbahsy/anti-ai-slop) (MIT) | multi-gate pipeline: hidden-character cleanup, linter, second-agent review, optional second model | assumes the draft is model-written and "cuts hard" by default; optional gate needs an API key and LiteLLM |
| [manavmishra/ZeroSlop](https://github.com/manavmishra/ZeroSlop) (MIT) | checks that core details survive the edit; benchmarks and examples | hosted MCP and optional metadata request; English focus |
| [jalaalrd/anti-ai-slop-writing](https://github.com/jalaalrd/anti-ai-slop-writing) (no license detected) | broad banned lists, works as a pasted system prompt | ban lists treat single words as proof, which the research no longer supports |

What this skill adds:
- An audit mode with verdicts: APPROVED or BLOCKED per piece, exact quote, signal, severity, ready rewrite. Built from a real pre-publish review process.
- Facts as the first gate. Invented sounds, inflated roles, false promises and unverifiable claims block even when the prose is fine.
- Reliability and trend on every signal (strong, medium, weak; active, saturated, fading, historical), with sources, because model tells change with each release.
- Italian in depth, plus Spanish, French and German lists marked as lower confidence.
- A platform and series layer: YouTube inauthentic-content policy, tag rules, AI music disclosure, CTA and template counts across a batch of posts.
- Visual and audio checks for thumbnails, frames and AI music, with clear limits.
- Honest limits. Detector error rates with numbers, so the agent answers "is this AI?" truthfully.
- A scanner with zero dependencies, tests, and five evaluation scenarios in `evals/`.

What it does not do better: it has no second-model review gate (misbahsy does), no hosted editor (ZeroSlop does), and its Spanish, French and German lists are shorter than those of dedicated single-language skills such as [stop-slop-spanish](https://github.com/sohantanna/stop-slop-spanish).

## Tests

```bash
python3 -m unittest discover -s tests -v
```

`evals/evals.json` holds five scenarios in the format suggested by Anthropic's skill authoring guide: an audit with false claims, a rewrite that must keep keywords, a series audit with slang to preserve, an "is this AI?" question, and a detector-evasion request that must be refused.

## Credits and sources

The research behind the signal lists comes mainly from Wikipedia's "Signs of AI writing" guide and its editors, Graphite's "AI Tells", Macaron's counted corpus, Sloptells, Pangram, humanizer-it, Treccani's work on "IA-taliano", the detector studies by OpenAI, Weber-Wulff et al., Liang et al., Russell et al. and Kobak et al., YouTube and Google policy pages, and the existing skills listed above. Every source is in [skills/anti-slop/references/sources.md](skills/anti-slop/references/sources.md), split into what was read in full and what was read through summaries. All text is written fresh; nothing was copied from repositories without a license.

## License

MIT. See [LICENSE](LICENSE).
