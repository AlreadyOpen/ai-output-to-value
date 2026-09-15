from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ClaimGatePrintTests(unittest.TestCase):
    def test_claim_gate_has_dedicated_print_summary(self):
        source = (ROOT / "web" / "src" / "components" / "claim-gate-app.tsx").read_text(encoding="utf-8")
        self.assertIn('className="aiov-print-summary"', source)
        self.assertIn("Printable decision record", source)
        self.assertIn("Record complete for this decision. Not an audit of the underlying system.", source)
        self.assertIn("Print decision record", source)

    def test_print_css_hides_interactive_gate_and_formats_record(self):
        source = (ROOT / "web" / "src" / "styles.css").read_text(encoding="utf-8")
        self.assertIn(".aiov-gate-root > :not(.aiov-print-summary)", source)
        self.assertIn(".aiov-print-summary", source)
        self.assertIn(".aiov-print-check", source)
        self.assertIn("break-inside: avoid", source)
        self.assertIn(".site-header", source)


if __name__ == "__main__":
    unittest.main()
