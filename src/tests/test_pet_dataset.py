import unittest
import pandas as pd

from pet_dataset import PetDataset


class TestPetDataset(unittest.TestCase):
    def setUp(self):
        # Initialize a PetDataset instance
        self.pet_data_instance = PetDataset()

    def test_singleton_instance(self):
        # Test if the class is a singleton
        another_instance = PetDataset()
        self.assertIs(self.pet_data_instance, another_instance)

    def test_get_data(self):
        # Test if get_data() returns a DataFrame
        data = self.pet_data_instance.get_data()
        self.assertIsInstance(data, pd.DataFrame)

    def test_get_document(self):
        # Test if get_document() returns a PetDocument object
        document_number = 0
        document = self.pet_data_instance.get_document(document_number)
        self.assertTrue(hasattr(document, "name"))
        self.assertTrue(hasattr(document, "tokens"))
        self.assertTrue(hasattr(document, "ner_tags"))

    def test_get_document_by_name(self):
        # Test if get_document_by_name() returns a PetDocument object
        document_name = "doc-3.2"
        document = self.pet_data_instance.get_document_by_name(document_name)
        self.assertTrue(hasattr(document, "name"))
        self.assertTrue(hasattr(document, "tokens"))
        self.assertTrue(hasattr(document, "ner_tags"))


if __name__ == "__main__":
    unittest.main()
