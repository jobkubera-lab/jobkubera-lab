import unittest
from kubera_innovation.provider_budget import ProviderSeriesBudget

class ProviderSeriesBudgetTests(unittest.TestCase):
    def test_cumulative_tokens_and_calls(self):
        b=ProviderSeriesBudget(2,100)
        b.consume(tokens=40); b.consume(tokens=50)
        self.assertEqual(b.remaining_calls,0); self.assertEqual(b.remaining_tokens,10)
        with self.assertRaises(PermissionError): b.consume(tokens=1)
    def test_token_exhaustion(self):
        b=ProviderSeriesBudget(5,10)
        with self.assertRaises(PermissionError): b.consume(tokens=11)
