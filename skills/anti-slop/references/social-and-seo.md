# Social and SEO

Slop on social platforms is mostly a **series** problem and a **policy** problem. One caption can be fine; twenty-one captions built from the same mould put monetisation at risk.

## Contents
- YouTube policy that matters for AI-assisted channels
- Series checks
- Titles, descriptions, captions, overlays
- Platform notes (YouTube, Shorts, TikTok, Instagram, LinkedIn)
- SEO without slop

## YouTube policy that matters for AI-assisted channels

- Inauthentic content. Since July 2025 the old "repetitious content" policy is called "inauthentic content" and explicitly covers repetitive or mass-produced content [YT1]. YouTube excludes from monetisation content that feels made from a template or is "interchangeable from video to video", series with "minimal variation across videos", and AI content made with "generic or unoriginal templates giving the impression of mass production" without the creator's point of view. Reviewers also look at **titles, thumbnails and descriptions** [YT1].
- Spam and deceptive practices. Titles or thumbnails that promise what the video does not deliver are a violation [YT3].
- Tags. YouTube forbids excessive tags in the description; tags play a small role in discovery, while title, thumbnail and description matter more [YT4].
- **Keyword stuffing** is named by YouTube as a sign of low quality (in its guidance on kids' content) [YT1].
- AI disclosure. Creators must disclose realistic altered or synthetic content. YouTube lists "AI generated music" among the cases and asks for disclosure when AI generates "music that's the main focus of the video". Music has Fully / Partly / No Gen AI categories [YT2][YT5]. Disclosure alone does not limit reach or monetisation [YT2].
- Google Search. Generating many pages without added value breaks the "scaled content abuse" policy, whoever or whatever wrote them [GGL][GGS].

Kommers et al. (2026) describe slop with three properties: superficial competence, asymmetric effort (cheap to make, costly to read), and mass producibility [WSL]. The series checks below target the third one.

## Series checks

Run these when a batch of posts belongs to one campaign or channel:

1. Put all pieces side by side in one table (title, caption, overlay, CTA, hashtags).
2. Look for the same skeleton everywhere, for example hook, then three instruments, then CTA.
3. Count each CTA type ("send this", "save this", "where are you listening from?"). One per piece at most; vary it across the series; skip it where it adds nothing.
4. Count mood words and lists of three across the series.
5. Check overlays that differ only by a number.
6. Agreed fixed parts (a standard closing line, `#Shorts`) are a format choice, not slop. Everything else must change for real.

A series fails as a whole (BLOCKED for the repeated element) when the same template or CTA runs through most pieces, even if each piece passes alone.

<!-- slop-scan: off -->
## Titles, descriptions, captions, overlays

| Field | Do | Avoid |
|---|---|---|
| Long-video title | keyword first, then one concrete human detail (place, moment, duration); about 60-70 characters, 100 max | pompous Title Case plus three adjectives plus ✨; "Ultimate", "Perfect", "Best ever" |
| Description | line 1: keywords plus what is really in the video (visible before "more"); lines 2-4: two or three spoken sentences with a production detail or an opinion; verified timestamps; honest AI line | 30 keywords at the bottom (forbidden), promises, "curated, arranged and mastered" when untrue |
| Short / Reel / TikTok caption | one or two sentences, one idea per post, different across the series; 2-3 niche hashtags plus #Shorts on YouTube | the same hook and CTA in every post; hashtag walls |
| Overlay text | few words, readable, typed by a person (never rendered inside a generated image), no typos | clever lines with no fact; "POV: your soul finally breathes" |
| Hook | a time, an action, a sound: "7:30, kettle on" | rhetorical question with instant answer; "Here's the thing" |
<!-- slop-scan: on -->

## Platform notes

- YouTube long form. The first three hashtags in a description show above the title, so three is a sensible maximum. Chapters need the first timestamp at 0:00 and each chapter at least 10 seconds long.
- YouTube Shorts. A plain-text link in a Short's caption is not clickable; use the "related video" field in YouTube Studio to link the full video.
- TikTok and Instagram. The first line (roughly the first 125 characters on Instagram) is all most people see before tapping "more"; one idea and one CTA at most. A common working range is 3-5 niche hashtags on TikTok and 5-12 on Instagram. These are editorial habits [SCR], not platform rules.
- LinkedIn. The densest home of the "isn't just Y, it's Z" contrast, the rhetorical question with instant answer, and one-line paragraphs [MAC][ORI]. Originality.ai estimated 81.2% of long LinkedIn posts as likely AI in July 2026; that figure comes from a detector vendor [ORI]. <!-- slop-scan: ignore-line -->
- Plain-text platforms. Run the scanner with `--plain` so visible Markdown is flagged.

## SEO without slop

- Real search terms are not slop. In a music channel, "smooth jazz", "lofi", "study music", "rainy café" are what people type. Keep them.
- Put keywords in the title and the first line of the description, in a sentence a person would say.
- Keep tags in the tag field: 8-15 specific and true.
- Explain technical terms the audience may not know ("tape saturation" can become "the warm, slightly worn sound of old cassettes"). Genre words the audience knows (Rhodes, walking bass, brushes) can stay.
- Never trade accuracy for a keyword. "Rain sounds" in a title is a false promise if there is no rain in the audio.
