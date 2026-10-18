#!/usr/bin/env python3
"""slop_scan.py: heuristic scanner for AI-slop signals in text and Markdown.

Standard library only, Python 3.8+.

It finds candidate signals and reports where they are and how dense they are.
It does NOT decide whether a human or a model wrote the text. No tool can do
that reliably (see references/detector-limits.md). Treat every hit as a reason
to reread the line, then judge it with the AUDIT workflow in SKILL.md.

Usage:
    python3 slop_scan.py FILE [FILE ...]
    cat draft.txt | python3 slop_scan.py -
    python3 slop_scan.py caption.txt --plain --lang en,it --json

Exit codes:
    0  scan finished (and --fail-on threshold not reached)
    1  --fail-on threshold reached
    2  usage or input error

Markers you can put in a file:
    <!-- slop-scan: off --> ... <!-- slop-scan: on -->   skip a region
    any line containing "slop-scan: ignore-line"         skip that line
"""

import argparse
import json
import re
import statistics
import sys
import unicodedata

# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------
# Points per hit, by severity. The numbers encode the density rule from
# SKILL.md: a weak word alone (1 point) never reaches the REVIEW line, while
# three or four different medium/strong signals in about 100 words do.
WEIGHTS = {"fingerprint": 10, "strong": 3, "medium": 2, "weak": 1}

# Density is points per 100 words. Captions are often 10-20 words, and one weak
# hit there would read as 5-10 points per 100 words. Dividing by at least 50
# words keeps a single isolated hit in a short caption below REVIEW.
MIN_WORDS_FOR_DENSITY = 50

# Verdict hint thresholds in points per 100 words. Derived from the working rule
# "fewer than 2-3 medium signals per 100 words, never clustered" (SKILL.md).
REVIEW_DENSITY = 3.0
CLUSTER_DENSITY = 6.0

# A paragraph is a cluster when it has at least this many distinct signals,
# this many points, and a local density of at least CLUSTER_DENSITY. Three different signals in one paragraph is the point where
# the sources stop calling it coincidence (Wikipedia, Macaron, unslop).
CLUSTER_MIN_DISTINCT = 3
CLUSTER_MIN_POINTS = 6

# Sentence-length uniformity: only measured with enough sentences to be
# meaningful. The coefficient of variation threshold is a conservative
# heuristic chosen for this tool, not a published number.
UNIFORMITY_MIN_SENTENCES = 8
UNIFORMITY_MAX_CV = 0.25

# ---------------------------------------------------------------------------
# Signal catalog
# ---------------------------------------------------------------------------
# Each entry: (id, lang, category, severity, trend, regex)
# lang: "any", "en", "it", "es", "fr", "de"
# severity: fingerprint | strong | medium | weak  (also used as reliability)
# trend: active | saturated | fading | historical | model-dependent

F = re.IGNORECASE

