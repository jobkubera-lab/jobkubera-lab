import unittest
from unittest.mock import patch

from kubera_innovation.tool_safety import PrivacyGate, ToolLoopGuard, ToolValidator


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
