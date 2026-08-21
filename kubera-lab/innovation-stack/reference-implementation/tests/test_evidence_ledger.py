import unittest

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


if __name__ == "__main__":
    unittest.main()