SIGNALS = [
    # --- Fingerprints: chatbot residue -----------------------------------
    ("chatbot-residue", "en", "fingerprint", "fingerprint", "active",
     r"\bhere(?:'s| is) (?:your|the|a) (?:revised |updated |final |new )?"
     r"(?:caption|post|draft|version|description|title|rewrite|email|tweet|thread)s?\b\s*:"),
    ("chatbot-residue", "en", "fingerprint", "fingerprint", "active",
     r"\bI hope (?:this|that) helps\b"),
    ("chatbot-residue", "en", "fingerprint", "fingerprint", "active",
     r"\bwould you like me to\b"),
    ("chatbot-residue", "en", "fingerprint", "fingerprint", "active",
     r"\blet me know if you(?:'d| would)? (?:like|want|need) (?:me to|any|more)\b"),
    ("ai-disclaimer", "en", "fingerprint", "fingerprint", "historical",
     r"\bas an AI(?: language)? model\b"),
    ("ai-disclaimer", "en", "fingerprint", "fingerprint", "historical",
     r"\bas of my (?:last )?(?:knowledge )?(?:update|cutoff|training)\b"),
    ("chatbot-residue", "it", "fingerprint", "fingerprint", "active",
     r"\bcerto!\s*ecco\b"),
    ("chatbot-residue", "it", "fingerprint", "fingerprint", "active",
     r"\becco (?:la tua|il tuo|una|un|le tue|i tuoi) (?:nuova |nuovo )?"
     r"(?:caption|post|bozza|versione|descrizione|titolo|testo)\w*\s*:"),
    ("chatbot-residue", "it", "fingerprint", "fingerprint", "active",
     r"\bspero che (?:questo|ti) (?:ti )?(?:sia (?:utile|d'aiuto)|aiuti)\b"),
    ("chatbot-residue", "it", "fingerprint", "fingerprint", "active",
     r"\bfammi sapere se (?:vuoi|hai bisogno|desideri)\b"),
    ("ai-disclaimer", "it", "fingerprint", "fingerprint", "historical",
     r"\bin quanto (?:modello (?:di )?linguistico|intelligenza artificiale)\b"),
    ("chatbot-residue", "es", "fingerprint", "fingerprint", "active",
     r"\bespero que (?:esto )?te (?:sea (?:útil|de ayuda)|ayude)\b"),
    ("chatbot-residue", "es", "fingerprint", "fingerprint", "active",
     r"¡claro(?: que sí)?! aquí\b"),
    ("chatbot-residue", "fr", "fingerprint", "fingerprint", "active",
     r"\bj'espère que (?:cela|ça) (?:t'|vous )?aide\b"),
    ("chatbot-residue", "de", "fingerprint", "fingerprint", "active",
     r"\bich hoffe,? (?:das|dies) hilft\b"),
    ("ai-disclaimer", "any", "fingerprint", "fingerprint", "historical",
     r"\b(?:como modelo de lenguaje|en tant que modèle de langage|als KI-Sprachmodell)\b"),

    # --- Fingerprints: placeholders --------------------------------------
    ("placeholder", "any", "fingerprint", "fingerprint", "active",
     r"\[(?:your|insert|add|enter|nome|inserisci|tuo|tua|tu|votre|ihr|link)\b[^\]\n]{0,40}\]"),
    ("placeholder", "any", "fingerprint", "fingerprint", "active",
     r"\b(?:19|20)\d\d-XX-XX\b"),
    ("placeholder", "any", "fingerprint", "fingerprint", "active",
     r"\((?:add|insert|inserisci|aggiungi) [^)\n]{1,50} (?:here|qui)\)"),

    # --- Fingerprints: chatbot citation codes -----------------------------
    ("citation-code", "any", "fingerprint", "fingerprint", "active",
     r":?contentReference\[oaicite:\d+\](?:\{index=\d+\})?"),
    ("citation-code", "any", "fingerprint", "fingerprint", "active", r"\boaicite\b"),
    ("citation-code", "any", "fingerprint", "fingerprint", "active", r"\boai_citation\b"),
    ("citation-code", "any", "fingerprint", "fingerprint", "active",
     r"\bturn\d+(?:search|view|news|fetch|image)\d+\b"),
    ("citation-code", "any", "fingerprint", "fingerprint", "active",
     r"\[cite:\s*\d+(?:\s*,\s*\d+)*\]"),
    ("citation-code", "any", "fingerprint", "fingerprint", "active",
     r"\[span_\d+\]\((?:start|end)_span\)"),
    ("citation-code", "any", "fingerprint", "fingerprint", "active", r"\bgrok_card\b"),
    ("citation-code", "any", "fingerprint", "fingerprint", "active", r"【\d+†[^】\n]*】"),
    ("citation-code", "any", "fingerprint", "fingerprint", "active", r"\[attached_file:\d+\]"),
    ("citation-code", "any", "fingerprint", "fingerprint", "active", r":::writing\{"),

    # --- Fingerprints: link parameters (passed through a chatbot) -------
    ("chatbot-link-param", "any", "fingerprint", "fingerprint", "active",
     r"\butm_source=(?:chatgpt\.com|openai|copilot\.com|perplexity(?:\.ai)?|gemini)\b"),
    ("chatbot-link-param", "any", "fingerprint", "fingerprint", "active",
     r"\breferrer=grok\.com\b"),

    # --- Facts and promises (always need verification) -----------------
    ("unverifiable-promise", "en", "facts", "strong", "active",
     r"\binstant (?:calm|focus|relief|relaxation|sleep)\b"),
    ("unverifiable-promise", "en", "facts", "strong", "active",
     r"\b(?:guaranteed|scientifically proven|clinically proven)\b"),
    ("unverifiable-promise", "any", "facts", "strong", "active",
     r"\b100\s?% (?:relax|relaxing|calm|guaranteed|natural|human|focus)\b"),
    ("unverifiable-promise", "en", "facts", "strong", "active", r"\bno ads\b"),
    ("unverifiable-promise", "it", "facts", "strong", "active",
     r"\b(?:scientificamente provat[oaie]|garantit[oaie]|relax immediato|ti farà dormire)\b"),
    ("vague-attribution", "en", "facts", "medium", "active",
     r"\b(?:experts (?:say|agree|believe|suggest)|studies (?:show|suggest|have shown)|"
     r"research (?:shows|suggests)|industry reports|many believe)\b"),
    ("vague-attribution", "it", "facts", "medium", "active",
     r"\b(?:gli esperti (?:dicono|sostengono|concordano)|(?:gli |diversi |molti )?studi "
     r"(?:dimostrano|mostrano)|è dimostrato che|secondo molti|molti ritengono)\b"),
    ("vague-attribution", "es", "facts", "medium", "active",
     r"\b(?:los expertos (?:dicen|sostienen|coinciden)|(?:los )?estudios (?:muestran|demuestran))\b"),
    ("vague-attribution", "fr", "facts", "medium", "active",
     r"\b(?:les experts (?:disent|s'accordent)|les études montrent)\b"),
    ("vague-attribution", "de", "facts", "medium", "active",
     r"\b(?:Experten (?:sagen|sind sich einig)|Studien (?:zeigen|belegen))\b"),
    ("source-disclaimer", "en", "facts", "strong", "active",
     r"\b(?:while specific details are (?:limited|scarce)|not widely documented|"
     r"limited information is available)\b"),
    ("media-coverage-puffery", "en", "facts", "strong", "active",
     r"\b(?:featured in (?:leading|major|prominent) (?:outlets|publications)|"
     r"(?:maintains|has) an active (?:social media )?presence)\b"),

    # --- Corrective contrast ("not X, it's Y") --------------------------
    ("contrast-not-just", "en", "structure", "strong", "active",
     r"\b(?:it'?s|this is|that'?s|is|are|was|were)\s+not\s+(?:just|only|simply|merely)\b"),
    ("contrast-not-just", "en", "structure", "strong", "active",
     r"\b(?:isn'?t|aren'?t|wasn'?t)\s+(?:just|only|simply|merely)\b"),
    ("contrast-not-just", "en", "structure", "strong", "active",
     r"(?:^|[.!?]\s+)not\s+(?:just|only|simply|merely)\s+[^.!?\n]{1,60}?[,;:\u2014\u2013]\s*(?:it'?s|but|it is)\b"),
    ("contrast-its-not", "en", "structure", "strong", "saturated",
     r"\b(?:it'?s|this is|that'?s) not (?:about )?[^.!?\n]{1,40}?[,;.:\u2014\u2013]\s*(?:it'?s|this is|that'?s) "),
    ("contrast-not-because", "en", "structure", "strong", "active",
     r"\bnot because\b[^.!?\n]{1,60}[.!?,]\s*because\b"),
    ("contrast-less-more", "en", "structure", "strong", "active",
     r"\bless like (?:a |an |the )?[^.!?\n]{1,30}? and more like\b"),
    ("contrast-less-more", "en", "structure", "medium", "active",
     r"(?:^|[.!?]\s+)less \w+(?: \w+)?[,.] more \w+"),
    ("contrast-rather-than", "en", "structure", "weak", "active", r"\brather than\b"),
    ("contrast-non-solo", "it", "structure", "strong", "active",
     r"\bnon solo\b[^.!?\n]{1,80}?\bma anche\b"),
    ("contrast-non-e", "it", "structure", "strong", "active",
     r"\bnon (?:è|si tratta di) (?:solo |soltanto |semplicemente )?[^.!?\n]{1,50}?"
     r"[,;.:\u2014\u2013]\s*(?:è|ma|si tratta)\b"),
    ("contrast-no-solo", "es", "structure", "strong", "active",
     r"\bno solo\b[^.!?\n]{1,80}?\bsino\b"),
    ("contrast-no-es", "es", "structure", "strong", "active",
     r"\bno (?:es|se trata de) (?:solo )?[^.!?\n]{1,40}?[,;.]\s*(?:es|sino|se trata)\b"),
    ("contrast-non-seulement", "fr", "structure", "strong", "active",
     r"\bnon seulement\b[^.!?\n]{1,80}?\bmais\b"),
    ("contrast-ce-nest-pas", "fr", "structure", "strong", "active",
     r"\bce n'est pas (?:seulement |juste |simplement )?[^.!?\n]{1,40}?[,;.]\s*c'est\b"),
    ("contrast-loin-detre", "fr", "structure", "medium", "active", r"\bloin d'être\b"),
    ("contrast-nicht-nur", "de", "structure", "strong", "active",
     r"\bnicht nur\b[^.!?\n]{1,80}?\bsondern\b"),

    # --- Other structure and rhetoric -----------------------------------
    ("signals-importance", "en", "structure", "strong", "active",
     r"\b(?:matters because|this (?:distinction|difference) matters|what (?:really )?matters (?:most )?is)\b"),
    ("legacy-puffery", "en", "structure", "strong", "active",
     r"\b(?:(?:a|an) (?:enduring |lasting )?testament to|stands as (?:a|an)|serves as (?:a|an)|"
     r"plays? (?:a|an) (?:pivotal|crucial|vital|key|significant) role|"
     r"(?:a|an) pivotal moment|marks (?:a|an) (?:significant |pivotal )?shift|"
     r"reflects broader|setting the stage for|leaves? (?:a|an) (?:lasting|indelible) (?:mark|impact))\b"),
    ("free-benefit", "en", "structure", "medium", "active",
     r"\bwithout (?:sacrificing|compromising|losing|requiring)\b"),
    ("false-range", "en", "structure", "medium", "active",
     r"\bfrom (?:\w+ ){1,3}to (?:\w+ ){0,2}\w+, (?:this|it|these|our)\b"),
    ("whether-youre", "en", "structure", "strong", "saturated",
     r"\bwhether you(?:'re| are) [^.!?\n]{1,40}? or\b"),
    ("che-tu-stia", "it", "structure", "strong", "saturated",
     r"\bche tu (?:stia|sia) [^.!?\n]{1,40}? o\b"),
    ("pseudo-agency", "en", "structure", "medium", "active",
     r"\b(?:the|this|that|my|your|our) (?:beat|piano|music|song|track|melody|sax|guitar|playlist|"
     r"mix|rhodes|trumpet|data|code|rain) (?:knows|understands|feels|remembers|wants|whispers|"
     r"tells us|gets you|knows it)\b"),
    ("pseudo-agency", "it", "structure", "medium", "active",
     r"\b(?:il|questo|quel) (?:beat|piano|brano|sax|disco|mix) (?:sa|capisce|ricorda|sussurra)\b"),
    ("self-care-cliche", "en", "lexicon", "medium", "active",
     r"\byou (?:actually|really|truly) (?:deserve|need)\b"),

    # --- Openers, closers, filler (by language) --------------------------
    ("empty-opener", "en", "lexicon", "strong", "saturated",
     r"\bin today'?s (?:fast-paced|digital|ever-changing|modern|busy|hectic) world\b"),
    ("empty-opener", "en", "lexicon", "strong", "saturated",
     r"\bin the (?:ever-evolving|rapidly evolving|ever-changing) (?:world|landscape) of\b"),
    ("importance-preface", "en", "lexicon", "strong", "saturated",
     r"\b(?:it'?s|it is) (?:worth noting|important to note|worth mentioning|crucial to note)\b"),
    ("importance-preface", "en", "lexicon", "medium", "active", r"\bworth noting\b"),
    ("announced-closer", "en", "lexicon", "medium", "saturated",
     r"(?:^|[.!?]\s+)(?:in conclusion|in summary|to sum up|ultimately|all in all),"),
    ("formal-transition", "en", "lexicon", "medium", "active",
     r"(?:^|[.!?]\s+)(?:moreover|furthermore|additionally),"),
    ("travel-brochure", "en", "lexicon", "strong", "active",
     r"\b(?:nestled (?:in|among|between)|in the heart of|rich (?:cultural )?heritage|"
     r"diverse array of|natural beauty)\b"),
    ("marketing-cliche", "en", "lexicon", "strong", "saturated",
     r"\b(?:look no further|perfect for any occasion|embark on (?:a|your) journey|"
     r"immerse yourself|unlock the (?:power|potential|secrets?)|elevate your|"
     r"take (?:it|your \w+) to the next level|game[- ]chang(?:er|ing))\b"),
    ("announcement-cliche", "en", "lexicon", "strong", "saturated",
     r"\b(?:thrilled|excited|humbled|proud) to (?:announce|share)\b"),
    ("viral-hook", "en", "lexicon", "medium", "saturated",
     r"\b(?:here'?s the (?:thing|kicker|truth)|let that sink in|read that again|"
     r"no fluff|you'?re not alone|and honestly\?)"),
    ("ritual-cta", "en", "lexicon", "medium", "active",
     r"\b(?:curious what others think|let me know in the comments|drop a comment below|"
     r"smash that like)\b"),
    ("review-formula", "en", "lexicon", "medium", "active",
     r"\bI recently had the pleasure of\b"),
    ("the-real-question", "en", "lexicon", "medium", "active",
     r"\bthe real question is\b"),
    ("sincerity-adverb", "en", "lexicon", "medium", "active", r"\bgenuinely\b"),
    ("the-actual-x", "en", "lexicon", "weak", "active", r"\bthe actual \w+"),
    ("ai-word", "en", "lexicon", "weak", "historical",
     r"\b(?:delv(?:e|es|ed|ing)|tapestry|testament|realm|beacon)\b"),
    ("ai-word", "en", "lexicon", "weak", "fading",
     r"\b(?:vibrant|pivotal|crucial|intricate|meticulous(?:ly)?|underscor(?:e|es|ed|ing)|"
     r"bolster(?:s|ed)?|garner(?:s|ed)?|interplay|enduring)\b"),
    ("ai-word", "en", "lexicon", "weak", "active",
     r"\b(?:showcas(?:e|es|ed|ing)|highlighting|emphasizing|foster(?:s|ed|ing)?|enhanc(?:e|es|ed|ing)|"
     r"leverag(?:e|es|ed|ing)|seamless(?:ly)?|robust|utiliz(?:e|es|ed|ing)|multifaceted|"
     r"boasts|dependable|meaningful|transformative|groundbreaking|revolutionary|"
     r"unprecedented|invaluable|indelible|incredibly|remarkably|profound)\b"),

    ("empty-opener", "it", "lexicon", "strong", "saturated",
     r"\bnel mondo (?:frenetico |moderno |digitale )?(?:di oggi|d'oggi)\b"),
    ("empty-opener", "it", "lexicon", "strong", "saturated",
     r"\b(?:nell'era digitale|in un contesto sempre più|in un mondo in continua evoluzione)\b"),
    ("importance-preface", "it", "lexicon", "strong", "saturated",
     r"\b(?:è importante (?:notare|sottolineare|ricordare)|vale la pena (?:sottolineare|notare|ricordare)|"
     r"è fondamentale sottolineare|va sottolineato che)\b"),
    ("announced-closer", "it", "lexicon", "medium", "saturated",
     r"(?:^|[.!?]\s+)(?:in conclusione|in sintesi|riassumendo|in definitiva|in breve),?"),
    ("template-opener", "it", "lexicon", "strong", "saturated",
     r"\b(?:diamo un'occhiata|scopri il potere|non perdere|ecco cosa devi sapere|"
     r"unisciti a me|preparati a|immergiamoci|approfondiamo)\b"),
    ("mood-cliche", "it", "lexicon", "strong", "saturated",
     r"\b(?:immergiti|lasciati trasportare|un viaggio (?:sonoro|musicale|emozionale)|"
     r"un'esperienza (?:unica|indimenticabile)|atmosfera (?:magica|avvolgente)|"
     r"una coccola per le orecchie|la colonna sonora perfetta|perfett[oa] per ogni (?:momento|occasione)|"
     r"ideale per ogni occasione|note che raccontano storie|emozioni pure)\b"),
    ("escalation", "it", "lexicon", "strong", "saturated",
     r"\b(?:e non finisce qui|ma c'è di più)\b"),
    ("marketing-cliche", "it", "lexicon", "medium", "active",
     r"\b(?:il futuro è qui|al (?:prossimo|livello successivo)|portare al livello successivo|"
     r"sfruttare (?:il|tutto il) (?:pieno )?potenziale|aprire nuovi orizzonti|a 360 gradi|game changer)\b"),
    ("journey-closer", "it", "lexicon", "strong", "saturated",
     r"\b(?:oggi chiudo un capitolo|il viaggio continua|da qui riparto)\b"),
    ("ai-word", "it", "lexicon", "weak", "active",
     r"\b(?:approfondire|panorama|cruciale|arazzo|sinfonia|intricato|avvincente|"
     r"testimonianza di|innovativ[oaie]|rivoluzionari[oaie]|sorprendentemente|significativamente)\b"),

    ("empty-opener", "es", "lexicon", "strong", "saturated",
     r"\b(?:en el mundo actual|en la era digital|en un mundo cada vez más)\b"),
    ("importance-preface", "es", "lexicon", "strong", "saturated",
     r"\b(?:cabe destacar(?: que)?|es importante (?:señalar|destacar|mencionar)|vale la pena mencionar)\b"),
    ("legacy-puffery", "es", "lexicon", "medium", "active",
     r"\b(?:juega un papel (?:fundamental|clave|crucial)|sin lugar a dudas|un amplio abanico de)\b"),
    ("announced-closer", "es", "lexicon", "medium", "saturated",
     r"(?:^|[.!?]\s+)(?:en definitiva|en resumen|en conclusión),?"),
    ("ai-word", "es", "lexicon", "weak", "active",
     r"\b(?:vibrante|crucial|robusto|panorama|ecosistema|potenciar|sumérgete|desbloquear)\b"),

    ("empty-opener", "fr", "lexicon", "strong", "saturated",
     r"\b(?:dans un monde en constante évolution|à l'ère du numérique|depuis la nuit des temps)\b"),
    ("importance-preface", "fr", "lexicon", "strong", "saturated",
     r"\b(?:il est important de noter|il convient de souligner|force est de constater)\b"),
    ("announced-closer", "fr", "lexicon", "medium", "saturated",
     r"(?:^|[.!?]\s+)(?:en somme|en conclusion|en définitive),?"),
    ("ai-word", "fr", "lexicon", "weak", "active",
     r"\b(?:incontournable|enjeu majeur|levier|plonger au cœur de|naviguer dans)\b"),

    ("empty-opener", "de", "lexicon", "strong", "saturated",
     r"\bin der heutigen (?:schnelllebigen|digitalen) Welt\b"),
    ("importance-preface", "de", "lexicon", "strong", "saturated",
     r"\b(?:es ist wichtig zu beachten|zusammenfassend lässt sich sagen)\b"),
    ("formal-transition", "de", "lexicon", "medium", "active",
     r"(?:^|[.!?]\s+)(?:darüber hinaus|nichtsdestotrotz|folglich),?"),
    ("ai-word", "de", "lexicon", "weak", "active",
     r"\b(?:vielfältig|entscheidend|nahtlos|ganzheitlich)\b"),
]

