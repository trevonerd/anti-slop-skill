"""Minimal tests for slop_scan.py. Run with: python3 -m unittest discover -s tests"""
import io
import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "skills", "anti-slop", "scripts", "slop_scan.py")
sys.path.insert(0, os.path.dirname(SCRIPT))

import slop_scan  # noqa: E402


def signals(report):
    return {f["signal"] for f in report["findings"]}


class FingerprintTests(unittest.TestCase):
    def test_chatbot_residue_and_citation_codes(self):
        rep = slop_scan.scan_text("Here's your caption: rainy jazz :contentReference[oaicite:0]{index=0}")
        self.assertIn("chatbot-residue", signals(rep))
        self.assertIn("citation-code", signals(rep))
        self.assertTrue(rep["verdict_hint"].startswith("BLOCK"))

    def test_utm_param_in_url_is_found(self):
        rep = slop_scan.scan_text("Source: https://example.com/a?utm_source=chatgpt.com")
        self.assertIn("chatbot-link-param", signals(rep))

    def test_placeholder(self):
        rep = slop_scan.scan_text("Subscribe at [Insert link] and see you on 2026-XX-XX.")
        self.assertEqual(sum(1 for f in rep["findings"] if f["signal"] == "placeholder"), 2)

    def test_italian_residue(self):
        rep = slop_scan.scan_text("Certo! Ecco la tua caption: caffè e jazz.", langs=["it"])
        self.assertIn("chatbot-residue", signals(rep))

    def test_invisible_character_but_not_emoji_zwj(self):
        rep = slop_scan.scan_text("jazz\u200bcafe")
        self.assertIn("invisible-character", signals(rep))
        family = "\U0001F468\u200d\U0001F469\u200d\U0001F467"
        self.assertNotIn("invisible-character", signals(slop_scan.scan_text("our crew " + family)))


class StructureTests(unittest.TestCase):
    def test_contrast_en(self):
        rep = slop_scan.scan_text("It's not just music, it's a mood.")
        self.assertTrue(signals(rep) & {"contrast-its-not", "contrast-not-just"})

    def test_contrast_counted_once(self):
        rep = slop_scan.scan_text("It's not just music, it's a mood.")
        contrasts = [f for f in rep["findings"] if f["signal"].startswith("contrast")]
        self.assertEqual(len(contrasts), 1)

    def test_contrast_it_es_fr_de(self):
        cases = {
            "it": "Non solo musica, ma anche emozioni.",
            "es": "No solo música, sino también calma.",
            "fr": "Non seulement de la musique, mais aussi du calme.",
            "de": "Nicht nur Musik, sondern auch Ruhe.",
        }
        for lang, text in cases.items():
            rep = slop_scan.scan_text(text, langs=[lang])
            self.assertTrue(any(s.startswith("contrast") for s in signals(rep)), lang)

    def test_rhetorical_question_and_staccato(self):
        rep = slop_scan.scan_text("The result? A calmer morning. Clear. Direct. Human.")
        self.assertIn("rhetorical-question-answer", signals(rep))
        self.assertIn("staccato-fragments", signals(rep))

    def test_em_dash_aggregate(self):
        rep = slop_scan.scan_text("Rain \u2014 coffee \u2014 jazz \u2014 again \u2014 and more.")
        dash = [a for a in rep["aggregates"] if a["signal"] == "em-dash"][0]
        self.assertEqual(dash["count"], 4)
        self.assertEqual(dash["points"], 3)

    def test_emoji_bullets_and_bold_labels(self):
        text = "\u2705 Fast\n\U0001F680 Easy\n- **Mood:** cozy\n- **Tempo:** slow\n"
        rep = slop_scan.scan_text(text)
        self.assertIn("emoji-bullet", signals(rep))
        self.assertIn("bold-label-list", signals(rep))

    def test_plain_mode_flags_markdown(self):
        rep = slop_scan.scan_text("**Smooth jazz** for a rainy morning", plain=True)
        self.assertIn("markdown-leak-bold", signals(rep))
        self.assertNotIn("markdown-leak-bold", signals(slop_scan.scan_text("**Smooth jazz** here")))


