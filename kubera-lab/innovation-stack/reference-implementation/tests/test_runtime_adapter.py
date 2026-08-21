import unittest
from kubera_innovation.runtime_adapter import new_run_id, RunStatus

class RuntimeAdapterTests(unittest.TestCase):
    def test_new_run_id(self): self.assertTrue(len(new_run_id())>20)
    def test_statuses(self): self.assertEqual(RunStatus.PAUSED.value,"paused")