EMOJI_BULLET = re.compile(
    r"^[ \t]*(?:[-*\u2022][ \t]*)?(?:\u2705|\u274c|\U0001F680|\u26a0\ufe0f?|\U0001F449|\U0001F525|"
    r"\U0001F4A1|\U0001F4CC|\u2728|\U0001F3AF|[1-9]\ufe0f?\u20e3|\u27a1\ufe0f?|\u2714\ufe0f?|\u2b50)",
    re.MULTILINE,
)
BOLD_LABEL = re.compile(r"^[ \t]*(?:[-*\u2022]|\d+\.)[ \t]+\*\*[^*\n]{1,40}?(?::\*\*|\*\*:)", re.MULTILINE)
BOLD_SPAN = re.compile(r"\*\*[^*\n]+?\*\*|__[^_\n]+?__")
MD_HEADER = re.compile(r"^[ \t]{0,3}#{1,6}[ \t]+\S", re.MULTILINE)
HASHTAG = re.compile(r"(?<![\w&])#[^\s#.,;:!?]{2,}")
EM_DASH = re.compile("\u2014|(?<= )\u2013(?= )")
ODD_SYMBOL = re.compile("[\u2192\u2248\u2500\u21d2]")
TRIAD = re.compile(
    r"\b([A-Za-zÀ-ÿ'-]{3,}), ([A-Za-zÀ-ÿ'-]{3,}),? (?:and|or|e|o|y|et|und) ([A-Za-zÀ-ÿ'-]{3,})\b"
)
# "The result? A calmer morning." The tell is a verbless noun-phrase question
# answered at once. Real engagement questions ("What's for breakfast?") have a
# verb and are not answered, so they are not matched.
SHORT_QA = re.compile(
    r"(?:^|(?<=[.!?])[ \t]+)((?:(?:the|my|our|your|its|il|la|lo|le|el|los|las|der|die|das)[ \t]+"
    r"[A-Za-zÀ-ÿ']+(?:[ \t][A-Za-zÀ-ÿ']+)?|why|how|perché|result|risultato|answer|lesson|twist)\?)"
    r"[ \t]+(?=[A-ZÀ-Ý0-9])",
    re.MULTILINE | re.IGNORECASE)
