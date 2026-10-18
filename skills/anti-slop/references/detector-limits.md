# Detector limits: why 100% does not exist

Read this before answering "was this written by AI?". The honest answer is almost always "the text shows these patterns; that does not prove who wrote it".

## Contents
- No signal is exclusive to AI
- Signals change with every model
- Humans alone are unreliable
- Automatic detectors are wrong and biased
- Human writing is drifting towards model writing
- Images, video and audio
- What this skill does instead

## No signal is exclusive to AI

Models learn from human text, Wikipedia included [W1]. In Macaron's corpus, 16% of curated human explanatory texts and 8% of real LinkedIn posts contained at least one "AI" word or formula, while only 19-22% of model LinkedIn drafts contained one (28% counting em dashes) [MAC]. Most of the "AI sound" lives in rhythm and in word choice spread over every sentence, not in a list [MAC].

## Signals change with every model

65% of tells are typical of one model family; between two consecutive versions of the same model 55-72% of tells differ [GRA]. Famous tells weaken by 21-50% because vendors correct them, which does not make model writing more human [GRA]. A check built on 2024 lists ("delve", the em dash) misfires today. <!-- slop-scan: ignore-line -->

## Humans alone are unreliable

- A 2025 study cited by Wikipedia found people no better than chance; a study on German theses found 57% recognition for model texts and 64% for human ones [W1].
- Experts do better: five people who often use ChatGPT for writing, voting by majority, misclassified 1 article out of 300 (Russell et al., ACL 2025) [RUS]. In a 2025 preprint, expert annotators found 90% of model texts while misjudging 3.3% of human ones [W1].

## Automatic detectors are wrong and biased

- OpenAI withdrew its classifier on 20 July 2023 "due to its low rate of accuracy": it caught 26% of AI text and flagged 9% of human text as AI; it was unreliable under 1,000 characters and outside English [OAI].
- Weber-Wulff et al. (2023) tested 14 tools including Turnitin: all below 80% accuracy, only 5 above 70%; about 20% of AI texts were attributed to humans; paraphrasing and manual edits made results worse [WW].
- Liang et al. (2023): seven detectors classified on average 61.22% of TOEFL essays by non-native writers as AI, while classifying US students' essays almost perfectly; 97.8% of the TOEFL essays were flagged by at least one detector. Cause: second-language writing is more predictable [LIA]. The English of an Italian, Spanish or German writer can be mistaken for AI.
- Wikipedia: detectors do "better than chance" but with non-trivial error, and suffer from paraphrasing, formatting changes and new models; a high score is not enough to delete a page [W1]. Graphite and Macaron report much better results under some conditions (Macaron: about 90% of model drafts caught with a 1-in-20 threshold) [MAC][GRA], so accuracy depends on genre, length and model. Vendor figures (for example Pangram's 99.98% quoted by The Economist) are commercial claims [ECO].

## Human writing is drifting towards model writing

Wikipedia notes human writing, even in podcasts, moving towards model style, while the reverse does not happen [W1]. Kobak et al. estimate that at least 13.5% of 2024 biomedical abstracts went through an LLM (up to 40% in some subgroups), with a surge of style words such as delves, underscores, showcasing, potential, crucial, intricate, notably, meticulously [KOB]. People who read a lot of model text start writing like it. <!-- slop-scan: ignore-line -->

## Images, video and audio

Watermarks can be removed and metadata gets lost, so absence proves nothing [TR][SYN]. Music detectors partly rely on technical shortcuts and fail on re-encoding and new models [ISM].

## What this skill does instead

It gives verdicts on **quality and compliance**, which can be checked:
- facts verified, no false promises;
- no clusters of signals;
- a series that really varies;
- correct AI disclosure.

Origin cannot be checked with certainty, so the skill never states it. Use wording such as "template-like", "generic", "pattern cluster", never "this was written by AI".
