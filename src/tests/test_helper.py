import unittest

from helper import convert_result, convert_tags


class TestHelperMethods(unittest.TestCase):
    def test_convert_results(self):
        test_annotations = [
            "<A>The<A>",
            "<A>company<A>",
            "sents",
            "the",
            "confirmation",
            "to",
            "<A>the<A>",
            "<A>client<A>",
            ".",
        ]

        expected_result = [
            "Actor",
            "Actor",
            "O",
            "O",
            "O",
            "O",
            "Actor",
            "Actor",
            "O",
        ]

        test_result = convert_result(test_annotations, "Actor")

        self.assertEqual(expected_result, test_result)

    def test_convert_tags(self):
        test_tags = [
            "B-Actor",
            "I-Actor",
            "O",
            "O",
            "O",
            "B-Actor",
        ]

        expected_result = [
            "Actor",
            "Actor",
            "O",
            "O",
            "O",
            "Actor",
        ]

        test_result = convert_tags(test_tags, "Actor")

        self.assertEqual(test_result, expected_result)


if __name__ == "__main__":
    unittest.main()