# Zero-width and bidi control characters. ZWJ (U+200D) and VS16 are normal inside
# emoji sequences, so ZWJ is only reported between two letters or digits.
INVISIBLE = re.compile("[\u200b\u200c\u2060\ufeff\u00ad\u202a-\u202e\u2066-\u2069\U000E0000-\U000E007F]"
                       "|(?<=\\w)\u200d(?=\\w)")
URL = re.compile(r"https?://\S+|www\.\S+")
WORD = re.compile(r"[A-Za-zÀ-ÿ0-9']+")

_COMPILED = [(sid, lang, cat, sev, trend, re.compile(rx, F | re.MULTILINE))
             for sid, lang, cat, sev, trend, rx in SIGNALS]


# ---------------------------------------------------------------------------
# Text preparation
# ---------------------------------------------------------------------------
def _blank(text, start, end):
    """Replace text[start:end] with spaces, keeping newlines so offsets and
    line numbers stay valid."""
    chunk = text[start:end]
    return text[:start] + re.sub(r"[^\n]", " ", chunk) + text[end:]


def mask_regions(text, skip_quotes=False):
    """Return (structural_mask, prose_mask).

    structural_mask hides front matter, fenced code, inline code, ignored
    regions and ignored lines. It is used for fingerprints and link
    parameters, so a guide that documents `oaicite` in backticks is not
    flagged while a leaked code in prose is.
    prose_mask additionally hides URLs, so words inside a URL do not count
    as prose.
    """
    out = text
    fm = re.match(r"\A---\n.*?\n---[ \t]*\n", out, re.DOTALL)
    if fm:
        out = _blank(out, 0, fm.end())
    for m in list(re.finditer(r"<!--\s*slop-scan:\s*off\s*-->.*?(?:<!--\s*slop-scan:\s*on\s*-->|\Z)",
                              out, re.DOTALL | re.IGNORECASE)):
        out = _blank(out, m.start(), m.end())
    for m in list(re.finditer(r"^[ \t]*(```|~~~).*?^[ \t]*\1[^\n]*$", out, re.DOTALL | re.MULTILINE)):
        out = _blank(out, m.start(), m.end())
    for m in list(re.finditer(r"^.*slop-scan:\s*ignore-line.*$", out, re.MULTILINE | re.IGNORECASE)):
        out = _blank(out, m.start(), m.end())
    if skip_quotes:
        for m in list(re.finditer(r"^[ \t]*>.*$", out, re.MULTILINE)):
            out = _blank(out, m.start(), m.end())
    for m in list(re.finditer(r"`[^`\n]+`", out)):
        out = _blank(out, m.start(), m.end())
    structural = out
    for m in list(URL.finditer(out)):
        out = _blank(out, m.start(), m.end())
    return structural, out


