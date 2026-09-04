import unittest
from dataclasses import replace

from kubera_innovation.evidence_ledger import EvidenceLedger


class EvidenceLedgerTests(unittest.TestCase):
    def setUp(self):
        self.ledger = EvidenceLedger()

    def tearDown(self):
        self.ledger.close()

    def test_append_and_verify_chain(self):
        self.ledger.append(run_id="r1", stage="builder", input_value={"x": 1}, output_value={"y": 2})
        self.ledger.append(run_id="r1", stage="critic", input_value={"y": 2}, output_value={"ok": True})
        self.assertTrue(self.ledger.verify_chain())

    def test_first_entry_uses_genesis(self):
        entry = self.ledger.append(run_id="r1", stage="builder", input_value="a", output_value="b")
        self.assertEqual(entry.previous_hash, EvidenceLedger.GENESIS_HASH)

    def test_second_entry_links_first_hash(self):
        first = self.ledger.append(run_id="r1", stage="builder", input_value="a", output_value="b")
        second = self.ledger.append(run_id="r1", stage="critic", input_value="b", output_value="c")
        self.assertEqual(second.previous_hash, first.entry_hash)

    def test_filter_by_run_id(self):
        self.ledger.append(run_id="r1", stage="builder", input_value=1, output_value=2)
        self.ledger.append(run_id="r2", stage="builder", input_value=3, output_value=4)
        self.assertEqual(len(self.ledger.entries("r1")), 1)

    def test_hash_is_stable_for_dictionary_order(self):
        self.assertEqual(
            EvidenceLedger.hash_value({"a": 1, "b": 2}),
            EvidenceLedger.hash_value({"b": 2, "a": 1}),
        )

    def test_empty_stage_rejected(self):
        with self.assertRaises(ValueError):
            self.ledger.append(run_id="r1", stage=" ", input_value=1, output_value=2)

    def test_export_package_is_hash_verifiable_and_omits_raw_payloads(self):
        self.ledger.append(
            run_id="r1",
            stage="source",
            input_value={"query": "private raw query"},
            output_value={"answer": "private raw answer"},
            metadata={"source": "https://example.gov.uk/service"},
        )
        self.ledger.append(
            run_id="r1",
            stage="verify",
            input_value="private raw answer",
            output_value={"verified": True},
        )
        package = self.ledger.export_package("r1")

        self.assertTrue(EvidenceLedger.verify_package(package))
        self.assertEqual(len(package.entries), 2)
        rendered = str(package.to_dict())
        self.assertNotIn("private raw query", rendered)
        self.assertNotIn("private raw answer", rendered)
        self.assertIn("https://example.gov.uk/service", rendered)

    def test_package_hash_tampering_is_detected(self):
        self.ledger.append(run_id="r1", stage="builder", input_value=1, output_value=2)
        package = self.ledger.export_package("r1")
        tampered = replace(package, package_hash="sha256:" + "0" * 64)
        self.assertFalse(EvidenceLedger.verify_package(tampered))

    def test_entry_tampering_is_detected(self):
        self.ledger.append(run_id="r1", stage="builder", input_value=1, output_value=2)
        package = self.ledger.export_package("r1")
        bad_entry = replace(package.entries[0], stage="tampered")
        tampered = replace(package, entries=(bad_entry,))
        self.assertFalse(EvidenceLedger.verify_package(tampered))

    def test_package_rejects_entry_from_other_run(self):
        self.ledger.append(run_id="r1", stage="builder", input_value=1, output_value=2)
        other = self.ledger.append(run_id="r2", stage="builder", input_value=3, output_value=4)
        package = self.ledger.export_package("r1")
        mixed = replace(package, entries=(other,))
        self.assertFalse(EvidenceLedger.verify_package(mixed))

    def test_export_missing_run_rejected(self):
        with self.assertRaises(KeyError):
            self.ledger.export_package("missing")


if __name__ == "__main__":
    unittest.main()
