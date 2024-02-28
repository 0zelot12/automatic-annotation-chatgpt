import unittest
from annotation_metrics import AnnotationMetrics

from entity import Entity
from entity_type import EntityType

from helper import parse_entities, calculate_metrics


class TestHelperMethods(unittest.TestCase):
    # TODO: Empty case, Invalid Case
    def test_parse_entities(self):
        self.assertEqual(
            parse_entities(
                [
                    "<ACTOR>",
                    "The",
                    "MPON",
                    "</ACTOR>",
                    "<ACTIVITY>",
                    "sents",
                    "</ACTIVITY>",
                    "<ACTIVITY_DATA>",
                    "the",
                    "dismissal",
                    "</ACTIVITY_DATA>",
                    "to",
                    "<ACTOR>",
                    "the",
                    "MPOO",
                    "</ACTOR>",
                    ".",
                ]
            ),
            [
                Entity(EntityType.ACTOR, 0, ["The", "MPON"]),
                Entity(EntityType.ACTIVITY, 2, ["sents"]),
                Entity(EntityType.ACTIVITY_DATA, 3, ["the", "dismissal"]),
                Entity(EntityType.ACTOR, 6, ["the", "MPOO"]),
            ],
        )

    def test_calculate_metrics(self):
        expected_metrics = AnnotationMetrics(precision=0.67, recall=0.5, f1_score=0.57)
        metrics = calculate_metrics(
            [
                Entity(EntityType.ACTOR, 1, ["MPON"]),
                Entity(EntityType.ACTIVITY, 2, ["sents"]),
                Entity(EntityType.ACTIVITY_DATA, 3, ["the", "dismissal"]),
            ],
            [
                Entity(EntityType.ACTOR, 0, ["The", "MPON"]),
                Entity(EntityType.ACTIVITY, 2, ["sents"]),
                Entity(EntityType.ACTIVITY_DATA, 3, ["the", "dismissal"]),
                Entity(EntityType.ACTOR, 6, ["the", "MPOO"]),
            ],
        )
        self.assertEqual(metrics, expected_metrics)

    def test_calculate_metrics_total_match(self):
        expected_metrics = AnnotationMetrics(precision=1.0, recall=1.0, f1_score=1.0)
        metrics = calculate_metrics(
            [
                Entity(EntityType.ACTOR, 0, ["The", "MPON"]),
                Entity(EntityType.ACTIVITY, 2, ["sents"]),
                Entity(EntityType.ACTIVITY_DATA, 3, ["the", "dismissal"]),
                Entity(EntityType.ACTOR, 6, ["the", "MPOO"]),
            ],
            [
                Entity(EntityType.ACTOR, 0, ["The", "MPON"]),
                Entity(EntityType.ACTIVITY, 2, ["sents"]),
                Entity(EntityType.ACTIVITY_DATA, 3, ["the", "dismissal"]),
                Entity(EntityType.ACTOR, 6, ["the", "MPOO"]),
            ],
        )
        self.assertEqual(metrics, expected_metrics)

    def test_calculate_metrics_total_mismatch(self):
        expected_metrics = AnnotationMetrics(precision=0.0, recall=0.0, f1_score=-1.0)
        metrics = calculate_metrics(
            [
                Entity(EntityType.ACTOR, 3, ["The", "MPON"]),
                Entity(EntityType.ACTIVITY, 5, ["sents"]),
                Entity(EntityType.ACTIVITY_DATA, 8, ["the", "dismissal"]),
                Entity(EntityType.ACTOR, 10, ["the", "MPOO"]),
            ],
            [
                Entity(EntityType.ACTOR, 0, ["The", "MPON"]),
                Entity(EntityType.ACTIVITY, 2, ["sents"]),
                Entity(EntityType.ACTIVITY_DATA, 3, ["the", "dismissal"]),
                Entity(EntityType.ACTOR, 6, ["the", "MPOO"]),
            ],
        )
        self.assertEqual(metrics, expected_metrics)


if __name__ == "__main__":
    unittest.main()
