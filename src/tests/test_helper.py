import unittest

from ..entity import Entity
from ..entity_type import EntityType


class TestHelperMethods(unittest.TestCase):
    def test_parse_entities(self):
        test_input = [
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
        expected_result = [Entity(EntityType.ACTOR, 0, ["The", "MPON"])]
        # test_result = parse_

        self.assertEqual(expected_result, test_result)


if __name__ == "__main__":
    unittest.main()
