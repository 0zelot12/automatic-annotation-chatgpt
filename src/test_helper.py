import unittest

from annotation_metrics import AnnotationMetrics

from entity import Entity
from entity_type import EntityType
from entity_tag import EntityTag

from helper import parse_entities, calculate_metrics, convert_to_template_example


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

    def test_parse_entities_offset(self):
        tokens = [
            "The",
            "MPON",
            "sents",
            "the",
            "dismissal",
            "to",
            "the",
            "MPOO",
            ".",
        ]

        annotated_tokens = [
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

        entities = parse_entities(annotated_tokens)

        self.assertEqual(len(tokens), len(annotated_tokens) - len(entities) * 2)

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

    def test_convert_to_template_example(self):
        tokens = [
            "The",
            "manufacturer",
            "sends",
            "the",
            "invoice",
            "to",
            "the",
            "customer",
            ".",
            "If",
            "the",
            "customer",
            "pays",
            "within",
            "two",
            "weeks",
            "the",
            "order",
            "is",
            "marked",
            "as",
            "completed",
            ".",
        ]

        ner_tags = [
            EntityTag.B_ACTOR,
            EntityTag.I_ACTOR,
            EntityTag.B_ACTIVITY,
            EntityTag.B_ACTIVITY_DATA,
            EntityTag.I_ACTIVITY_DATA,
            EntityTag.NO_ENTITY,
            EntityTag.B_ACTOR,
            EntityTag.I_ACTOR,
            EntityTag.NO_ENTITY,
            EntityTag.NO_ENTITY,
            EntityTag.B_ACTOR,
            EntityTag.I_ACTOR,
            EntityTag.B_ACTIVITY,
            EntityTag.NO_ENTITY,
            EntityTag.NO_ENTITY,
            EntityTag.NO_ENTITY,
            EntityTag.NO_ENTITY,
            EntityTag.NO_ENTITY,
            EntityTag.B_ACTIVITY,
            EntityTag.I_ACTIVITY,
            EntityTag.NO_ENTITY,
            EntityTag.NO_ENTITY,
            EntityTag.NO_ENTITY,
        ]

        expected_example = [
            "<ACTOR>",
            "The",
            "manufacturer",
            "</ACTOR>",
            "<ACTIVITY>",
            "sends",
            "</ACTIVITY>",
            "<ACTIVITY_DATA>",
            "the",
            "invoice",
            "</ACTIVITY_DATA>",
            "to",
            "<ACTOR>",
            "the",
            "customer",
            "</ACTOR>",
            ".",
            "If",
            "<ACTOR>",
            "the",
            "customer",
            "</ACTOR>",
            "<ACTIVITY>",
            "pays",
            "</ACTIVITY>",
            "within",
            "two",
            "weeks",
            "the",
            "order",
            "<ACTIVITY>",
            "is",
            "marked",
            "</ACTIVITY>",
            "as",
            "completed",
            ".",
        ]

        self.assertEqual(
            convert_to_template_example(tokens, ner_tags),
            expected_example,
        )


if __name__ == "__main__":
    unittest.main()
