import unittest
from types import SimpleNamespace

from kubera_innovation.presidio_adapter import PresidioTextRedactor


class _FakeAnalyzer:
    def __init__(self):
        self.calls = []

    def analyze(self, **kwargs):
        self.calls.append(kwargs)
        return [SimpleNamespace(entity_type="EMAIL_ADDRESS")]


class _FakeAnonymizer:
    def anonymize(self, *, text, analyzer_results):
        return SimpleNamespace(text=text.replace("person@example.com", "<EMAIL_ADDRESS>"))


class PresidioAdapterTests(unittest.TestCase):
    def test_redacts_using_injected_engines(self):
        analyzer = _FakeAnalyzer()
        redactor = PresidioTextRedactor(analyzer=analyzer, anonymizer=_FakeAnonymizer())
        result = redactor.redact("Contact person@example.com")
        self.assertEqual(result, "Contact <EMAIL_ADDRESS>")
        self.assertEqual(analyzer.calls[0]["language"], "en")

    def test_entities_are_forwarded_when_configured(self):
        analyzer = _FakeAnalyzer()
        redactor = PresidioTextRedactor(
            entities=["EMAIL_ADDRESS", "PHONE_NUMBER"],
            analyzer=analyzer,
            anonymizer=_FakeAnonymizer(),
        )
        redactor.redact("person@example.com")
        self.assertEqual(analyzer.calls[0]["entities"], ["EMAIL_ADDRESS", "PHONE_NUMBER"])

    def test_injected_engines_must_be_supplied_as_pair(self):
        with self.assertRaises(ValueError):
            PresidioTextRedactor(analyzer=_FakeAnalyzer())

    def test_language_must_not_be_empty(self):
        with self.assertRaises(ValueError):
            PresidioTextRedactor(language=" ", analyzer=_FakeAnalyzer(), anonymizer=_FakeAnonymizer())


if __name__ == "__main__":
    unittest.main()