class DensityRuleTests(unittest.TestCase):
    def test_single_weak_word_is_not_a_block(self):
        rep = slop_scan.scan_text("A crucial detail: the Rhodes comes in at 0:12, after the kettle.")
        self.assertEqual(rep["clusters"], [])
        self.assertTrue(rep["verdict_hint"].startswith("NO STRONG PATTERN"))

    def test_cluster_detected(self):
        text = ("In today's fast-paced world, this vibrant playlist is a testament to calm. "
                "Whether you're studying or relaxing, it's not just music, it's a mood.")
        rep = slop_scan.scan_text(text)
        self.assertTrue(rep["clusters"])
        self.assertTrue(rep["verdict_hint"].startswith("LIKELY SLOP CLUSTER"))

    def test_human_caption_is_clean(self):
        rep = slop_scan.scan_text("7:30, kettle on, first track of the mix. "
                                  "The Rhodes comes in at 0:12. #smoothjazz #lofi #Shorts")
        self.assertEqual(rep["findings"], [])

    def test_single_triads_hidden_but_habit_counted(self):
        text = ("Calm, cozy and warm. Rain, coffee and jazz. Slow, soft and kind. "
                "Piano, bass and drums.")
        rep = slop_scan.scan_text(text)
        self.assertNotIn("triad", signals(rep))
        self.assertIn("triad-habit", {a["signal"] for a in rep["aggregates"]})
        self.assertIn("triad", signals(slop_scan.scan_text(text, verbose=True)))

    def test_promise_needs_verification(self):
        rep = slop_scan.scan_text("Soft piano for instant calm.")
        self.assertTrue(rep["claims_to_verify"])


class MaskingTests(unittest.TestCase):
    def test_code_frontmatter_and_ignore_markers(self):
        text = ("---\nname: x\ndescription: a testament to delve\n---\n"
                "```\nIt's not just code, it's a mood.\n```\n"
                "Inline `vibrant tapestry` stays quiet.\n"
                "<!-- slop-scan: off -->\nIn today's fast-paced world\n<!-- slop-scan: on -->\n"
                "Nestled in the heart of town. slop-scan: ignore-line\n"
                "Plain sentence about a sax.\n")
        rep = slop_scan.scan_text(text)
        self.assertEqual(rep["findings"], [])

    def test_inline_code_fingerprint_is_documentation(self):
        rep = slop_scan.scan_text("The scanner flags `oaicite` and `utm_source=chatgpt.com` codes.")
        self.assertEqual(rep["fingerprints"], 0)

    def test_line_numbers(self):
        rep = slop_scan.scan_text("first line\nsecond line\nWe delve into jazz.")
        hit = [f for f in rep["findings"] if f["signal"] == "ai-word"][0]
        self.assertEqual((hit["line"], hit["col"]), (3, 4))


class CliTests(unittest.TestCase):
    def run_cli(self, args, stdin=""):
        return subprocess.run([sys.executable, SCRIPT] + args, input=stdin,
                              capture_output=True, text=True)

    def test_json_from_stdin(self):
        res = self.run_cli(["-", "--json"], stdin="I hope this helps!")
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data["fingerprints"], 1)

    def test_fail_on_exit_code(self):
        res = self.run_cli(["-", "--fail-on", "fingerprint"], stdin="As an AI language model, I")
        self.assertEqual(res.returncode, 1)
        res = self.run_cli(["-", "--fail-on", "fingerprint"], stdin="Brushes on the snare.")
        self.assertEqual(res.returncode, 0)

    def test_missing_file_and_bad_lang(self):
        self.assertEqual(self.run_cli(["/no/such/file.md"]).returncode, 2)
        self.assertEqual(self.run_cli(["-", "--lang", "xx"], stdin="hi").returncode, 2)


if __name__ == "__main__":
    unittest.main()