def line_col(text, pos):
    line = text.count("\n", 0, pos) + 1
    col = pos - (text.rfind("\n", 0, pos) + 1) + 1
    return line, col


def split_sentences(text):
    flat = re.sub(r"\s+", " ", text)
    parts = re.split(r"(?<=[.!?])\s+", flat)
    return [p for p in (s.strip() for s in parts) if WORD.search(p)]


def paragraphs(text):
    """Yield (start_offset, end_offset) for blank-line separated paragraphs."""
    pos = 0
    for block in re.split(r"(\n[ \t]*\n)", text):
        if block.strip() and not re.fullmatch(r"\n[ \t]*\n", block):
            yield pos, pos + len(block)
        pos += len(block)


# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------
def _finding(raw, pos, end, sid, lang, cat, sev, trend, note=""):
    line, col = line_col(raw, pos)
    match = raw[pos:end].replace("\n", " ").strip()
    if len(match) > 80:
        match = match[:77] + "..."
    return {"line": line, "col": col, "start": pos, "end": end, "signal": sid, "lang": lang,
            "category": cat, "severity": sev, "trend": trend,
            "points": WEIGHTS[sev], "match": match, "note": note}


def _drop_nested(findings):
    """When one hit sits inside another (for example "testament" inside
    "a testament to", or two contrast patterns on the same phrase), keep only
    the one with more points so a single phrase is not counted twice.
    Fingerprints and document-wide hits (staccato) are never dropped."""
    keep = []
    for f in findings:
        nested = False
        for g in findings:
            if g is f or g["category"] == "fingerprint" or f["category"] == "fingerprint":
                continue
            if g["signal"] in ("staccato-fragments", "hashtag-stack") or f["signal"] in ("staccato-fragments", "hashtag-stack"):
                continue
            inside = g["start"] <= f["start"] and f["end"] <= g["end"]
            if inside and (g["points"], g["end"] - g["start"]) > (f["points"], f["end"] - f["start"]):
                nested = True
                break
        if not nested:
            keep.append(f)
    return keep


