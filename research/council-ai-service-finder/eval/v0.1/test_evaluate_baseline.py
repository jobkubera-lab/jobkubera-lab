import unittest

import evaluate_baseline as baseline


class BaselineEvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.catalogue = [
            {
                "id": "council-tax-support",
                "name": "Council tax support",
                "description": "Help if you cannot afford your council tax bill",
                "aliases": ["council tax reduction", "help with council tax"],
            },
            {
                "id": "bulky-waste",
                "name": "Bulky waste collection",
                "description": "Collection of large household items",
                "aliases": ["old fridge", "large rubbish"],
            },
        ]

    def test_predict_returns_best_controlled_service(self):
        predicted, top3, score = baseline.predict(
            "I need help with council tax", self.catalogue
        )
        self.assertEqual(predicted, "council-tax-support")
        self.assertEqual(top3[0][0], "council-tax-support")
        self.assertGreater(score, 0)

    def test_predict_falls_back_for_unrelated_query(self):
        predicted, _, score = baseline.predict(
            "renew my passport", self.catalogue
        )
        self.assertIsNone(predicted)
        self.assertLess(score, baseline.FALLBACK_THRESHOLD)

    def test_evaluate_reports_top1_top3_and_fallback_metrics(self):
        queries = [
            {
                "id": "q1",
                "query": "help with council tax",
                "expected_service_id": "council-tax-support",
            },
            {
                "id": "q2",
                "query": "take away my old fridge",
                "expected_service_id": "bulky-waste",
            },
            {
                "id": "q3",
                "query": "renew my passport",
                "expected_service_id": None,
            },
        ]
        metrics = baseline.evaluate(self.catalogue, queries)
        self.assertEqual(metrics["precision_at_1"], 1.0)
        self.assertEqual(metrics["top3_recall"], 1.0)
        self.assertEqual(metrics["fallback_accuracy"], 1.0)
        self.assertEqual(metrics["false_positive_fallbacks"], 0)


if __name__ == "__main__":
    unittest.main()
