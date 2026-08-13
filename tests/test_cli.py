from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VocCliTests(unittest.TestCase):
    def test_audit_example(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "audit_review_csv.py"),
                    str(ROOT / "examples" / "reviews.example.csv"),
                    "--text-col",
                    "review",
                    "--platform-col",
                    "platform",
                    "--id-col",
                    "review_id",
                    "--output-dir",
                    str(output_dir),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            summary = json.loads(result.stdout)
            self.assertEqual(summary["input_rows"], 6)
            self.assertEqual(summary["effective_rows"], 4)
            self.assertEqual(summary["excluded_rows"], 2)
            self.assertEqual(summary["exclusions_by_reason"]["default_boilerplate"], 1)
            self.assertEqual(summary["exclusions_by_reason"]["exact_duplicate"], 1)
            self.assertTrue((output_dir / "cleaned_reviews.csv").exists())
            self.assertTrue((output_dir / "excluded_reviews.csv").exists())

    def test_render_example(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            html_path = output_dir / "report.html"
            text_path = output_dir / "report.txt"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "render_voc_html.py"),
                    str(ROOT / "examples" / "report-spec.example.json"),
                    "--html",
                    str(html_path),
                    "--text",
                    str(text_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            summary = json.loads(result.stdout)
            self.assertEqual(summary["tables"], 2)
            self.assertTrue(summary["contains_yellow"])
            self.assertFalse(summary["contains_original_comment_column"])
            self.assertIn("25.0%（1/4）", html_path.read_text(encoding="utf-8"))
            self.assertIn("跨平台真实需求结论", text_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