def scan_text(raw, langs=None, plain=False, skip_quotes=False, verbose=False):
    """Scan a string. Returns a report dict (see --json output).

    Single lists of three are normal in human prose (Macaron measured the same
    rate in human and model explanatory text), so each one is listed only with
    verbose=True. They always count towards the document-level triad-habit.
    """
    langs = set(langs or ["en", "it", "es", "fr", "de"])
    langs.add("any")
    structural, prose = mask_regions(raw, skip_quotes=skip_quotes)
    findings = []

    for sid, lang, cat, sev, trend, rx in _COMPILED:
        if lang not in langs:
            continue
        target = structural if cat == "fingerprint" else prose
        for m in rx.finditer(target):
            # Patterns anchored on a sentence start may include the previous
            # punctuation; report the position of the first letter.
            start = m.start()
            while start < m.end() and not target[start].isalnum():
                start += 1
            findings.append(_finding(raw, start, m.end(), sid, lang, cat, sev, trend))

    for m in INVISIBLE.finditer(structural):
        name = unicodedata.name(m.group(0), "U+%04X" % ord(m.group(0)))
        findings.append(_finding(raw, m.start(), m.end(), "invisible-character", "any",
                                 "fingerprint", "strong", "active",
                                 note="hidden character %s: delete it, never add one" % name))

    for m in EMOJI_BULLET.finditer(prose):
        findings.append(_finding(raw, m.start(), m.end(), "emoji-bullet", "any", "formatting",
                                 "medium", "active"))
    for m in BOLD_LABEL.finditer(prose):
        findings.append(_finding(raw, m.start(), m.end(), "bold-label-list", "any", "formatting",
                                 "medium", "active"))
    for m in SHORT_QA.finditer(prose):
        findings.append(_finding(raw, m.start(1), m.end(1), "rhetorical-question-answer", "any",
                                 "structure", "medium", "active"))
    for m in TRIAD.finditer(prose):
        findings.append(_finding(raw, m.start(), m.end(), "triad", "any", "structure", "weak",
                                 "active", note="fine alone; a problem when repeated or when the "
                                                "three items say the same thing"))
    if plain:
        for rx, sid in ((BOLD_SPAN, "markdown-leak-bold"), (MD_HEADER, "markdown-leak-header")):
            for m in rx.finditer(prose):
                findings.append(_finding(raw, m.start(), m.end(), sid, "any", "fingerprint",
                                         "strong", "active",
                                         note="Markdown will show as raw symbols on this platform"))
    for i, line in enumerate(prose.split("\n")):
        tags = HASHTAG.findall(line)
        if len(tags) > 5:
            pos = sum(len(l) + 1 for l in prose.split("\n")[:i])
            findings.append(_finding(raw, pos, pos + len(line), "hashtag-stack", "any", "social",
                                     "medium", "active", note="%d hashtags on one line" % len(tags)))

    # Staccato: three or more consecutive sentences of at most three words.
    for p_start, p_end in paragraphs(prose):
        sents = split_sentences(prose[p_start:p_end])
        run = 0
        for s in sents:
            run = run + 1 if len(WORD.findall(s)) <= 3 else 0
            if run == 3:
                findings.append(_finding(raw, p_start, p_end, "staccato-fragments", "any",
                                         "structure", "medium", "active",
                                         note="three or more very short sentences in a row"))
                break

    findings.sort(key=lambda f: (f["start"], f["signal"]))
    # Drop exact duplicates (same signal at same place from overlapping patterns).
    seen, unique = set(), []
    for f in findings:
        key = (f["start"], f["signal"])
        if key not in seen:
            seen.add(key)
            unique.append(f)
    findings = _drop_nested(unique)

    words = len(WORD.findall(prose))
    aggregates = []

    dashes = EM_DASH.findall(prose)
    if dashes:
        extra = max(0, len(dashes) - 1)
        aggregates.append({"signal": "em-dash", "count": len(dashes),
                           "per_100_words": round(100.0 * len(dashes) / max(words, 1), 2),
                           "points": min(extra, 5), "trend": "model-dependent",
                           "note": "one dash is normal; many is a pattern. In Italian, Spanish and "
                                   "French the spaced dash is an English habit"})
    bolds = BOLD_SPAN.findall(prose)
    if len(bolds) >= 3 and len(bolds) * 60 > max(words, 1) and not plain:
        aggregates.append({"signal": "bold-everywhere", "count": len(bolds),
                           "per_100_words": round(100.0 * len(bolds) / max(words, 1), 2),
                           "points": 2, "trend": "active",
                           "note": "more than one bold span per 60 words"})
    symbols = ODD_SYMBOL.findall(prose)
    if len(symbols) >= 3:
        aggregates.append({"signal": "unicode-symbols", "count": len(symbols),
                           "per_100_words": round(100.0 * len(symbols) / max(words, 1), 2),
                           "points": 1, "trend": "active",
                           "note": "arrows and box-drawing characters used as prose punctuation"})
    triads = [f for f in findings if f["signal"] == "triad"]
    if not verbose:
        findings = [f for f in findings if f["signal"] != "triad"]
    if len(triads) >= 3 and len(triads) * 100 >= 3 * max(words, 1):
        aggregates.append({"signal": "triad-habit", "count": len(triads),
                           "per_100_words": round(100.0 * len(triads) / max(words, 1), 2),
                           "points": 2, "trend": "active",
                           "note": "three or more lists of three per 100 words"})
    sents = split_sentences(prose)
    if len(sents) >= UNIFORMITY_MIN_SENTENCES:
        lengths = [len(WORD.findall(s)) for s in sents]
        mean = statistics.mean(lengths)
        cv = statistics.pstdev(lengths) / mean if mean else 0.0
        if cv < UNIFORMITY_MAX_CV:
            aggregates.append({"signal": "metronome-rhythm", "count": len(sents),
                               "per_100_words": None, "points": 2, "trend": "active",
                               "note": "sentence lengths barely vary (CV %.2f, mean %.1f words)"
                                       % (cv, mean)})

    # Clusters per paragraph.
    clusters = []
    for p_start, p_end in paragraphs(prose):
        inside = [f for f in findings if p_start <= f["start"] < p_end and f["category"] != "fingerprint"]
        distinct = sorted({f["signal"] for f in inside})
        pts = sum(f["points"] for f in inside)
        p_words = len(WORD.findall(prose[p_start:p_end]))
        p_density = 100.0 * pts / max(p_words, MIN_WORDS_FOR_DENSITY)
        # A long block (a 21-row table) can collect three unrelated hits far
        # apart; it is a cluster only if the hits are also dense.
        if (len(distinct) >= CLUSTER_MIN_DISTINCT and pts >= CLUSTER_MIN_POINTS
                and p_density >= CLUSTER_DENSITY):
            l1, _ = line_col(raw, p_start)
            l2, _ = line_col(raw, max(p_start, p_end - 1))
            clusters.append({"lines": [l1, l2], "distinct_signals": distinct, "points": pts})

    points = sum(f["points"] for f in findings) + sum(a["points"] for a in aggregates)
    density = round(100.0 * points / max(words, MIN_WORDS_FOR_DENSITY), 2)
    fingerprints = [f for f in findings if f["severity"] == "fingerprint" or f["category"] == "fingerprint"]
    claims = [f for f in findings if f["category"] == "facts"]

    if fingerprints:
        verdict = "BLOCK: fingerprint found (fix before anything else)"
    elif clusters or density >= CLUSTER_DENSITY:
        verdict = "LIKELY SLOP CLUSTER: rewrite the flagged paragraphs"
    elif claims:
        verdict = "VERIFY CLAIMS: check every flagged claim against a source"
    elif density >= REVIEW_DENSITY:
        verdict = "REVIEW: several signals, reread with the checklist"
    else:
        verdict = "NO STRONG PATTERN (heuristics only; still read it)"

    return {"words": words, "points": points, "density_per_100_words": density,
            "verdict_hint": verdict, "fingerprints": len(fingerprints),
            "claims_to_verify": len(claims), "findings": findings,
            "aggregates": aggregates, "clusters": clusters}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def format_report(name, rep):
    out = ["slop_scan: %s" % name,
           "words %d | points %d | density %.2f per 100 words | %s"
           % (rep["words"], rep["points"], rep["density_per_100_words"], rep["verdict_hint"])]
    if rep["findings"]:
        out.append("findings (line:col severity signal \"match\"):")
        for f in rep["findings"]:
            note = "  [%s]" % f["note"] if f["note"] else ""
            out.append("  %d:%d  %-11s %-26s \"%s\" (%s)%s"
                       % (f["line"], f["col"], f["severity"].upper(), f["signal"], f["match"],
                          f["trend"], note))
    if rep["aggregates"]:
        out.append("document-level:")
        for a in rep["aggregates"]:
            per = "" if a["per_100_words"] is None else ", %.2f per 100 words" % a["per_100_words"]
            out.append("  %-18s count %d%s, +%d points. %s"
                       % (a["signal"], a["count"], per, a["points"], a["note"]))
    if rep["clusters"]:
        out.append("clusters:")
        for c in rep["clusters"]:
            out.append("  lines %d-%d: %d distinct signals, %d points (%s)"
                       % (c["lines"][0], c["lines"][1], len(c["distinct_signals"]), c["points"],
                          ", ".join(c["distinct_signals"])))
    out.append("note: heuristic hits are reasons to reread, not proof of AI authorship.")
    return "\n".join(out)


