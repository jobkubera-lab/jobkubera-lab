import unittest
from unittest.mock import patch

from kubera_innovation.tool_safety import (
    PrivacyGate,
    PrivacyRedactionError,
    ToolLoopGuard,
    ToolValidator,
)


class _EmailRedactor:
    def redact(self, text: str) -> str:
        return text.replace("person@example.com", "<EMAIL>")


class _BrokenRedactor:
    def redact(self, text: str) -> str:
        raise RuntimeError("boom")


class _InvalidRedactor:
    def redact(self, text: str):
        return None


class PrivacyGateTests(unittest.TestCase):
    def test_redacts_secret_by_key(self):
        result = PrivacyGate.sanitize({"api_key": "abc123", "path": "README.md"})
        self.assertEqual(result.value["api_key"], "***REDACTED***")
        self.assertEqual(result.value["path"], "README.md")
        self.assertIn("api_key", result.redacted_paths)

    def test_redacts_nested_bearer_and_connection_string(self):
        result = PrivacyGate.sanitize({"headers": {"x": "Bearer abcdefghijk"}, "dsn": "postgres://u:p@host/db"})
        self.assertNotIn("abcdefghijk", str(result.value))
        self.assertNotIn("postgres://", str(result.value))
        self.assertEqual(len(result.redacted_paths), 2)

    def test_preserves_non_secret_text(self):
        result = PrivacyGate.sanitize({"message": "normal project text"})
        self.assertTrue(result.clean)
        self.assertEqual(result.value["message"], "normal project text")

    def test_optional_text_redactor_masks_pii_and_records_path(self):
        result = PrivacyGate.sanitize(
            {"message": "Email person@example.com for help"},
            text_redactor=_EmailRedactor(),
        )
        self.assertEqual(result.value["message"], "Email <EMAIL> for help")
        self.assertEqual(result.redacted_paths, ("message",))

    def test_builtin_secret_redaction_still_wins_with_external_redactor(self):
        result = PrivacyGate.sanitize(
            {"api_key": "person@example.com"},
            text_redactor=_EmailRedactor(),
        )
        self.assertEqual(result.value["api_key"], "***REDACTED***")
        self.assertEqual(result.redacted_paths, ("api_key",))

    def test_external_redactor_failure_fails_closed(self):
        with self.assertRaises(PrivacyRedactionError):
            PrivacyGate.sanitize({"message": "sensitive"}, text_redactor=_BrokenRedactor())

    def test_external_redactor_must_return_string(self):
        with self.assertRaises(PrivacyRedactionError):
            PrivacyGate.sanitize({"message": "sensitive"}, text_redactor=_InvalidRedactor())


class ToolValidatorTests(unittest.TestCase):
    def setUp(self):
        self.schema = {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "format": {"type": "string", "enum": ["text", "json"]},
            },
            "required": ["path"],
            "additionalProperties": False,
        }

    def test_accepts_valid_input(self):
        self.assertTrue(ToolValidator.validate({"path": "a.txt", "format": "text"}, self.schema).valid)

    def test_rejects_missing_required_field(self):
        self.assertFalse(ToolValidator.validate({}, self.schema).valid)

    def test_rejects_extra_field_fail_closed(self):
        result = ToolValidator.validate({"path": "a", "unknown": 1}, self.schema)
        self.assertFalse(result.valid)
        self.assertIn("unexpected field", result.error)

    def test_rejects_wrong_enum(self):
        self.assertFalse(ToolValidator.validate({"path": "a", "format": "xml"}, self.schema).valid)


class ToolLoopGuardTests(unittest.TestCase):
    def test_must_start(self):
        with self.assertRaises(RuntimeError):
            ToolLoopGuard().step()

    def test_iteration_limit(self):
        guard = ToolLoopGuard(max_iterations=2)
        guard.start()
        guard.step()
        guard.step()
        with self.assertRaises(RuntimeError):
            guard.step()

    def test_timeout_uses_monotonic_clock(self):
        guard = ToolLoopGuard(timeout_seconds=1)
        with patch("kubera_innovation.tool_safety.time.monotonic", side_effect=[10.0, 11.1]):
            guard.start()
            with self.assertRaises(TimeoutError):
                guard.step()


if __name__ == "__main__":
    unittest.main()
