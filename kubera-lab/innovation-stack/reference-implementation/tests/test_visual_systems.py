import unittest

from kubera_innovation.visual_systems import DiagramIntent, SUPPORTED_DIAGRAM_TYPES


class VisualSystemsTests(unittest.TestCase):
    def test_catalog_has_39_types(self):
        self.assertEqual(len(SUPPORTED_DIAGRAM_TYPES), 39)

    def test_valid_intent_has_contract_version(self):
        intent = DiagramIntent("architecture", "Agent OS", "Show system layers")
        self.assertEqual(intent.to_payload()["contract_version"], "1.0")

    def test_unknown_type_fails(self):
        with self.assertRaises(ValueError):
            DiagramIntent("unknown", "x", "y")

    def test_empty_title_fails(self):
        with self.assertRaises(ValueError):
            DiagramIntent("timeline", " ", "y")

    def test_output_format_fails_closed(self):
        with self.assertRaises(ValueError):
            DiagramIntent("timeline", "x", "y", output_format="pdf")

    def test_mermaid_source_supported(self):
        intent = DiagramIntent("flowchart", "x", "y", source_format="mermaid")
        self.assertIn("mermaid", intent.to_renderer_instruction())

    def test_brand_source_is_preserved(self):
        intent = DiagramIntent("architecture", "x", "y", brand_source="https://example.com")
        self.assertIn("https://example.com", intent.to_renderer_instruction())

    def test_static_output_is_default(self):
        intent = DiagramIntent("sequence", "x", "y")
        self.assertFalse(intent.motion)
        self.assertIn("Keep output static", intent.to_renderer_instruction())


if __name__ == "__main__":
    unittest.main()