FAIL_LEVELS = ("fingerprint", "cluster", "review")


def should_fail(rep, level):
    if level is None:
        return False
    if rep["fingerprints"]:
        return True
    if level in ("cluster", "review") and (rep["clusters"] or rep["density_per_100_words"] >= CLUSTER_DENSITY):
        return True
    if level == "review" and (rep["density_per_100_words"] >= REVIEW_DENSITY or rep["claims_to_verify"]):
        return True
    return False


def main(argv=None):
    ap = argparse.ArgumentParser(description="Heuristic AI-slop signal scanner (no dependencies).")
    ap.add_argument("paths", nargs="+", help="files to scan, or - for stdin")
    ap.add_argument("--lang", default="en,it,es,fr,de",
                    help="comma-separated languages to check (default: en,it,es,fr,de)")
    ap.add_argument("--plain", action="store_true",
                    help="target platform shows raw text (YouTube, TikTok, Instagram): flag Markdown")
    ap.add_argument("--skip-quotes", action="store_true", help="ignore Markdown blockquote lines")
    ap.add_argument("--json", action="store_true", help="print JSON instead of text")
    ap.add_argument("--verbose", action="store_true",
                    help="also list every single list of three (always counted in triad-habit)")
    ap.add_argument("--fail-on", choices=FAIL_LEVELS, default=None,
                    help="exit 1 when this level is reached (for CI or pre-publish hooks)")
    args = ap.parse_args(argv)

    langs = [l.strip().lower() for l in args.lang.split(",") if l.strip()]
    unknown = [l for l in langs if l not in ("en", "it", "es", "fr", "de")]
    if unknown:
        sys.stderr.write("error: unsupported language(s): %s. Use en, it, es, fr, de.\n" % ", ".join(unknown))
        return 2

    reports, failed = {}, False
    for path in args.paths:
        try:
            if path == "-":
                text = sys.stdin.read()
            else:
                with open(path, encoding="utf-8") as fh:
                    text = fh.read()
        except FileNotFoundError:
            sys.stderr.write("error: file not found: %s\n" % path)
            return 2
        except UnicodeDecodeError:
            sys.stderr.write("error: %s is not UTF-8 text. Convert it first, e.g. "
                             "iconv -f latin1 -t utf-8 %s > out.txt\n" % (path, path))
            return 2
        except OSError as exc:
            sys.stderr.write("error: cannot read %s: %s\n" % (path, exc))
            return 2
        rep = scan_text(text, langs=langs, plain=args.plain, skip_quotes=args.skip_quotes,
                        verbose=args.verbose)
        reports[path] = rep
        failed = failed or should_fail(rep, args.fail_on)

    if args.json:
        print(json.dumps(reports if len(reports) > 1 else next(iter(reports.values())),
                         ensure_ascii=False, indent=2))
    else:
        print("\n\n".join(format_report(n, r) for n, r in reports.items()))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
