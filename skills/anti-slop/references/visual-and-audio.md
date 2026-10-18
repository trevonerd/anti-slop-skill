# Visual and audio

Thumbnails, frames, Shorts and AI music. None of these signs is proof: real bodies, makeup, editing and compression can imitate all of them [KEL]. Use them to decide what to zoom in on before publishing.

## Contents
- Images and thumbnails
- Video
- Provenance and watermarks
- AI music
- Pre-publish checklist

## Images and thumbnails

Matt Groh's group at Northwestern (Kellogg) sorts visual cues into five families [KEL]:

| Family | What to look for | Reliability | Trend |
|---|---|---|---|
| Anatomy | extra or fused fingers, hands without nails, long necks, overlapping teeth, non-round pupils, glassy or empty eyes [KEL] | medium | fading (TechRadar says Sora 2 "almost solved" hands and blur) [TR] |
| Stylistic "AI gloss" | waxy skin, oversaturated colour, a face that is too perfect, wind-blown hair, cinematic background, face lit differently from the scene [KEL][PS] | medium (many real photos are retouched) | active |
| Functional implausibility | garbled text on signs and shirts, straps melting into clothes, hand inside the sandwich, slack strings, watches that vanish [KEL][PS] | strong for garbled text | fading but still common in backgrounds |
| Physics | shadows in different directions, reflections that do not match, stairs to nowhere, warped perspective [KEL][PS][TR] | medium to strong | active |
| Sociocultural | a scene that is culturally or historically implausible [KEL] | medium | active |

Too-perfect repeated patterns (tiles, facades) and wrong nature (leaves, hands) are also common [PS].

## Video

| Signal | Reliability | Trend |
|---|---|---|
| background that changes, people merging, objects appearing and disappearing, motion that is too smooth, still objects that "breathe", hair and cloth moved by wind that is not there [PS][TR] | medium to strong | active |
| very short cuts or slow motion that hide seams; grain, smudges and melting textures [PS][TR] | medium | active |

## Provenance and watermarks

- A visible watermark (for example Sora's) or C2PA metadata is strong evidence when present. Google's SynthID can be checked by uploading the file to Gemini [TR][SYN].
- **Absence tells you nothing.** Watermarks can be cropped and metadata is lost on export [TR][SYN].
- Never remove watermarks or provenance metadata from your own generated media. That misleads viewers and may break platform terms.

## AI music

The least studied area for human listening; the sources are serious but few.

| Signal | Reliability | Notes |
|---|---|---|
| Phasing | medium | Authors of an ISMIR study report that Suno output "generally suffers from acoustic phasing that is difficult to correct"; Udio has higher fidelity [ISM]. Model- and version-dependent. |
| High-frequency and sampling artefacts | for machines; weak for ears | Detectors seem to exploit signal details, including shortcuts such as sample rate and bitrate (Suno 192 kbps, Udio 320 kbps, both 48 kHz), and degrade with re-encoding, pitch shift or new models [ISM]. |
| Vocals and lyrics | weak to medium | breathless or smeared vocals, odd consonants, "ghost" harmonies, formulaic repeated lyrics (a research summary; not checked word by word against the papers) [ISM][APN] |
| Artist provenance | medium | profile, concerts, label, presence on generation platforms. The Velvet Sundown case (2025) was exposed this way: no concerts, members without social accounts, fake photos [APN][WSL]. |

Context numbers:
- Deezer/Ipsos survey (9,000 people, October 2025): 97% failed to identify all three tracks correctly (two AI, one human). The Verge notes the criterion was "all three right"; in an informal test with the same tracks single tracks were guessed 43% of the time [DZI].
- Deezer: fully AI tracks were over 18% of daily uploads in April 2025 and over 28% in September 2025; since June 2025 Deezer labels them and excludes them from recommendations [DZR].

## Pre-publish checklist

- [ ] Overlay text typed by a person, readable, no typos, never generated inside the image.
- [ ] Hands, cups, instruments (piano keys, sax keys, strings) checked at zoom.
- [ ] Light and shadows consistent; no garbled text in the background.
- [ ] Real places look like themselves, or the image does not claim to be them.
- [ ] Realistic generated imagery disclosed where the platform requires it [YT2].
- [ ] AI music disclosed (on YouTube: music that is the main focus of the video) [YT2][YT5].
- [ ] Copy does not promise sounds or scenes that are absent (see [facts-and-claims.md](facts-and-claims.md)).
