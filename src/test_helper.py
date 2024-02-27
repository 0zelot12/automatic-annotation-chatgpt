import unittest

from entity import Entity
from entity_type import EntityType

from helper import parse_entities


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


if __name__ == "__main__":
    unittest.main()
